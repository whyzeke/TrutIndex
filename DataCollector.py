import requests
from bs4 import BeautifulSoup
import sqlite3

def setup_database():
    conn = sqlite3.connect("headers.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS headers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn  
    
def extract_data(soup, conn):
    h3_tags = soup.find_all('h3') 
    cursor = conn.cursor()
    for tag in h3_tags:
        header_text = tag.get_text(strip=True)
        print(header_text)
        cursor.execute("INSERT INTO headers (text) VALUES (?)", (header_text,))
    conn.commit()
        
    conn.commit()
        
def parse_html(response, conn):
    soup = BeautifulSoup(response.content, 'html.parser')
    extract_data(soup, conn)
     
def get_page(url, conn):
    response = requests.get(url)
    if response.status_code == 200:
        return parse_html(response, conn)
    else:
        return None
               
if __name__ == "__main__":
    conn = setup_database()
    get_page("https://theonion.com/latest/", conn)
    conn.close()

    
    

