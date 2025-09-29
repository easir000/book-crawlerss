import asyncio
import httpx
from selectolax.parser import HTMLParser
from urllib.parse import urljoin
from crawler.scraper import crawl_category
from crawler.storage import db
from crawler.config import BASE_URL
from crawler.state import load_last_category, save_last_category

async def main():
    await db.connect()
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Fetch homepage to get categories
        resp = await client.get("")
        tree = HTMLParser(resp.text)
        category_links = tree.css(".side_categories a")[1:]  # Skip "Books"
        full_category_urls = [
            urljoin(BASE_URL, link.attributes["href"])
            for link in category_links
        ]

        # Load last successfully crawled category
        last_done = load_last_category()
        if last_done and last_done in full_category_urls:
            start_idx = full_category_urls.index(last_done) + 1
            if start_idx >= len(full_category_urls):
                print("✅ All categories already crawled. Starting fresh crawl.")
                category_urls_to_crawl = full_category_urls
                # Optional: reset state to allow re-crawl
                save_last_category("")
            else:
                category_urls_to_crawl = full_category_urls[start_idx:]
                print(f"✅ Resuming from category {start_idx + 1}/{len(full_category_urls)}")
        else:
            category_urls_to_crawl = full_category_urls

        print(f"🌐 Found {len(category_urls_to_crawl)} categories to crawl.")

        # Crawl with progress tracking
        async def crawl_and_track(url):
            await crawl_category(client, url)
            save_last_category(url)

        if category_urls_to_crawl:
            await asyncio.gather(*[crawl_and_track(url) for url in category_urls_to_crawl])
        else:
            print("ℹ️  No categories to crawl.")

    await db.close()
    print("✅ Full crawl completed successfully.")
    # Optional: uncomment to reset state after every full run
    # save_last_category("")

if __name__ == "__main__":
    asyncio.run(main())