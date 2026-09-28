import asyncio
import csv
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(60000)

        print("E-commerce (Books) Website သို့ သွားနေပါသည်...")
        await page.goto("https://books.toscrape.com/", wait_until="domcontentloaded")

        await page.wait_for_selector("article.product_pod")

        books = await page.locator("article.product_pod").all()
        print(f"တွေ့ရှိသော စာအုပ် အရေအတွက်: {len(books)} အုပ်\n")

        with open("book_prices.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Price", "Availability"])

            for book in books:
                title = await book.locator("h3 a").get_attribute("title")

                price = await book.locator(".price_color").text_content()

                availability = await book.locator(".availability").text_content()
                availability = availability.strip()

                writer.writerow([title, price, availability])
                print(f"Saved: {title[:20]}... | {price} | {availability}")

        print("\n--> book_prices.csv ဖိုင်ထဲသို့ Data များ အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ!")
        await browser.close()
if __name__ == "__main__":
    asyncio.run(main())        

