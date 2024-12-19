@echo off

if "%~1" == "" (
	echo You must supply the name of a json file to generate a save file from
	exit /b 1
)

if not exist %1 (
	echo File %1 not found
	exit /b 1
)

if exist global-v35 move /Y global-v35 OLD_global-v35

REM compact the json
type %1 | python -m json.tool --compact > tmp_compact.json

REM gzip it
7z.exe a global-v35.gz tmp_compact.json
del tmp_compact.json

move /Y global-v35.gz global-v35

