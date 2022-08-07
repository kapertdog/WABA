echo Off
cls
echo Make sure that you have Python3.10!!!
pause
py -m venv ".\updater\waba_additional_files\venv"
".\updater\waba_additional_files\venv\Scripts\pip.exe" install -r ".\updater\requirements.txt"