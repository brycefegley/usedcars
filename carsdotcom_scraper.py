# carsdotcom_scraper.py

import os
import sys
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from datetime import datetime, timezone

def fetch_cars_page(zip_code, page=1):
    url = (
        f"https://www.cars.com/shopping/results/?stock_type=used"
        f"&makes[]=toyota&models[]=toyota-4runner"
        f"&maximum_distance=250&zip={zip_code}&page={page}"
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page_obj = browser.new_page()
        page_obj.goto(url, timeout=60000)
        page_obj.wait_for_selector("div.vehicle-card", timeout=20000)
        html = page_obj.content()
        browser.close()
    return html

def parse_cars_page(html):
    soup = BeautifulSoup(html, "lxml")
    listings = []
    for card in soup.select("div.vehicle-card"):
        try:
            title = card.select_one("h2.title").get_text(strip=True)
            year = int(title.split()[0])
            price = card.select_one("span.primary-price").get_text(strip=True).replace("$", "").replace(",", "")
            mileage = card.select_one("div.mileage").get_text(strip=True).replace(",", "").replace(" mi.", "")
            dealer = card.select_one("div.dealer-name").get_text(strip=True)
            link = "https://www.cars.com" + card.find("a", href=True)["href"]
            listings.append({
                "year": year,
                "title": title,
                "price": int(price),
                "mileage": int(mileage),
                "dealer": dealer,
                "url": link
            })
        except Exception:
            continue
    return listings

def scrape_multiple_pages(zip_code, max_pages=3):
    all_data = []
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        html = fetch_cars_page(zip_code, page)
        page_listings = parse_cars_page(html)
        all_data.extend(page_listings)
    return all_data

def main():
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).strftime("%Y%m%d")
    fn = os.path.join("data", f"{date}_carsdotcom_4runners.csv")
    if os.path.exists(fn):
        print(f"Data file for {date} already exists...skipping scrape.")
    else:
        data = scrape_multiple_pages("98225", max_pages=3)
        df = pd.DataFrame(data)
        df.to_csv(fn, index=False)

    return 0

if __name__ == "__main__":
    main()
