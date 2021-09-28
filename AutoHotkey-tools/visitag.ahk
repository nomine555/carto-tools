#NoEnv  
#Warn   
SendMode Input               
SetWorkingDir %A_ScriptDir%  
CoordMode, Mouse, Screen

i := 0
max := 11

; Esperamos a la pantalla de inicio
Start:

Loop {

Click, 960,  0
Sleep, 1000

WinGetTitle, title, A
title = % SubStr(title,7)

If  (title = 3)
	break

}

; Seleccionamos un estudio
Click, 960,  0
Sleep, 1000
Click, 992, 688
Sleep, 1000

; Study Date
Click, 408,457
Sleep, 1000

; Order by Date
Click, 264,500
Sleep, 1000

Click, 573,538
Sleep, 1000

Loop, %i% {
	Send, {Down}
	Sleep, 500
}

;Cancelamos
;Click, 1682,835
;Sleep, 1000


; Esperamos a que carge el Estudio

Click, 1560,835
Sleep, 1000

Loop {
	Click, 960,  0
	Sleep, 1000
	WinGetTitle, title, A
	if (title = "CARTO")
		break
	Sleep, 5000
}


Click, 960,  0
Sleep, 1000
Click, 35, 13
Sleep, 1000
Click, 164,160
Sleep, 1000
Click, 1580,236
Sleep, 1000
Click, 1580,312
Sleep, 1000
Click, 1580,350
Sleep, 1000
Click, 1718,472

Loop {
	Sleep, 5000
	WinGetTitle, title, A
	if (title = "GeneralProgressForm")
		continue
	else
		break
}


Click, 35, 13
Sleep, 1000
Click, 137, 223
Sleep, 1000

i++
if (i == max)
    	; ExitApp
	Shutdown, 12
else
	GoTo, Start


Esc::ExitApp  ; Exit script with Escape key

