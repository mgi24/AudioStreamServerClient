@echo off
REM Activate the Python environment and run server.py

REM Set the path to the Python executable
set PYTHON_EXE=C:\Users\Workload13\Documents\pythonenv\yolo\Scripts\python.exe

REM Run server.py using the specified Python environment
"%PYTHON_EXE%" serverudp.py