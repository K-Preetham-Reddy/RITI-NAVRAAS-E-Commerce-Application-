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

@app.route('/checkout',methods=['POST'])
def checkout():
    cart_data=request.json
    conn=get_db_connection()
    cur=conn.cursor()
    
    product_ids=tuple(cart_data.keys())
    cur.execute(f"SELECT id, title, cost FROM products WHERE id IN {product_ids};")
    products=cur.fetchall()

    total=0
    checkout_items=[]
    for p in products:
        qty=cart_data[str(p[0])]
        total_cost=p[2]*qty
        total+=total_cost
        checkout_items.append({"id":p[0],"title":p[1],"quantity":qty,"total": total_cost})
    cur.close()
    conn.close()
    return jsonify({"items":checkout_items,"total":total})

