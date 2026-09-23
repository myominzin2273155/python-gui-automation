import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Chromium Browser ကို ပွင့်လာအောင် မောင်းနှင်ခြင်း
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # စမ်းသပ်မည့် Website သို့ သွားခြင်း
        await page.goto("https://quotes.toscrape.com/")
        print("Page Title:", await page.title())
        
        # ၅ စက္ကန့် စောင့်ပြီး Browser ကို ပိတ်ခြင်း
        await page.wait_for_timeout(5000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())