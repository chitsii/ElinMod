@echo off
setlocal

set MOD_NAME=Elin_SukutsuArena

echo Generating Source.tsv (Zone.tsv)
pushd tools
uv run python builder/create_zone_excel.py
popd

echo Converting tsv to xlsx (requires LibreOffice)
set "SOFFICE=C:\Program Files\LibreOffice\program\soffice.exe"
if exist "%SOFFICE%" (
    "%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\EN\Zone.tsv" --outdir "%~dp0LangMod\EN"
    "%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\JP\Zone.tsv" --outdir "%~dp0LangMod\JP"

    echo Renaming Zone.xlsx to SourceSukutsu.xlsx
    move /Y "%~dp0LangMod\EN\Zone.xlsx" "%~dp0LangMod\EN\SourceSukutsu.xlsx"
    move /Y "%~dp0LangMod\JP\Zone.xlsx" "%~dp0LangMod\JP\SourceSukutsu.xlsx"

    echo Cleaning up TSV files (Zone)
    del "%~dp0LangMod\EN\Zone.tsv"
    del "%~dp0LangMod\JP\Zone.tsv"

    REM --- Chara Pipeline ---
    echo Generating Chara.tsv
    pushd tools
    uv run python builder/create_chara_excel.py
    popd

    "%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\EN\Chara.tsv" --outdir "%~dp0LangMod\EN"
    "%SOFFICE%" --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\JP\Chara.tsv" --outdir "%~dp0LangMod\JP"

    echo Renaming Chara.xlsx to SourceChara.xlsx...
    move /Y "%~dp0LangMod\EN\Chara.xlsx" "%~dp0LangMod\EN\SourceChara.xlsx"
    move /Y "%~dp0LangMod\JP\Chara.xlsx" "%~dp0LangMod\JP\SourceChara.xlsx"

    echo Cleaning up TSV files (Chara)...
    del "%~dp0LangMod\EN\Chara.tsv"
    del "%~dp0LangMod\JP\Chara.tsv"
    REM ----------------------

    REM --- Drama Pipeline (openpyxl直接生成) ---
    echo Generating Drama Excel files...
    pushd tools
    uv run python builder/create_drama_excel.py
    uv run python builder/create_opening_drama.py
    popd
    REM ----------------------

    REM --- Flag System Pipeline ---
    echo Generating C# Flag Classes...
    pushd tools
    uv run python builder/generate_flags.py
    popd

    echo Validating Scenario Flags...
    pushd tools
    uv run python builder/validate_scenario_flags.py
    if %ERRORLEVEL% NEQ 0 (
        echo Flag Validation Failed!
        popd
        exit /b 1
    )
    popd
    REM ----------------------

    echo Conversion complete.
) else (
    echo WARNING: LibreOffice not found at %SOFFICE%. Skipping compatibility fix.
    echo Please install LibreOffice or manually save SourceSukutsu.tsv as .xlsx.
)

echo Compiling with dotnet...
dotnet build "%~dp0%MOD_NAME%.csproj" -c Release

if %ERRORLEVEL% NEQ 0 (
    echo Build Failed!
    exit /b 1
)

echo Build Successful!

REM Quiet copy to Package folder
echo Deploying to Package folder...
xcopy "%~dp0_bin\%MOD_NAME%.dll" "%~dp0elin_link\Package\%MOD_NAME%\" /Y /Q >nul
xcopy "%~dp0package.xml" "%~dp0elin_link\Package\%MOD_NAME%\" /Y /Q >nul
xcopy "%~dp0LangMod" "%~dp0elin_link\Package\%MOD_NAME%\LangMod\" /E /Y /I /Q >nul
xcopy "%~dp0Texture" "%~dp0elin_link\Package\%MOD_NAME%\Texture\" /E /Y /I /Q >nul
xcopy "%~dp0Portrait" "%~dp0elin_link\Package\%MOD_NAME%\Portrait\" /E /Y /I /Q >nul
xcopy "%~dp0Sound" "%~dp0elin_link\Package\%MOD_NAME%\Sound\" /E /Y /I /Q >nul
echo   Done.

REM Quiet copy to Steam game folder
echo Deploying to Steam folder...
set STEAM_PACKAGE_DIR="C:\Program Files (x86)\Steam\steamapps\common\Elin\Package\%MOD_NAME%"
if not exist %STEAM_PACKAGE_DIR% mkdir %STEAM_PACKAGE_DIR%
xcopy "%~dp0_bin\%MOD_NAME%.dll" %STEAM_PACKAGE_DIR% /Y /Q >nul
xcopy "%~dp0package.xml" %STEAM_PACKAGE_DIR% /Y /Q >nul
xcopy "%~dp0LangMod" %STEAM_PACKAGE_DIR%\LangMod\ /E /Y /I /Q >nul
xcopy "%~dp0Texture" %STEAM_PACKAGE_DIR%\Texture\ /E /Y /I /Q >nul
xcopy "%~dp0Portrait" %STEAM_PACKAGE_DIR%\Portrait\ /E /Y /I /Q >nul
xcopy "%~dp0Sound" %STEAM_PACKAGE_DIR%\Sound\ /E /Y /I /Q >nul
echo   Done.

echo.
echo === Build Complete ===

endlocal
