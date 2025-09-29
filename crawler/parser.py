from selectolax.parser import HTMLParser
from app.models.book import Book
from datetime import datetime
import re


def parse_book_page(url: str, html: str) -> dict:
    tree = HTMLParser(html)

    # === Title (required) ===
    title_el = tree.css_first("h1")
    title = title_el.text().strip() if title_el else "Unknown Title"

    # === Category (required) ===
    breadcrumbs = tree.css("ul.breadcrumb li")
    category = breadcrumbs[-2].text().strip() if len(breadcrumbs) >= 2 else "Unknown"

    # === Price (required) ===
    price_el = tree.css_first("p.price_color")
    price_text = price_el.text().replace("£", "") if price_el else "0.0"
    price = float(price_text) if price_text.replace(".", "").isdigit() else 0.0

    # === Availability (required) ===
    avail_el = tree.css_first(".availability")
    avail_raw = avail_el.text(strip=True) if avail_el else "Not available"
    count_match = re.search(r"\((\d+) available\)", avail_raw)
    count = int(count_match.group(1)) if count_match else 0

    # === Number of Reviews (required) ===
    review_el = tree.css_first("table.table tr:nth-child(7) td")
    num_reviews = int(review_el.text()) if review_el and review_el.text().isdigit() else 0

    # === Image URL (required) ===
    img_el = tree.css_first("#product_gallery img")
    img_src = img_el.attributes.get("src") if img_el and img_el.attributes else ""
    image_url = "https://books.toscrape.com/" + img_src.replace("../", "") if img_src else ""

    # === Rating (required) ===
    rating_el = tree.css_first("p.star-rating")
    rating_class = rating_el.attributes.get("class", "") if rating_el else ""
    rating_word = rating_class.split()[-1] if rating_class else "Zero"
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating = rating_map.get(rating_word, 0)

    # === Description (optional) ===
    desc_el = tree.css_first("#product_description ~ p")
    description = desc_el.text().strip() if desc_el else None

    # === Build Book Model ===
    book = Book(
        url=url,
        title=title,
        description=description,
        category=category,
        price_excl_tax=price,
        price_incl_tax=price,
        availability_raw=avail_raw,
        availability_count=count,
        num_reviews=num_reviews,
        image_url=image_url,
        rating=rating,
        raw_html=html,
        crawled_at=datetime.utcnow()
    )
    return book.model_dump()  # Returns dict for MongoDB