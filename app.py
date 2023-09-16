import requests
from bs4 import BeautifulSoup
import telebot
import os
import time

# Replace with your Telegram bot API token
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = int(os.environ.get("TELEGRAM_CHAT_ID"))

if not bot_token:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set.")

bot = telebot.TeleBot(bot_token)

# Function to scrape the website and find bold words
def scrape():
    url = 'https://www.blockchaincenter.net/en/bitcoin-rainbow-chart/'

    def make_request_with_retry(url, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"Request failed ({retries+1}/{max_retries}): {e}")
                retries += 1
                time.sleep(5)  # Wait for a few seconds before retrying
        print("Max retries reached. Request failed.")
        return None

    try:
        response_text = make_request_with_retry(url)
        if response_text is None:
            return

        soup = BeautifulSoup(response_text, 'html.parser')

        active_span = soup.find('span', class_=lambda x: x and 'active' in x)

        active_text = active_span.get_text()

        previous_data = read_previous_data()

        if active_text != previous_data:
            bot.send_message(chat_id, active_text)
            write_current_data(active_text)
    except Exception as e:
        print("Error:", e)
        bot.send_message(chat_id, "Error while scraping the website.")

# Function to read the previously stored data from a file
def read_previous_data():
    previous_data = ""
    if os.path.isfile("word.txt"):
        with open("word.txt", "r") as file:
            previous_data = file.read()
    return previous_data

# Function to write the current data to a file
def write_current_data(data):
    with open("word.txt", "w") as file:
        file.write(data)

# Run the scraping function once a day
if __name__ == "__main__":
    while True:
        scrape()
        # Sleep for 24 hours (86400 seconds) before checking again
        time.sleep(86400)
