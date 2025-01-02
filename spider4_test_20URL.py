import os
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
import csv
import time
import random
from bs4 import BeautifulSoup

# Define the folder containing XML files and the folder to save HTML files
html_folder = "/Users/hannahthompson/Documents/FreshDirect3/saved_htmls"  # Folder where HTML files will be saved
output_csv = "product_data_with_units_test.csv"
user_agent_strings = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko"
]

# Create the folder to save HTML files if it doesn't exist
os.makedirs(html_folder, exist_ok=True)

# Function to extract product details from saved HTML file
def extract_product_details_from_html(html_file):
    try:
        with open(html_file, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            
            # Extract Product Name
            product_name = soup.find("h1", {"data-testid": "product-name"})
            product_name = product_name.get_text(strip=True) if product_name else "N/A"
            
            # Extract Total Price
            product_price_total = soup.find("b", {"data-testid": "add-to-cart-total-price"})
            product_price_total = product_price_total.get_text(strip=True) if product_price_total else "N/A"
            
            # Extract Price per Unit
            product_price_per_unit = soup.find("span", {"data-testid": "Tile unit price"})
            product_price_per_unit = product_price_per_unit.get_text(strip=True) if product_price_per_unit else "N/A"
            
            return product_name, product_price_total, product_price_per_unit
    except Exception as e:
        print(f"Error reading HTML file {html_file}: {e}")
        return "Error fetching product name", "Error fetching total price", "Error fetching unit price"

# Function to save HTML file for each URL
def save_html_for_url(page, url, file_name):
    try:
        # Save the HTML content to a file in the designated folder
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(page.content())
        print(f"Saved HTML for {url} to {file_name}")
    except Exception as e:
        print(f"Error saving HTML for {url}: {e}")

# Function to extract URLs from XML
def extract_urls_from_xml(xml_file, limit=20):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Assuming URLs are in an <url> tag, adjust as needed based on XML structure
        urls = []
        for url_element in root.findall(".//url"):  # Adjust the XPath if necessary
            url = url_element.text.strip()
            urls.append(url)

        return urls[:limit]  # Return the first 'limit' URLs
    except Exception as e:
        print(f"Error reading XML file {xml_file}: {e}")
        return []

# Open CSV file for writing
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["URL", "Product Name", "Product Price", "Product Unit"])  # Add the unit column

    # Define the path to your XML file
    xml_file_path = "/Users/hannahthompson/Documents/FreshDirect3/fd_xmls/sitemap_product_meat_seafood.xml"  # Adjust to your actual XML file path
    urls = extract_urls_from_xml(xml_file_path)  # Get the first 20 URLs from the XML file

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use headless=False for visible browser
        context = browser.new_context(
            user_agent=random.choice(user_agent_strings),
            extra_http_headers={"Upgrade-Insecure-Requests": "1"},
            ignore_https_errors=True,
            incognito=True
        )
        page = context.new_page()

        for url in urls:
            print(f"Fetching URL: {url}")
            try:
                # Navigate to the page
                page.goto(url, wait_until="load")
                time.sleep(3)  # Wait a bit to ensure page loads completely
                print(f"Page loaded: {url}")  # Verify the page is loading
                
                # Save the HTML content for later
                html_file_name = os.path.join(html_folder, f"{url.split('/')[-1]}.html")  # Save using the last part of the URL as the filename
                save_html_for_url(page, url, html_file_name)

                # Extract product details from the saved HTML
                product_name, product_price, product_unit = extract_product_details_from_html(html_file_name)

                # Write data to CSV
                csvwriter.writerow([url, product_name, product_price, product_unit])

                # Add a small delay to avoid overloading the server
                time.sleep(random.uniform(3, 7))  # Adjust delay as needed

            except Exception as e:
                print(f"Error fetching {url}: {e}")

        browser.close()

print(f"Data extraction complete. Results saved to {output_csv}")
