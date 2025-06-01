# XML to HTML Product Data Scraper
## Overview
This script extracts product data (e.g., name, price, price per unit) from an XML sitemap containing URLs of product pages. It saves the HTML content of these pages and compiles the extracted product details into a CSV file.

## Features
- Parses XML files to extract product page URLs.
- Uses Playwright to fetch and save HTML content from URLs.
- Extracts product name, total price, and price per unit using BeautifulSoup.
- Saves the scraped data to a CSV file.

## Requirements
Python Libraries
The script requires the following Python libraries:
- `os`
- `glob`
- `xml.etree.ElementTree`
- `playwright`
- `csv`
- `time`
- `random`
- `bs4` (BeautifulSoup)

Install the necessary libraries using:
`pip install playwright beautifulsoup4`

Run script with:
python spider4.py

## Playwright Setup
Before running the script, install the Playwright browsers:
`playwright install`

## Setup
1. Clone or download this repository.
2. Update the paths in the script:
- xml_folder: Path to the folder containing XML sitemap files.
- html_folder: Path to the folder where HTML files will be saved.
- output_csv: Path for the output CSV file.
3. Place the XML sitemap files in the specified folder.

## Usage
1. Run the script:
`python spider4.py`

2. The script will:

- Extract URLs from XML files.
- Save the HTML content of product pages to the specified folder.
- Extract product details and save them in the CSV file.
- The CSV file will include the following columns:

* URL
* Product Name
* Product Price
* Product Unit

## Notes
- Ensure the target website allows web scraping and complies with its terms of service.
- Adjust delays (e.g., time.sleep) to avoid overloading the server.
- The script uses random user-agent strings to simulate real browser traffic.

## Error Handling
Errors during HTML saving or data extraction are logged to the console but do not stop the script.
If a URL fails, the error is logged, and the script continues with the next URL.

## Example Folder Structure
project/
script_name.py              # The Python script
fd_xmls/                    # Folder containing XML sitemap files
saved_htmls/                # Folder where HTML files will be saved
product_data_with_units_test.csv   # Output CSV file

## Limitations
- The script assumes a specific HTML structure for extracting product details (e.g., data-testid attributes). Modify the extract_product_details_from_html function if the website structure changes.
- Only .xml files in the specified folder are processed.
- Saving all of the HTMLs takes a lot of space, can add code to delete HTML after information extracted to csv.
- FD servers block after a few iterations. Try implementing rotating proxies. 
