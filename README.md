
# Flight Price Scraper

This project is a Python-based web scraper that collects flight price data from Google Flights for various European destinations. The scraper is designed to gather the 5 cheapest flights between London and a set of predefined cities in Europe between January 2025 and May 2025. It emails the results every 48 hours.

## Features

- Scrapes flight prices for 27 different European cities.
- Navigates Google Flights calendar to find the 5 cheapest flights for each destination.
- Sends results via email automatically every 48 hours.
- Configured to scrape prices for trips starting from January 2025.

## Requirements

To run this project, you will need:

- Python 3.x
- `smtplib` (for sending emails)
- `selenium` (for web scraping)
- A configured Gmail account to send the emails

### Libraries
- `smtplib` (comes with Python)
- `email.mime` (comes with Python)
- `selenium`
- `datetime`
- `time`

### Installation

1. Install Selenium:

```bash
pip install selenium
```

2. Download and install [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) to enable Selenium to interact with Chrome.
3. Ensure ChromeDriver is set up and the path to it is specified in the script.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/flight-price-scraper.git
cd flight-price-scraper
```

2. Edit the `send_email()` function in the Python script to add your Gmail credentials.

```python
from_email = "your-email@gmail.com"
password = "your-gmail-password"
```

3. Set the `initial_message_id` if you want to send replies instead of new emails.
   
4. Adjust the `driver_path` in the script to point to where your ChromeDriver is installed.

## Running the Script

To run the script, execute:

```bash
python refactoredscraper.py
```

The scraper will navigate through Google Flights, collect flight prices, and email the results to the specified address.

## Automating with Cron (Mac/Linux)

To run the script automatically every 48 hours, you can set up a cron job:

1. Open the crontab editor:

```bash
crontab -e
```

2. Add the following line to schedule the script to run every 48 hours:

```bash
0 */48 * * * /usr/bin/python3 /path/to/refactoredscraper.py
```

3. Save the file.

## Sample Output

```plaintext
Destination: Berlin, Germany
Date: Monday, January 6, 2025, Price: $64
Date: Monday, January 13, 2025, Price: $64
Date: Monday, February 3, 2025, Price: $64
Date: Monday, March 6, 2025, Price: $64
```

## License

This project is open-source and available under the MIT License.
