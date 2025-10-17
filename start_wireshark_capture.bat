@echo off
REM ============================================================
REM Wireshark Packet Capture for GE-SRTP Research
REM ============================================================

set PLC_IP=172.16.12.124
set PLC_PORT=18245
set INTERFACE=Ethernet
set OUTPUT_FILE=plc_srtp_capture_%DATE:~-4,4%%DATE:~-10,2%%DATE:~-7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%.pcapng
set OUTPUT_FILE=%OUTPUT_FILE: =0%

echo ============================================================
echo GE-SRTP Packet Capture
echo ============================================================
echo PLC IP:       %PLC_IP%
echo PLC Port:     %PLC_PORT%
echo Interface:    %INTERFACE%
echo Output File:  %OUTPUT_FILE%
echo.
echo Press Ctrl+C to stop capture
echo ============================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires Administrator privileges
    echo.
    echo Please run:
    echo   Right-click this batch file
    echo   Select "Run as administrator"
    pause
    exit /b 1
)

REM Start capture using dumpcap
"C:\Program Files\Wireshark\dumpcap.exe" ^
    -i "%INTERFACE%" ^
    -f "host %PLC_IP% and port %PLC_PORT%" ^
    -w "%OUTPUT_FILE%"

REM When stopped, show summary
echo.
echo ============================================================
echo Capture complete!
echo File saved: %OUTPUT_FILE%
echo.
echo To analyze:
echo   Open %OUTPUT_FILE% in Wireshark
echo ============================================================
pause
