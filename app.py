from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)

DB_HOST=os.getenv("DB_HOST")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASS=os.getenv("DB_PASS")
def get_db_connection():
    return psycopg2.connect(host=DB_HOST,dbname=DB_NAME,user=DB_USER,password=DB_PASS)

@app.route('/')
def index():
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute("SELECT * FROM products;")
    products=cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html',products=products)

