from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session, g
import sqlite3
from datetime import datetime
import pytz
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from werkzeug.security import generate_password_hash, check_password_hash
import functools
from typing import Dict

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')  # Must be set in .env
app.config['JSON_AS_ASCII'] = False  # Add this for proper encoding

DB_PATH = Path(os.environ.get('DB_PATH', 'mantenimiento.db'))

# Configure Gemini (add your API key in environment variables)
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

# Translation dictionaries
CATEGORY_TRANSLATIONS: Dict[str, str] = {
    'Aceite': 'Oil',
    'Frenos': 'Brakes',
    'Motor': 'Engine',
    'Transmisión': 'Transmission',
    'Suspensión': 'Suspension',
    'Dirección': 'Steering',
    'Eléctrico': 'Electrical',
    'Llantas': 'Tires',
    'Carrocería': 'Body',
    'Otros': 'Others'
}