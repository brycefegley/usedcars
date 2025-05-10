from scraper import fetch_rendered_html, parse_inventory_listing 
from bs4 import BeautifulSoup
import pandas as pd

def build_autotrader_url(zip_code, radius_miles, page_num=1):
    base_url = "https://www.autotrader.com/cars-for-sale/all-cars/toyota/4runner"
    return f"{base_url}?zip={zip_code}&searchRadius={radius_miles}&page={page_num}"

def main():
    url = build_autotrader_url(zip_code="98225", radius_miles=200)
    html = fetch_rendered_html(url)
    print(html[:1000])

    listings = [parse_listing_card(str(card)) for card in cards]
    df = pd.DataFrame(listings)
    df.to_csv("data/raw_listings.csv", index=False)

if __name__ == "__main__":
    main()

