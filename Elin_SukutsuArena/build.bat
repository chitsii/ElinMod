@echo off
setlocal EnableDelayedExpansion

set MOD_NAME=Elin_SukutsuArena
set "SOFFICE=C:\Program Files\LibreOffice\program\soffice.exe"
set STEAM_PACKAGE_DIR=C:\Program Files (x86)\Steam\steamapps\common\Elin\Package\%MOD_NAME%

echo.
echo === %MOD_NAME% Build ===
echo.

REM ============================================================
REM Step 1: Validation
REM ============================================================
<nul set /p "=[1/8] Validation... "
pushd tools\common
uv run python validation.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    echo.
    echo ============================================================
    echo VALIDATION ERROR - Details:
    echo ============================================================
    uv run python validation.py
    popd
    goto :error
)
popd
echo OK

REM ============================================================
REM Step 2: Zone Excel
REM ============================================================
<nul set /p "=[2/8] Zone Excel... "
pushd tools
uv run python builder/create_zone_excel.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
popd
"%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\EN\Zone.tsv" --outdir "%~dp0LangMod\EN" >nul 2>&1
"%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\JP\Zone.tsv" --outdir "%~dp0LangMod\JP" >nul 2>&1
move /Y "%~dp0LangMod\EN\Zone.xlsx" "%~dp0LangMod\EN\SourceSukutsu.xlsx" >nul 2>&1
move /Y "%~dp0LangMod\JP\Zone.xlsx" "%~dp0LangMod\JP\SourceSukutsu.xlsx" >nul 2>&1
del "%~dp0LangMod\EN\Zone.tsv" >nul 2>&1
del "%~dp0LangMod\JP\Zone.tsv" >nul 2>&1
echo OK

REM ============================================================
REM Step 3: Chara Excel
REM ============================================================
<nul set /p "=[3/8] Chara Excel... "
pushd tools
uv run python builder/create_chara_excel.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
popd
"%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\EN\Chara.tsv" --outdir "%~dp0LangMod\EN" >nul 2>&1
"%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\JP\Chara.tsv" --outdir "%~dp0LangMod\JP" >nul 2>&1
move /Y "%~dp0LangMod\EN\Chara.xlsx" "%~dp0LangMod\EN\SourceChara.xlsx" >nul 2>&1
move /Y "%~dp0LangMod\JP\Chara.xlsx" "%~dp0LangMod\JP\SourceChara.xlsx" >nul 2>&1
del "%~dp0LangMod\EN\Chara.tsv" >nul 2>&1
del "%~dp0LangMod\JP\Chara.tsv" >nul 2>&1
echo OK

REM ============================================================
REM Step 4: Drama Excel
REM ============================================================
<nul set /p "=[4/8] Drama Excel... "
pushd tools
uv run python builder/create_drama_excel.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    echo.
    uv run python builder/create_drama_excel.py
    popd
    goto :error
)
uv run python builder/create_opening_drama.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
popd
echo OK

REM ============================================================
REM Step 5: C# Flags
REM ============================================================
<nul set /p "=[5/8] C# Flags... "
pushd tools
uv run python builder/generate_flags.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
uv run python builder/validate_scenario_flags.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    echo.
    echo ============================================================
    echo FLAG VALIDATION ERROR - Details:
    echo ============================================================
    uv run python builder/validate_scenario_flags.py
    popd
    goto :error
)
popd
echo OK

REM ============================================================
REM Step 6: Config JSON (Quest + Battle Stages)
REM ============================================================
<nul set /p "=[6/8] Config JSON... "
pushd tools\common
uv run python -c "from quest_dependencies import export_quests_to_json; import os; export_quests_to_json(os.path.join('..', '..', 'Package', 'quest_definitions.json'))" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
uv run python -c "from battle_stages import export_stages_to_json; import os; export_stages_to_json(os.path.join('..', '..', 'Package', 'battle_stages.json'))" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
popd
echo OK

REM ============================================================
REM Step 7: dotnet build
REM ============================================================
<nul set /p "=[7/8] dotnet build... "
dotnet build "%~dp0%MOD_NAME%.csproj" -c Release -v q --nologo >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    echo.
    echo ============================================================
    echo BUILD ERROR - Details:
    echo ============================================================
    dotnet build "%~dp0%MOD_NAME%.csproj" -c Release
    goto :error
)
echo OK

REM ============================================================
REM Step 8: Deploy
REM ============================================================
<nul set /p "=[8/8] Deploy... "

REM Package folder
xcopy "%~dp0_bin\%MOD_NAME%.dll" "%~dp0elin_link\Package\%MOD_NAME%\" /Y /Q >nul 2>&1
xcopy "%~dp0package.xml" "%~dp0elin_link\Package\%MOD_NAME%\" /Y /Q >nul 2>&1
xcopy "%~dp0Package\quest_definitions.json" "%~dp0elin_link\Package\%MOD_NAME%\Package\" /Y /I /Q >nul 2>&1
xcopy "%~dp0Package\battle_stages.json" "%~dp0elin_link\Package\%MOD_NAME%\Package\" /Y /I /Q >nul 2>&1
xcopy "%~dp0LangMod" "%~dp0elin_link\Package\%MOD_NAME%\LangMod\" /E /Y /I /Q >nul 2>&1
xcopy "%~dp0Texture" "%~dp0elin_link\Package\%MOD_NAME%\Texture\" /E /Y /I /Q >nul 2>&1
xcopy "%~dp0Portrait" "%~dp0elin_link\Package\%MOD_NAME%\Portrait\" /E /Y /I /Q >nul 2>&1
xcopy "%~dp0Media" "%~dp0elin_link\Package\%MOD_NAME%\Media\" /E /Y /I /Q >nul 2>&1

REM Steam folder
if not exist "%STEAM_PACKAGE_DIR%" mkdir "%STEAM_PACKAGE_DIR%" >nul 2>&1
xcopy "%~dp0_bin\%MOD_NAME%.dll" "%STEAM_PACKAGE_DIR%\" /Y /Q >nul 2>&1
xcopy "%~dp0package.xml" "%STEAM_PACKAGE_DIR%\" /Y /Q >nul 2>&1
xcopy "%~dp0Package\quest_definitions.json" "%STEAM_PACKAGE_DIR%\Package\" /Y /I /Q >nul 2>&1
xcopy "%~dp0Package\battle_stages.json" "%STEAM_PACKAGE_DIR%\Package\" /Y /I /Q >nul 2>&1
xcopy "%~dp0LangMod" "%STEAM_PACKAGE_DIR%\LangMod\" /E /Y /I /Q >nul 2>&1
xcopy "%~dp0Texture" "%STEAM_PACKAGE_DIR%\Texture\" /E /Y /I /Q >nul 2>&1
xcopy "%~dp0Portrait" "%STEAM_PACKAGE_DIR%\Portrait\" /E /Y /I /Q >nul 2>&1
xcopy "%~dp0Media" "%STEAM_PACKAGE_DIR%\Media\" /E /Y /I /Q >nul 2>&1
echo OK

echo.
echo === Build Complete ===
endlocal
exit /b 0

:error
echo.
echo === Build Failed ===
endlocal
exit /b 1
