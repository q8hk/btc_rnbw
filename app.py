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

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all bold elements on the page
        # bold_elements = soup.find_all(['b', 'strong'])
        active_span = soup.find('span', class_=lambda x: x and 'active' in x)


        # Extract and concatenate the text from bold elements
        bold_text = ' '.join([element.get_text() for element in active_span])
        active_text = active_span.get_text()

        # Read the previously stored data from a file
        previous_data = read_previous_data()

        # Compare the current bold words with the previous data
        if active_text != previous_data:
            # Send the bold words as a message to the Telegram bot
            bot.send_message(chat_id,bold_text)

            # Update the stored data with the current bold words
            write_current_data(bold_text)
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