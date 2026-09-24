import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(60000)

        print("Website သို့ သွားနေပါသည်...")
        await page.goto("https://quotes.toscrape.com/scroll", wait_until="domcontentloaded")
        print("Data များ ပေါ်လာသည်အထိ စောင့်ဆိုင်းနေပါသည်...")
        await page.wait_for_selector(".quote")

        quotes = await page.locator(".quote .text").all_text_contents()

        print(f"\nတွေ့ရှိသော Quote အရေအတွက်: {len(quotes)}")
        for q in quotes[:3]:
            print("_", q)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())          