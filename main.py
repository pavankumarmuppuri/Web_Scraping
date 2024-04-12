import pandas as pd
from bs4 import BeautifulSoup
import requests

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

books_names = []
ratings_list = []
prices = []
links_list = []

for page_num in range(1, 51):  # Assuming there are 50 pages
    url = base_url.format(page_num)
    response = requests.get(url)
    html = response.text
    data = BeautifulSoup(html, 'html.parser')

    titles = data.find_all('a', title=True)
    for title in titles:
        books_names.append(title['title'])

    p_tags = data.find_all('p', class_='star-rating')
    for p in p_tags:
        rating = p['class'][1]
        ratings_list.append(rating)

    price_tags = data.find_all('p', class_='price_color')
    for tag in price_tags:
        price = tag.get_text(strip=True)
        prices.append(price[1:])

    links = data.find_all('h3')
    for link in links:
        href = link.a.get('href')
        links_list.append("https://books.toscrape.com/catalogue/" + href)

df = pd.DataFrame({
    'Book Title': books_names,
    'Rating': ratings_list,
    'Price': prices,
    'Link': links_list
})

print(df)
#df.describe()

#df.to_excel('books_data.xlsx', index=False)

#from google.colab import files

#files.download('books_data.xlsx')

