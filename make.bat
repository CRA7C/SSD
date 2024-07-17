@echo off

:: Define variables
set DOCS_DIR=docs
set DIST_DIR=dist
set BUILD_DIR=build

:: Create make targets
if "%1" == "help" goto help
if "%1" == "install" goto install
if "%1" == "doc" goto doc
if "%1" == "whl" goto whl
if "%1" == "html" goto html
if "%1" == "all" goto all
if "%1" == "clean" goto clean
if "%1" == "pylint" goto pylint
goto end

:help
echo Available targets:
echo install - Install dependencies from requirements.txt
echo doc     - Build the documentation
echo whl     - Build the Python wheel
echo html    - Build HTML documentation
echo all     - Run all targets (clean, pylint, doc, whl)
echo clean   - Clean the build and dist directories
echo pylint  - Run pylint on source directories
goto end


:install
echo Installing dependencies...
python -m pip install -r requirements.txt
goto end

:doc
echo Building documentation...
call %DOCS_DIR%/make html
goto end

:whl
echo Building wheel...
python -m build
goto end

:all
echo Running all targets...
call %0 clean
call %0 pylint
call %0 doc
call %0 whl
goto end

:clean
echo Cleaning build directories...
rmdir /s /q %BUILD_DIR%
rmdir /s /q %DIST_DIR%
del /s /q *.egg-info
call %DOCS_DIR%/make clean
goto end

:pylint
echo Running pylint...
pylint ssd testapp my_logger --output=pylint_report.txt
goto end

:end
echo Done.
