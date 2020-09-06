from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file


app = Flask("JobScrapper")

db = {}
#진짜 db가 아니라 그저 서버메모리에 있음 
#그래서 재시작하면 다시 불러와야함


@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  #사용자가 적은값 가져오기
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template(
    "report.html",
    searchingBy = word, 
    resultNumber=len(jobs),
    jobs=jobs
  )
  #report.html에 각각의 값을 넘겨준다. render
  
@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv", as_attachment=True)
  except:
    return redirect("/")  
  #try를 시도하다가 에러가나면 except실행 



app.run(host="0.0.0.0")