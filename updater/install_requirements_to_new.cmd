echo Off
cls
echo ## Make sure that you have Python3.10!!!
echo ## Creating new venv...
py -m venv ".\updater\waba_additional_files\venv"
echo ## Installing requirements...
".\updater\waba_additional_files\venv\Scripts\pip.exe" install -r ".\updater\requirements.txt"