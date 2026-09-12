@echo off
chcp 65001 >nul
title SALVAGE STATION - Deploy
cd /d "%~dp0"

echo.
echo   SALVAGE STATION - GitHub 배포
echo   ==================================
echo.

REM 1) index.html 동기화
echo [1/4] index.html 동기화...
copy /Y salvage_station.html index.html >nul
if errorlevel 1 (
    echo   [오류] salvage_station.html 을 찾을 수 없습니다.
    pause & exit /b 1
)

REM 2) 변경사항 확인
echo.
echo [2/4] 변경사항:
git status --short
echo.

REM 커밋할 것이 없으면 종료
git diff --cached --quiet
if not errorlevel 1 (
    git diff --quiet
    if not errorlevel 1 (
        echo   변경사항이 없습니다. 종료합니다.
        pause & exit /b 0
    )
)

REM 3) 커밋 메시지 입력
echo [3/4] 커밋 메시지를 입력하세요 (엔터만 치면 "Update game"):
set /p MSG=  ^>^>
if "%MSG%"=="" set MSG=Update game

git add -A
git commit -m "%MSG%"
if errorlevel 1 (
    echo   [오류] 커밋 실패
    pause & exit /b 1
)

REM 4) 푸시
echo.
echo [4/4] GitHub 푸시 중...
git push
if errorlevel 1 (
    echo   [오류] 푸시 실패 - 원격 저장소 인증을 확인하세요.
    pause & exit /b 1
)

echo.
echo   ==================================
echo   배포 완료!
echo   확인: https://maker1243.github.io/space/
echo   (Pages 반영까지 1~2분 소요)
echo   ==================================
pause
