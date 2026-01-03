@echo off
setlocal

set MOD_NAME=Elin_SukutsuArena

echo Generating Source.tsv (Zone.tsv)
pushd tools
uv run python create_zone_excel.py
popd

echo Converting tsv to xlsx (requires LibreOffice)
set SOFFICE="C:\Program Files\LibreOffice\program\soffice.exe"
if exist %SOFFICE% (
    %SOFFICE% --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\EN\Zone.tsv" --outdir "%~dp0LangMod\EN"
    %SOFFICE% --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\JP\Zone.tsv" --outdir "%~dp0LangMod\JP"

    echo Renaming Zone.xlsx to SourceSukutsu.xlsx
    move /Y "%~dp0LangMod\EN\Zone.xlsx" "%~dp0LangMod\EN\SourceSukutsu.xlsx"
    move /Y "%~dp0LangMod\JP\Zone.xlsx" "%~dp0LangMod\JP\SourceSukutsu.xlsx"

    echo Cleaning up TSV files (Zone)
    del "%~dp0LangMod\EN\Zone.tsv"
    del "%~dp0LangMod\JP\Zone.tsv"

    REM --- Chara Pipeline ---
    echo Generating Chara.tsv
    pushd tools
    uv run python create_chara_excel.py
    popd

    %SOFFICE% --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\EN\Chara.tsv" --outdir "%~dp0LangMod\EN"
    %SOFFICE% --headless --convert-to "xlsx:Calc MS Excel 2007 XML" --infilter="CSV:9,34,76" "%~dp0LangMod\JP\Chara.tsv" --outdir "%~dp0LangMod\JP"

    echo Renaming Chara.xlsx to SourceChara.xlsx...
    move /Y "%~dp0LangMod\EN\Chara.xlsx" "%~dp0LangMod\EN\SourceChara.xlsx"
    move /Y "%~dp0LangMod\JP\Chara.xlsx" "%~dp0LangMod\JP\SourceChara.xlsx"

    echo Cleaning up TSV files (Chara)...
    del "%~dp0LangMod\EN\Chara.tsv"
    del "%~dp0LangMod\JP\Chara.tsv"
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

echo Copying to Package folder...
xcopy "%~dp0_bin\%MOD_NAME%.dll" "%~dp0elin_link\Package\%MOD_NAME%\" /Y
xcopy "%~dp0package.xml" "%~dp0elin_link\Package\%MOD_NAME%\" /Y
xcopy "%~dp0LangMod" "%~dp0elin_link\Package\%MOD_NAME%\LangMod\" /E /Y /I
xcopy "%~dp0Texture" "%~dp0elin_link\Package\%MOD_NAME%\Texture\" /E /Y /I
xcopy "%~dp0Portrait" "%~dp0elin_link\Package\%MOD_NAME%\Portrait\" /E /Y /I

echo Copying to Steam game folder...
set STEAM_PACKAGE_DIR="C:\Program Files (x86)\Steam\steamapps\common\Elin\Package\%MOD_NAME%"
if not exist %STEAM_PACKAGE_DIR% mkdir %STEAM_PACKAGE_DIR%
xcopy "%~dp0_bin\%MOD_NAME%.dll" %STEAM_PACKAGE_DIR% /Y
xcopy "%~dp0package.xml" %STEAM_PACKAGE_DIR% /Y
xcopy "%~dp0LangMod" %STEAM_PACKAGE_DIR%\LangMod\ /E /Y /I
xcopy "%~dp0Texture" %STEAM_PACKAGE_DIR%\Texture\ /E /Y /I
xcopy "%~dp0Portrait" %STEAM_PACKAGE_DIR%\Portrait\ /E /Y /I

endlocal
