echo off

set source_path=boom

set install_path=%LOCALAPPDATA%\Programs
set install_folder_name=boom-zip
set install_folder=%install_path%\%install_folder_name%

move %source_path% %install_folder%
echo Moved %source_path% to %install_folder%

rem set desktop=%USERPROFILE%\OneDrive - Colonial First State\Desktop
rem echo Creating link on desktop: %desktop%
rem mklink "%install_folder%\boom.exe" "%desktop%\boom-zip.lnk"

rem echo A shortcut to boom-zip should appear on your desktop. Drag and drop files or folders onto the shortcut to zip and encrypt them.

pause