# scheduler/tasks.py
import asyncio
import httpx
from selectolax.parser import HTMLParser
from urllib.parse import urljoin
from crawler.config import BASE_URL
from crawler.parser import parse_book_page
from scheduler.change_detector import detect_and_log_changes
from scheduler.reports import generate_daily_report
from crawler.storage import db


async def crawl_book_with_change_detection(client: httpx.AsyncClient, url: str):
    """Fetch and parse a single book page, then run change detection."""
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        html = response.text
        book_data = parse_book_page(url, html)
        await detect_and_log_changes(book_data)
    except Exception as e:
        print(f"❌ Failed to process {url}: {e}")


async def crawl_category_for_changes(client: httpx.AsyncClient, category_url: str):
    """Crawl all books in a category and apply change detection."""
    page = 1
    while True:
        url = category_url if page == 1 else category_url.replace("index.html", f"page-{page}.html")
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                break
            raise

        tree = HTMLParser(response.text)
        book_links = tree.css("article.product_pod h3 a")
        if not book_links:
            break

        book_urls = []
        for link in book_links:
            href = link.attributes.get("href")
            if href:
                clean_href = href.replace("../", "")
                full_url = urljoin("https://books.toscrape.com/catalogue/", clean_href)
                book_urls.append(full_url)
        await asyncio.gather(*[crawl_book_with_change_detection(client, u) for u in book_urls])
        page += 1


async def run_full_crawl_and_detect_changes():
    """Main entry point for daily crawl + change detection."""
    print("🔍 Starting full crawl and change detection...")
    await db.connect()

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Get categories
        resp = await client.get("")
        tree = HTMLParser(resp.text)
        category_links = tree.css(".side_categories a")[1:]
        category_urls = [
            urljoin(BASE_URL, link.attributes["href"]) for link in category_links
        ]

        print(f"📚 Processing {len(category_urls)} categories...")
        for i, cat_url in enumerate(category_urls, 1):
            print(f"  {i}/{len(category_urls)}: {cat_url}")
            await crawl_category_for_changes(client, cat_url)

    await generate_daily_report()
    await db.close()
    print("✅ Daily crawl and change detection completed.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_full_crawl_and_detect_changes())