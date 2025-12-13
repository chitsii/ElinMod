@echo off
setlocal

call "%~dp0config.bat"

set CSC_PATH="C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
if not exist %CSC_PATH% (
    set CSC_PATH="C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"
)

if not exist %CSC_PATH% (
    echo csc.exe not found!
    exit /b 1
)

echo Using csc at %CSC_PATH%

if not exist "%~dp0_bin" mkdir "%~dp0_bin"

echo Compiling...
%CSC_PATH% /target:library /out:"%~dp0_bin\Elin_ItemRelocator.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\Elin.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\UnityEngine.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\UnityEngine.CoreModule.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\UnityEngine.UI.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\UnityEngine.TextRenderingModule.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\UnityEngine.UIModule.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\UnityEngine.InputLegacyModule.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\Plugins.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\Plugins.BaseCore.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\Plugins.UI.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\Plugins.Sound.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\Newtonsoft.Json.dll" ^
    /reference:"%~dp0elin_link\Elin_Data\Managed\DOTween.dll" ^
    /reference:"%~dp0elin_link\BepInEx\core\BepInEx.Core.dll" ^
    /reference:"%~dp0elin_link\BepInEx\core\BepInEx.Unity.dll" ^
    /reference:"%~dp0elin_link\BepInEx\core\0Harmony.dll" ^
    /reference:"System.Core.dll" ^
    "%~dp0src\Elin_ItemRelocator.cs" ^
    "%~dp0src\LayerItemRelocator.cs" ^
    "%~dp0src\RelocationProfile.cs" ^
    "%~dp0src\RelocatorManager.cs" ^
    "%~dp0src\Singleton.cs" ^
    "%~dp0src\RelocatorLang.cs" ^
    "%~dp0src\RelocatorPickers.cs"

if %ERRORLEVEL% NEQ 0 (
    echo Build Failed!
    exit /b 1
)

echo Build Successful!
echo Copying to Package folder...
xcopy "%~dp0_bin\Elin_ItemRelocator.dll" "%~dp0elin_link\Package\Elin_ItemRelocator\" /Y
xcopy "%~dp0package.xml" "%~dp0elin_link\Package\Elin_ItemRelocator\" /Y

echo Copying to Steam game folder...
set STEAM_PACKAGE_DIR="C:\Program Files (x86)\Steam\steamapps\common\Elin\Package\Elin_ItemRelocator"
if not exist %STEAM_PACKAGE_DIR% mkdir %STEAM_PACKAGE_DIR%
xcopy "%~dp0_bin\Elin_ItemRelocator.dll" %STEAM_PACKAGE_DIR% /Y
xcopy "%~dp0package.xml" %STEAM_PACKAGE_DIR% /Y

endlocal
