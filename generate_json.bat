@echo off

if "%~1" == "" (
	echo You must supply the name of a json file to save to
	exit /b 1
)

if not exist global-v35 (
	echo No save file found with name global-v35
	exit /b 1
)

copy global-v35 tmp.gz
7z.exe e -y tmp.gz
type tmp | python -m json.tool > %1
del tmp.gz tmp

