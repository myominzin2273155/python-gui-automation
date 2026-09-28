import asyncio
import csv
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(60000)

        print("Quotes (Multi-page) Website သို့ သွားနေပါသည်...")
        await page.goto("https://quotes.toscrape.com/", wait_until="domcontentloaded")

        with open("quotes_all_pages.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Quote", "Author", "Tags"])

            page_num = 1

            while True:
                print(f"\n--- စာမျက်နှာ ({page_num}) ကို Scraping လုပ်နေပါသည် ---")
                await page.wait_for_selector(".quote")

                quotes = await page.locator(".quote").all()
                for q in quotes:
                    text = await q.locator(".text").text_content()
                    author = await q.locator(".author").text_content()

                    tags_list = await q.locator(".tag").all_text_contents()
                    tags = ", ".join(tags_list)

                    writer.writerow([text, author, tags])

                print(f"Page {page_num} မှ Quote အရေအတွက် {len(quotes)} ခု သိမ်းဆည်းပြီးပါပြီ။")

                next_button = page.locator("li.next a")
                if await next_button.count() > 0:
                    page_num += 1
                    await next_button.click()
                    await page.wait_for_load_state("domcontentloaded")
                else:
                    print("n\--> နောက်ဆုံး စာမျက်နှာသို့ ရောက်ရှိသွားပါပြီ။")
                    break
        print("\n--> quotes_all_pages.csv ဖိုင်ထဲသို့ Data အားလုံး အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ !")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())                    