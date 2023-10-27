import requests
from bs4 import BeautifulSoup


#전달받은 url의 html 소스를 모두 가져와서
#그 중 링크들을 모두 가져온 후 마지막 페이지 return
def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
  last_page = len(pages)
  return int(last_page)


def extract_job(html):
  title = html.find("h2", {"class":"mb4 fc-black-800 fs-body3"}).find("a")["title"]

  company, location = html.find("h3", {"class":"fc-black-700 fs-body1 mb4"}).find_all("span", recursive=False)
  company = company.get_text(strip=True).strip("\n")
  location = location.get_text(strip=True).strip("\n")
  job_id = html.find("h2", {"class":"mb4 fc-black-800 fs-body3"}).find_all("a")
  job_id = str(job_id)
  job_id = job_id[46:52]

  return {
    'title': title,
    'company': company,
    'location': location,
    "apply_link": f"https://stackoverflow.com/jobs/{job_id}/"
    }



def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping: page: {page}")
    result = requests.get(f"{url}{page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"grid--cell fl1"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs
    

def get_jobs(word):
  url =f"https://stackoverflow.com/jobs?c=KRW&d=20&q={word}&u=Km&pg="
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs


def get_product_status(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  btns = soup.find("button", {"id":"ordButtn"})
  return btns