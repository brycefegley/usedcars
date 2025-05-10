# parse_results.py

import os
from bs4 import BeautifulSoup
import pandas as pd
from scraper import parse_inventory_listing

urls = [f"atp{i}.html" for i in range(1, 4)]
all_data = []

for u in urls:
    file_path = os.path.join('data', u)
    print(f"Parsing {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    cards = soup.select("div.item-card-body > div.inventory-listing-body")
    print(f"Found {len(cards)} cards")

    all_data.extend(parse_inventory_listing(card) for card in cards)

# Convert and export
df = pd.DataFrame(all_data)
df.to_csv("data/autotrader_scraped_results.csv", index=False)
print("✅ Parsed data written to data/autotrader_scraped_results.csv")
