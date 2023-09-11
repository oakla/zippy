@REM Create a venv in the current directory 
@REM Activate the venv 
@REM Upgrade to the latest pip 
@REM Note: There are better ways to do this, but this will do for now.  

@ECHO OFF 

Set "VENV=.venv" 

If Not Exist "%VENV%\Scripts\activate.bat" ( 
    ECHO Creating venv 
    Call python -m venv %VENV% 
) 

If Not Exist "%VENV%\Scripts\activate.bat" ( 
    ECHO Failed to create venv 
    Exit /B 1 
) 

ECHO Activating venv 
Call "%VENV%\Scripts\activate.bat" 
ECHO Upgrading pip 
Call python -m pip install --upgrade pip 

Call python -m pip install -e .

Pause 
Exit /B 0 

