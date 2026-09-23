import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto("https://quotes.toscrape.com/")
        
        # Website ပေါ်ရှိ Quote စာသားများကို ဆွဲထုတ်ခြင်း
        quotes = await page.locator(".quote .text").all_text_contents()
        authors = await page.locator(".quote .author").all_text_contents()
        
        print("\n--- Scraped Data ---")
        for i in range(len(quotes)):
            print(f"{i+1}. {quotes[i]} - {authors[i]}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())