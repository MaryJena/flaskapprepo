from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for scraping YouTube
@app.route('/scrape_youtube')
def scrape_youtube():
    youtube_url = "https://www.youtube.com/results?search_query=python+tutorial"
    response = requests.get(youtube_url)
    soup = BeautifulSoup(response.content, "html.parser")

    videos = []
    for video in soup.find_all('a', href=True, title=True):
        if '/watch?v=' in video['href']:
            videos.append({"title": video['title'], "link": "https://www.youtube.com" + video['href']})
    
    return render_template('youtube.html', videos=videos)

# Route for scraping Amazon
@app.route('/scrape_amazon')
def scrape_amazon():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    amazon_url = "https://www.amazon.com/s?k=laptops"
    response = requests.get(amazon_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    products = []
    for product in soup.find_all('span', class_="a-size-medium a-color-base a-text-normal"):
        products.append(product.get_text())

    return render_template('amazon.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)