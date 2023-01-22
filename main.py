import requests
from bs4 import BeautifulSoup
from flask import Flask, request

app = Flask(__name__, static_url_path='/static')


def headlines_get(search_term="ChatGPT", pages=20):
  all_headlines = []
  url = "https://news.ycombinator.com/"
  for i in range(1, pages + 1):
    page_url = f"{url}?p={i}"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('span', class_="titleline")
    for headline in headlines:
      head = headline.text.strip()
      link = headline.find('a')['href']
      if "item?id" in link:
        link = f"{url}{link}"
      if f"{search_term}" in head:
        all_headlines.append((head, link))
  return all_headlines


@app.route("/", methods=['GET'])
def index():
  pages = request.args.get("pages")
  search_term = request.args.get("search")
  if pages != None and search_term != None:
    pages = int(pages)
    headlines = headlines_get(search_term, pages)
  else:
    headlines = headlines_get()
    search_term = "ChatGPT"
  page = ""
  res = ""
  links = ""
  with open("index.html", "r") as f:
    page = f.read()
  with open("links.html", "r") as f:
    links = f.read()
  for headline, link in headlines:
    l = links
    l = l.replace("{headline}", headline)
    l = l.replace("{link}", link)
    res += l
  page = page.replace("{search_term}", search_term)
  page = page.replace("{content}", res)
  return page


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
