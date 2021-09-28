#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn   ; Enable warnings to assist with detecting common errors.

SendMode Input               ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

; ControlClick, Button2, WindowTitle

CoordMode, Mouse, Screen
Start: 
IfWinExist, ahk_class WindowsForms10.Window.8.app.0.3b32ee5_r12_ad1
{
ControlGet, OutputVar, Enabled,, Skip, ahk_class WindowsForms10.Window.8.app.0.3b32ee5_r12_ad1
	if (OutputVar = 1)
		Click, 1200,  720	
}
Sleep, 3000 
Goto Start
