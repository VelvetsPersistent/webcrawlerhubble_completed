import os
import requests
from bs4 import BeautifulSoup
import csv
import sys
import mysql.connector
from urllib.parse import urljoin

# Function to get all URLs from a given base URL


def get_all_urls(base_url):
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data - {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all anchor tags (links) on the page
    links = soup.find_all('a')

    # Extract the URLs and titles from the links
    urls_titles = [(urljoin(base_url, link.get('href')),
                    link.get_text()) for link in links]

    # Filter out None and empty URLs
    urls_titles = [(url, title)
                   for url, title in urls_titles if url and not url.startswith('#')]

    return urls_titles

# Function to save crawled data to CSV file


def save_to_csv(urls_titles):
    data_folder = 'datas'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    csv_filepath = os.path.join(data_folder, 'webpages.csv')
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Title'])
        writer.writerows(urls_titles)

    print(f"\nData saved to '{csv_filepath}' inside the 'datas' folder.")

# Function to save crawled data to MySQL database


def save_to_database(urls_titles):
    try:
        connection = mysql.connector.connect(
            host="your_mysql_host",
            user="your_mysql_user",
            password="your_mysql_password",
            database="your_mysql_database"
        )
        cursor = connection.cursor()

        # Create the 'webpages' table if it doesn't exist
        create_table_query = """CREATE TABLE IF NOT EXISTS webpages (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                url VARCHAR(500) NOT NULL,
                                title VARCHAR(500) NOT NULL
                            )"""
        cursor.execute(create_table_query)

        # Insert data into the 'webpages' table
        insert_query = "INSERT INTO webpages (url, title) VALUES (%s, %s)"
        cursor.executemany(insert_query, urls_titles)
        connection.commit()

        print("\nData saved to MySQL database.")
    except mysql.connector.Error as e:
        print(f"Error saving data to MySQL database - {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the URL of the website to crawl as a command-line argument.")
        sys.exit(1)

    website_url = sys.argv[1]
    urls_titles = get_all_urls(website_url)

    if urls_titles:
        print("\nWebpages in the website:")
        for i, (url, title) in enumerate(urls_titles, 1):
            print(f"{i}. URL: {url}")
            print(f"Title: {title.encode('utf-8').decode('cp1252')}\n")

        # Save crawled data to CSV file
        save_to_csv(urls_titles)

        # Save crawled data to MySQL database
        save_to_database(urls_titles)

        # Call index.py to index the data using Whoosh
        # os.system("python index.py")
    else:
        print("No webpages found on the website.")
