@echo off
setlocal
set "ROOT=%~dp0.."
set "JAVA_OUT=%TEMP%\dft-test-%RANDOM%-%RANDOM%"
set "FAILED=0"

pushd "%ROOT%" || exit /b 1

echo ===== Python tests =====
python "DFT test\run_python_tests.py"
if errorlevel 1 set "FAILED=1"

echo.
echo ===== Compile Java tests =====
mkdir "%JAVA_OUT%" >nul 2>&1
javac -encoding UTF-8 -d "%JAVA_OUT%" "BonusService.java" "RiskService.java" "DFT test\BonusServiceTest.java" "DFT test\RiskServiceTest.java"
if errorlevel 1 (
    set "FAILED=1"
) else (
    echo.
    echo ===== BonusService tests =====
    java -cp "%JAVA_OUT%" BonusServiceTest
    if errorlevel 1 set "FAILED=1"

    echo.
    echo ===== RiskService tests =====
    java -cp "%JAVA_OUT%" RiskServiceTest
    if errorlevel 1 set "FAILED=1"
)

if exist "%JAVA_OUT%" rmdir /s /q "%JAVA_OUT%"
popd

echo.
if "%FAILED%"=="0" (
    echo All tests passed.
) else (
    echo One or more tests failed. See the case-level results above.
)
exit /b %FAILED%
