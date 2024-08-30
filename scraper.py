import requests
from bs4 import BeautifulSoup
import time

def scrape_bbc_transfers():
    # Define the URL of the BBC Sport football transfers page
    url = 'https://www.bbc.co.uk/sport/football/transfers'

    try:
        # Send a GET request to the page with a timeout
        response = requests.get(url, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the page content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all the transfer news articles using the class names from your snippet
            articles = soup.find_all('a', class_='ssrcss-zmz0hi-PromoLink')

            new_updates = []

            for article in articles:
                title = article.find('p', class_='ssrcss-1b1mki6-PromoHeadline').get_text(strip=True)
                link = f"https://www.bbc.co.uk{article['href']}"  # Create the full link

                # Only add the article if it hasn't been seen before
                if title not in seen_titles:
                    new_updates.append((title, link))
                    seen_titles.add(title)

            # If there are new updates, print them
            if new_updates:
                print("BBC Sport Football Transfers News:")
                for title, link in new_updates:
                    print(f"Update: {title}\nLink: {link}\n")
            else:
                print("No new updates.")

        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}. Retrying in 10 seconds...")
        time.sleep(10)
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}. Retrying in 10 seconds...")
        time.sleep(10)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}. Exiting.")
        return

# Set to store seen titles
seen_titles = set()

while True:
    scrape_bbc_transfers()
    print("Waiting for 30 seconds before refreshing..")
    time.sleep(30)  # Wait for 30 seconds before refreshing