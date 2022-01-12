<#
	.SYNOPSIS
	Uninstall fonts from Windows system.
	.DESCRIPTION
	Uninstall and delete fonts from Windows system.
	.PARAMETER FontFamily
	The font family name to uninstall (wildcards could be added).
	.EXAMPLE
	Uninstall-Font -FontFamily font
	Uninstall provided font from Windows system.
#>
param
(
	[Parameter(Mandatory = $true)]
	[string]$FontFamily
)
begin
{
	# If not currently running "as Administrator"...
	If (-Not $(new-object System.Security.Principal.WindowsPrincipal([System.Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator))
	{
		Write-Error "This command must be run with administrator privileges."
		Exit
	}
	# Load P/Invoke calls
	Add-Type -Name Fonts -Namespace System -MemberDefinition @"
		/// <summary>The window handle value to send a message to all top-level windows in the system, including disabled or invisible unowned windows, overlapped windows, and pop-up windows. The message is not posted to child windows.</summary>
		public static IntPtr HWND_BROADCAST = new IntPtr(0xffff);
		/// <summary>The Windows message sent to all top-level windows in the system after changing the pool of font resources.</summary>
		public static uint WM_FONTCHANGE = 0x001D;
		/// <summary>Removes the fonts in the specified file from the system font table.</summary>
		/// <param name="lpFilename">The path of the font resources file.</param>
		/// <returns>
		///     If the function succeeds, the return value is nonzero.
		///     If the function fails, the return value is zero.
		/// </returns>
		/// <remarks>
		///     Any application that adds or removes fonts from the system font table should notify other windows of the change by sending a <see cref="WM_FONTCHANGE"/> message to all top-level windows in the operating system. The application should send this message by calling the SendMessage (or <see cref="PostMessage"/>) function and setting the hWnd parameter to <see cref="HWND_BROADCAST"/>.
		///     If there are outstanding references to a font, the associated resource remains loaded until no device context is using it. Furthermore, if the font is listed in the font registry (HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts) and is installed to any location other than the %windir%\fonts\ folder, it may be loaded into other active sessions (including session 0).
		///     When you try to replace an existing font file that contains a font with outstanding references to it, you might get an error that indicates that the original font can't be deleted because it’s in use even after you call RemoveFontResource. If your app requires that the font file be replaced, to reduce the resource count of the original font to zero, call RemoveFontResource in a loop as shown in this example code. If you continue to get errors, this is an indication that the font file remains loaded in other sessions. Make sure the font isn't listed in the font registry and restart the system to ensure the font is unloaded from all sessions.
		/// </remarks>
		[DllImport("gdi32.dll")]
		public static extern bool RemoveFontResource(string lpFilename);
		/// <summary>
		///     Places (posts) a message in the message queue associated with the thread that created the specified window and returns without waiting for the thread to process the message.
		/// </summary>
		/// <param name="hWnd">
		///     A handle to the window whose window procedure is to receive the message. The following values have special meanings.
		///     <list type="table">
		///         <listheader>
		///             <term>Value</term>
		///             <description>Meaning</description>
		///         </listheader>
		///         <item>
		///             <term>HWND_BROADCAST ((HWND)0xffff)</term>
		///             <description>The message is posted to all top-level windows in the system, including disabled or invisible unowned windows, overlapped windows, and pop-up windows. The message is not posted to child windows.</description>
		///         </item>
		///         <item>
		///             <term>NULL</term>
		///             <description>The function behaves like a call to PostThreadMessage with the dwThreadId parameter set to the identifier of the current thread.</description>
		///         </item>
		///     </list>
		///     Starting with Windows Vista, message posting is subject to UIPI. The thread of a process can post messages only to message queues of threads in processes of lesser or equal integrity level.
		/// </param>
		/// <param name="Msg">
		///     The message to be posted.
		///     For lists of the system-provided messages, see <see href="https://msdn.microsoft.com/en-us/library/windows/desktop/ms644927(v=vs.85).aspx#system_defined">System-Defined Messages</see>.
		/// </param>
		/// <param name="wParam">Additional message-specific information.</param>
		/// <param name="lParam">Additional message-specific information.</param>
		/// <returns>
		///     If the function succeeds, the return value is nonzero.
		///     If the function fails, the return value is zero. To get extended error information, call GetLastError. GetLastError returns ERROR_NOT_ENOUGH_QUOTA when the limit is hit.
		/// </returns>
		/// <remarks>
		///     When a message is blocked by UIPI the last error, retrieved with GetLastError, is set to 5 (access denied).
		///     Messages in a message queue are retrieved by calls to the GetMessage or PeekMessage function.
		///     Applications that need to communicate using HWND_BROADCAST should use the RegisterWindowMessage function to obtain a unique message for inter-application communication.
		/// </remarks>
		[return: MarshalAs(UnmanagedType.Bool)]
		[DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
		public static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
"@
}
process
{
	# For each font resource file...
	foreach ($fontRegistryEntry in ((Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts").PSObject.Properties | Where-Object { $_.Name -match $FontFamily }))
	{
		# Unregister and remove the font file...
		$fontPath = Join-Path ([System.Environment]::GetFolderPath("Fonts")) $fontRegistryEntry.Value
		if (Test-Path $fontPath)
		{
			if ([Fonts]::RemoveFontResource($fontPath))
			{
				[Fonts]::PostMessage([Fonts]::HWND_BROADCAST, [Fonts]::WM_FONTCHANGE, [IntPtr]::Zero, [IntPtr]::Zero) | Out-Null
				Write-Host "Font $($fontRegistryEntry.Value) unregistered." -ForegroundColor Yellow
			}
			if (Test-Path $fontPath) { Remove-Item $fontPath -Force }
			Write-Host "Font $fontPath removed." -ForegroundColor Yellow
		}
	}
}
end { }