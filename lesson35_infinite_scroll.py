import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(60000)

        print("Website သို့ သွားနေပါသည်...")
        await page.goto("https://quotes.toscrape.com/scroll", wait_until="domcontentloaded")

        for i in range(3):
            print(f"Scroll ခေါက်ကြိမ်: {i+1} - အောက်သို့ ဆွဲချနေပါသည်...")

            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            await page.wait_for_timeout(2000)

        quotes = await page.locator(".quote .text").all_text_contents()

        print(f"\nScroll လုပ်ပြီးနောက် စုစုပေါင်း ရရှိသော Quote အရေအတွက်: {len(quotes)}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())            