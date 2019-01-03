cd C:\ProgramData\Ableton\Live 9 Standard\Resources\MIDI Remote Scripts\alzyOSC
dir
del *.pyc
xcopy /Y "C:\Users\admin\Documents\alzyOSC" "C:\ProgramData\Ableton\Live 9 Standard\Resources\MIDI Remote Scripts\alzyOSC"

break > "C:\Users\admin\AppData\Roaming\Ableton\Live 9.7.7\Preferences\Log.txt"