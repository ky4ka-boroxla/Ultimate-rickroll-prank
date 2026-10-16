@echo off
if exist dist rmdir /s /q dist
python -m nuitka --msvc=latest  --standalone --onefile --plugin-enable=tk-inter --windows-console-mode=disable --windows-uac-admin --windows-icon-from-ico="icon.ico" --include-data-files="rick.avi=rick.avi" --output-filename="Steam_Online_Fix.exe" --output-dir=dist prank.py
pause