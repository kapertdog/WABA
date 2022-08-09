echo Off
cls
echo ## Make sure that you have Python3.10!!!
echo ## Creating new venv...
py -m venv ".\venv"
echo ## Installing requirements...
".\venv\Scripts\pip.exe" install -r %appdata%\waba\requirements.txt