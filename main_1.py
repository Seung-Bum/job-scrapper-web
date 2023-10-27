from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file


app = Flask("ProductStatus")

db = {}
#진짜 db가 아니라 그저 서버메모리에 있음 
#그래서 재시작하면 다시 불러와야함

@app.route("/")
def home():
  return render_template("home_1.html")


app.run(host="0.0.0.0")