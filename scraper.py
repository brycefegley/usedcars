# scraper.py
from bs4 import BeautifulSoup

def parse_title(title):
    parts = title.split()
    certified = "Certified" if parts[0] == "Certified" else None
    year = int(parts[1]) if certified else int(parts[0])
    make = parts[2] if certified else parts[1]
    model = parts[3] if certified else parts[2]
    trim = " ".join(parts[4:]) if certified else " ".join(parts[3:])
    return year, make, model, trim

def parse_inventory_listing(div):
    try:
        title_text = div.find("h2", attrs={"data-cmp": "subheading"}).get_text(strip=True)
        year, make, model, trim = parse_title(title_text)
    except:
        title_text, year, make, model, trim = None, None, None, None, None

    try:
        mileage = div.find("div", attrs={"data-cmp": "mileageSpecification"}).get_text(strip=True)
    except:
        mileage = None

    try:
        price = div.find("div", attrs={"data-cmp": "firstPrice"}).get_text(strip=True)
    except:
        price = None

    try:
        relative_url = div.find("a", attrs={"data-cmp": "link"})["href"]
        url = f"https://www.autotrader.com{relative_url}"
    except:
        url = None

    try:
        sponsor_tag = div.find_previous("div", class_="text-subdued", string=lambda t: t and "Sponsored by" in t)
        is_sponsored = sponsor_tag is not None
        sponsor_name = sponsor_tag.get_text(strip=True).replace("Sponsored by ", "") if is_sponsored else None
    except:
        is_sponsored = False
        sponsor_name = None

    return {
        "title": title_text,
        "year": year,
        "make": make,
        "model": model,
        "trim": trim,
        "certified": title_text.startswith("Certified") if title_text else False,
        "mileage": mileage,
        "price": price,
        "url": url,
        "is_sponsored": is_sponsored,
        "sponsor_name": sponsor_name
    }

