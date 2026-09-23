import asyncio
import csv
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(60000)
        
        print("Data များကို စတင် ဆွဲထုတ်နေပါသည်...")
        await page.goto("https://quotes.toscrape.com/", wait_until="domcontentloaded")
        
        # CSV ဖိုင်ဖွင့်၍ Header ရေးသားခြင်း
        with open("quotes.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Quote", "Author"])  # Header Column
            
            page_num = 1
            while True:
                quotes = await page.locator(".quote .text").all_text_contents()
                authors = await page.locator(".quote .author").all_text_contents()
                
                # ရရှိလာသော Data များကို CSV ဖိုင်ထဲသို့ တစ်ကြောင်းချင်း သိမ်းခြင်း
                for i in range(len(quotes)):
                    writer.writerow([quotes[i], authors[i]])
                
                print(f"Page {page_num} သိမ်းဆည်းပြီးပါပြီ။")
                
                next_button = page.locator("li.next a")
                if await next_button.count() > 0:
                    await next_button.click()
                    await page.wait_for_load_state("domcontentloaded")
                    page_num += 1
                else:
                    break
                    
        print("\n--> quotes.csv ဖိုင်ထဲသို့ Data အားလုံး အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ။")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())