import os
import csv
import sys
import mysql.connector

# Function to fetch data from MySQL database


def fetch_data_from_mysql():
    try:
        connection = mysql.connector.connect(
            host="your_mysql_host",
            user="your_mysql_user",
            password="your_mysql_password",
            database="your_mysql_database"
        )
        cursor = connection.cursor()

        select_query = "SELECT url, title FROM indexed_webpages"
        cursor.execute(select_query)

        data = [(url, title) for url, title in cursor]

        cursor.close()
        connection.close()

        return data

    except mysql.connector.Error as e:
        print(f"Error fetching data from MySQL database - {e}")
        return None


# Function to load crawled data from CSV file
def load_data_from_csv():
    data_folder = 'datas'
    csv_filepath = os.path.join(data_folder, 'webpages.csv')
    with open(csv_filepath, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        return [(row[0], row[1]) for row in reader]

# Function to save search results to CSV file


def save_search_results_to_csv(search_results):
    data_folder = 'datas'
    csv_filepath = os.path.join(data_folder, 'search_results.csv')

    with open(csv_filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Title'])
        writer.writerows(search_results)


# Function to perform a search query on the index
def search_webpages(search_query):
    data = fetch_data_from_mysql()

    if data is None:  # If data not available in MySQL, fallback to webpages.csv
        data = load_data_from_csv()

    if not data:
        print("No data found. Please run 'crawl.py' first to generate the data.")
        return

    processed_query = search_query.lower()

    found_results = []
    for url, title in data:
        if processed_query in title.lower():
            found_results.append((url, title))

    if found_results:
        # Sort the results based on the count of matched words in descending order
        ranked_results = sorted(found_results, key=lambda x: x[1].lower().count(
            processed_query), reverse=True)

        print("\nSearch Results:")
        for i, (url, title) in enumerate(ranked_results, 1):
            count_matched_words = title.lower().count(processed_query)
            print(f"{i}. URL: {url}")
            print(f"   Title: {title}")
            # print(f"   Matched Words: {count_matched_words}\n")

        # Save the search results to a CSV file
        save_search_results_to_csv(ranked_results)
        print("Search results saved to 'search_results.csv'")

    else:
        print("No matching results found.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the search query as a command-line argument.")
        sys.exit(1)

    search_query = sys.argv[1]
    search_webpages(search_query)
