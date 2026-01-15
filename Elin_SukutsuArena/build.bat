@echo off
setlocal EnableDelayedExpansion

set MOD_NAME=Elin_SukutsuArena

REM 環境変数が未設定ならデフォルト値を使用
if not defined SOFFICE set "SOFFICE=C:\Program Files\LibreOffice\program\soffice.exe"
if not defined STEAM_PACKAGE_DIR set "STEAM_PACKAGE_DIR=C:\Program Files (x86)\Steam\steamapps\common\Elin\Package\%MOD_NAME%"

REM ビルド構成の設定（引数で debug を指定するとDebugビルド）
set BUILD_CONFIG=Release
if /i "%~1"=="debug" set BUILD_CONFIG=Debug

echo.
if "%BUILD_CONFIG%"=="Debug" (
    echo === %MOD_NAME% Build [DEBUG] ===
    echo   * Enemy levels fixed to 1
    echo   * Debug keys enabled: F9/F11/F12
) else (
    echo === %MOD_NAME% Build [Release] ===
)
echo.

REM ============================================================
REM Step 0: Backup Excel files for diff
REM ============================================================
pushd tools
uv run python builder/excel_diff_manager.py backup >nul 2>&1
popd

REM ============================================================
REM Step 1: Validation
REM ============================================================
<nul set /p "=[1/13] Validation... "
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
<nul set /p "=[2/13] Zone Excel... "
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
<nul set /p "=[3/13] Chara Excel... "
pushd tools
if "%BUILD_CONFIG%"=="Debug" (
    uv run python builder/create_chara_excel.py --debug >nul 2>&1
) else (
    uv run python builder/create_chara_excel.py >nul 2>&1
)
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
REM Step 4: Thing Excel (Custom Items)
REM ============================================================
<nul set /p "=[4/13] Thing Excel... "
pushd tools
if "%BUILD_CONFIG%"=="Debug" (
    uv run python builder/create_thing_excel.py --debug >nul 2>&1
) else (
    uv run python builder/create_thing_excel.py >nul 2>&1
)
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
popd
"%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\EN\Thing.tsv" --outdir "%~dp0LangMod\EN" >nul 2>&1
"%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\JP\Thing.tsv" --outdir "%~dp0LangMod\JP" >nul 2>&1
move /Y "%~dp0LangMod\EN\Thing.xlsx" "%~dp0LangMod\EN\SourceThing.xlsx" >nul 2>&1
move /Y "%~dp0LangMod\JP\Thing.xlsx" "%~dp0LangMod\JP\SourceThing.xlsx" >nul 2>&1
del "%~dp0LangMod\EN\Thing.tsv" >nul 2>&1
del "%~dp0LangMod\JP\Thing.tsv" >nul 2>&1
echo OK

REM ============================================================
REM Step 5: Merchant Stock JSON
REM ============================================================
<nul set /p "=[5/13] Merchant Stock... "
pushd tools
uv run python builder/create_merchant_stock.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
popd
echo OK

REM ============================================================
REM Step 6: Element Excel (Custom Feats)
REM ============================================================
<nul set /p "=[6/13] Element Excel... "
pushd tools
uv run python builder/create_element_excel.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
popd
"%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\EN\Element.tsv" --outdir "%~dp0LangMod\EN" >nul 2>&1
"%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\JP\Element.tsv" --outdir "%~dp0LangMod\JP" >nul 2>&1
move /Y "%~dp0LangMod\EN\Element.xlsx" "%~dp0LangMod\EN\SourceElement.xlsx" >nul 2>&1
move /Y "%~dp0LangMod\JP\Element.xlsx" "%~dp0LangMod\JP\SourceElement.xlsx" >nul 2>&1
del "%~dp0LangMod\EN\Element.tsv" >nul 2>&1
del "%~dp0LangMod\JP\Element.tsv" >nul 2>&1
echo OK

REM ============================================================
REM Step 7: Stat Excel (Custom Stats)
REM ============================================================
<nul set /p "=[7/13] Stat Excel... "
pushd tools
uv run python builder/create_stat_excel.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
popd
"%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\EN\Stat.tsv" --outdir "%~dp0LangMod\EN" >nul 2>&1
"%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\JP\Stat.tsv" --outdir "%~dp0LangMod\JP" >nul 2>&1
move /Y "%~dp0LangMod\EN\Stat.xlsx" "%~dp0LangMod\EN\SourceStat.xlsx" >nul 2>&1
move /Y "%~dp0LangMod\JP\Stat.xlsx" "%~dp0LangMod\JP\SourceStat.xlsx" >nul 2>&1
del "%~dp0LangMod\EN\Stat.tsv" >nul 2>&1
del "%~dp0LangMod\JP\Stat.tsv" >nul 2>&1
echo OK

REM ============================================================
REM Step 6: BGM JSON
REM ============================================================
<nul set /p "=[8/13] BGM JSON... "
pushd tools
uv run python builder/create_bgm_json.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
popd
echo OK

REM ============================================================
REM Step 7: Drama Excel
REM ============================================================
<nul set /p "=[9/13] Drama Excel... "
pushd tools
REM -W default enables DeprecationWarning display, >nul hides stdout but keeps stderr
uv run python -W default builder/create_drama_excel.py >nul
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    echo.
    uv run python -W default builder/create_drama_excel.py
    popd
    goto :error
)
popd
echo OK

REM ============================================================
REM Step 8: C# Flags + Quest Data
REM ============================================================
<nul set /p "=[10/13] C# Flags... "
pushd tools
uv run python builder/generate_flags.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
uv run python builder/generate_jump_label_mapping.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
uv run python builder/generate_enum_mappings.py >nul 2>&1
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
uv run python builder/generate_quest_data.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
popd
echo OK

REM ============================================================
REM Step 9: Config JSON (Quest + Battle Stages)
REM ============================================================
<nul set /p "=[11/13] Config JSON... "
pushd tools\common
uv run python -c "from quest_dependencies import export_quests_to_json; import os; export_quests_to_json(os.path.join('..', '..', 'Package', 'quest_definitions.json'))" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
REM DEBUGビルドの場合は全敵レベル1に設定
if "%BUILD_CONFIG%"=="Debug" (
    uv run python -c "from battle_stages import export_stages_to_json; import os; export_stages_to_json(os.path.join('..', '..', 'Package', 'battle_stages.json'), debug_mode=True)" >nul 2>&1
) else (
    uv run python -c "from battle_stages import export_stages_to_json; import os; export_stages_to_json(os.path.join('..', '..', 'Package', 'battle_stages.json'), debug_mode=False)" >nul 2>&1
)
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    popd
    goto :error
)
popd
echo OK

REM ============================================================
REM Step 10: dotnet build
REM ============================================================
<nul set /p "=[12/13] dotnet build (%BUILD_CONFIG%)... "
dotnet build "%~dp0%MOD_NAME%.csproj" -c %BUILD_CONFIG% -v q --nologo >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FAILED
    echo.
    echo ============================================================
    echo BUILD ERROR - Details:
    echo ============================================================
    dotnet build "%~dp0%MOD_NAME%.csproj" -c %BUILD_CONFIG%
    goto :error
)
echo OK

REM ============================================================
REM Step 11: Deploy
REM ============================================================
<nul set /p "=[13/13] Deploy... "

REM Package folder
xcopy "%~dp0_bin\%MOD_NAME%.dll" "%~dp0elin_link\Package\%MOD_NAME%\" /Y /Q >nul 2>&1
xcopy "%~dp0package.xml" "%~dp0elin_link\Package\%MOD_NAME%\" /Y /Q >nul 2>&1
xcopy "%~dp0Package\quest_definitions.json" "%~dp0elin_link\Package\%MOD_NAME%\Package\" /Y /I /Q >nul 2>&1
xcopy "%~dp0Package\battle_stages.json" "%~dp0elin_link\Package\%MOD_NAME%\Package\" /Y /I /Q >nul 2>&1
xcopy "%~dp0LangMod" "%~dp0elin_link\Package\%MOD_NAME%\LangMod\" /E /Y /I /Q >nul 2>&1
xcopy "%~dp0Texture" "%~dp0elin_link\Package\%MOD_NAME%\Texture\" /E /Y /I /Q >nul 2>&1
xcopy "%~dp0Portrait" "%~dp0elin_link\Package\%MOD_NAME%\Portrait\" /E /Y /I /Q >nul 2>&1
xcopy "%~dp0Media" "%~dp0elin_link\Package\%MOD_NAME%\Media\" /E /Y /I /Q >nul 2>&1
xcopy "%~dp0Sound" "%~dp0elin_link\Package\%MOD_NAME%\Sound\" /E /Y /I /Q >nul 2>&1

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
xcopy "%~dp0Sound" "%STEAM_PACKAGE_DIR%\Sound\" /E /Y /I /Q >nul 2>&1
echo OK

REM ============================================================
REM Show Excel Diff
REM ============================================================
echo.
echo --- Excel Changes ---
pushd tools
uv run python builder/excel_diff_manager.py diff
popd

echo.
echo === Build Complete ===
endlocal
exit /b 0

:error
echo.
echo === Build Failed ===
endlocal
exit /b 1
