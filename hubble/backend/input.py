# def get_website_url():
# Replace the URL below with the website you want to crawl
# return "http://books.toscrape.com/"
# return "https://college.vac.edu.np/"
# return "https://quotes.toscrape.com/"

# import os


# def get_user_input():
#     website_url = input("Enter the URL of the website to crawl: ")
#     search_query = input("Enter search query: ")

#     # Call crawl.py and search.py with the user input
#     os.system(f"python crawl.py {website_url}")
#     os.system(f"python search.py {search_query}")


# if __name__ == "__main__":
#     get_user_input()


# import os
# import sys
# import getopt


# def get_user_input():
#     search_url = None
#     search_query = None

#     try:
#         opts, args = getopt.getopt(
#             sys.argv[1:], "", ["search_url=", "search_query="])
#     except getopt.GetoptError:
#         print("Usage: input.py --search_url <url> --search_query <query>")
#         sys.exit(1)

#     for opt, arg in opts:
#         if opt == "--search_url":
#             search_url = arg
#         elif opt == "--search_query":
#             search_query = arg

#     if not search_url or not search_query:
#         print("Please provide both the search URL and search query.")
#         sys.exit(1)

#     # Your remaining code to process the input goes here
#     # Call crawl.py and search.py with the user input
#     os.system(f"python crawl.py {search_url}")
#     os.system(f"python search.py {search_query}")


# if __name__ == "__main__":
#     get_user_input()


import os
import sys
import getopt


def crawl_and_search(search_url, search_query):
    # Call crawl.py with the search URL
    os.system(f"python crawl.py {search_url}")

    # Call search.py with the search query
    os.system(f"python search.py {search_query}")


def main(argv):
    search_url = ""
    search_query = ""

    try:
        opts, args = getopt.getopt(
            argv, "u:q:", ["search_url=", "search_query="])
    except getopt.GetoptError:
        print("input.py -u <search_url> -q <search_query>")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-u", "--search_url"):
            search_url = arg
        elif opt in ("-q", "--search_query"):
            search_query = arg

    if not search_url or not search_query:
        print("Please provide the search URL and search query.")
        print("input.py -u <search_url> -q <search_query>")
        sys.exit(2)

    crawl_and_search(search_url, search_query)


if __name__ == "__main__":
    main(sys.argv[1:])
