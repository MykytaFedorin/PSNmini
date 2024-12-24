#!/bin/bash
python app.py &&
uvicorn controller:app --host 0.0.0.0 --port 9000
#fastapi run controller.py

