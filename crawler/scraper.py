import httpx
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from urllib.parse import urljoin
from selectolax.parser import HTMLParser
from crawler.parser import parse_book_page
from crawler.storage import db
from crawler.config import CRAWL_CONCURRENCY

semaphore = asyncio.Semaphore(CRAWL_CONCURRENCY)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError))
)
async def fetch_page(client: httpx.AsyncClient, url: str) -> str:
    response = await client.get(url, timeout=10.0)
    response.raise_for_status()
    return response.text

# crawler/scraper.py
async def crawl_book(client: httpx.AsyncClient, url: str):
    async with semaphore:
        try:
            html = await fetch_page(client, url)
            book_dict = parse_book_page(url, html)
            # Save directly to collection
            await db.books.replace_one(
                {"url": book_dict["url"]},
                book_dict,
                upsert=True
            )
            print(f"✅ Saved: {book_dict['title']}")
        except Exception as e:
            print(f"❌ Failed to crawl {url}: {e}")

async def crawl_category(client: httpx.AsyncClient, category_url: str):
    page = 1
    while True:
        if page == 1:
            url = category_url
        else:
            url = category_url.replace("index.html", f"page-{page}.html")
        
        try:
            html = await fetch_page(client, url)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                break
            raise

        tree = HTMLParser(html)
        book_links = tree.css("article.product_pod h3 a")
        if not book_links:
            break

        full_urls = [
            urljoin("https://books.toscrape.com/catalogue/", 
                    link.attributes["href"].replace("../", ""))
            for link in book_links
        ]
        await asyncio.gather(*[crawl_book(client, u) for u in full_urls])
        page += 1