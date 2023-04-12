# Twitter Mutual Followers Scraper

This Python script uses the Tweepy library to scrape mutual followers for a given Twitter user. The script writes the data to a CSV file and logs information about the scraping process to a text file.

## Installation

1. Install Tweepy by running `pip install tweepy`.
2. Create a Twitter API account and generate access keys.
3. Replace the placeholders for API keys in the code with your own keys.
4. Run the script using `python mutual_followers.py`.

## Usage

1. Enter the Twitter username of the user for whom you want to scrape mutual followers.
2. The script will start scraping and display a countdown until the next rate limit window.
3. The script will write the mutual followers' data to a CSV file named `mutual_followers.csv`.
4. The script will write information about the scraping process to a text file named `logs.txt`.
5. The script will display the elapsed time at the end of the scraping process.

## License

This project is licensed under the MIT License.

## ChatGPT

This Code was generated with ChatGPT using iterations of this prompt:

'''
Give me a SaaS platform to download twitter mutuals as CSV.
'''
