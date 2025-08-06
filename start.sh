#!/bin/bash
# Script de inicialização para o Render
cd /opt/render/project/src
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port $PORT