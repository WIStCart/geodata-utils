:: Run this script inside of the Esri "Python Command Prompt"
:: E.g. C:\install scripts\> install.bat

:: Create and activate python environment
CALL create_python_env.bat

:: Install geodata-utils python library
python -m pip install --upgrade https://github.com/WIStCart/geodata-utils/archive/main.tar.gz

:: Open config so it can be set by user
for /f "delims=" %%i in ('python -c "from distutils.sysconfig import get_python_lib; from os.path import join; print(join(get_python_lib(),'geodatautils','config'))"') do set configpath=%%i
ren %configpath%\config-template.yml config.yml
notepad %configpath%\config.yml