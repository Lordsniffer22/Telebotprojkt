#!/bin/bash
pip install pytube aiogram==3.5 python_dotenv
wget -O pyt.py https://raw.githubusercontent.com/Lordsniffer22/Telebotprojkt/main/pyt.py
touch .env
echo "API_TOKEN= 7139989240:AAEtHvE6aNfY2Nsjh7ufl-vtxJroGVLFoUo" > .env
python3 pyt.py
