from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import timezone
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)

   
def get_book_author(book_title):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    
    search_url = f"https://www.goodreads.com/search?utf8=%E2%9C%93&q={requests.utils.quote(book_title)}&search_type=books"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    first_result = soup.find('tr', {'itemtype': 'http://schema.org/Book'})
    if not first_result:
        return "Book not found"
    
    author_tags = first_result.find_all('a', {'class': 'authorName'})
    authors = []

    if author_tags:
        for author in author_tags:
            name = author.find('span', {"itemprop": "name"}).get_text()
            authors.append(name.strip())  # Add each author's name to the list

        return authors

    else:
        return "Author not found"

@app.route('/get-author-name', methods=['POST'])
def get_cover_image():
    book_data = request.get_json()
    book_title = book_data.get('name')
    if book_data:
        if 'author' in book_data:
            return jsonify({"author": book_data['author']})
    
    author = get_book_author(book_title)

    if author == "Book not found" or author == "Author not found":
        response = requests.post(f"{os.getenv('LLM_MS_URI')}/author", json={
            "title": book_title
        })
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({"author": "Anonymous"})
    
    
    return jsonify({"author": author})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)), debug=os.getenv('DEBUG', 'False') == 'True')
