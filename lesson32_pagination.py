import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # လိုင်းမကောင်းပါက ခေတ္တစောင့်ရန် Timeout ပြင်ဆင်ခြင်း
        page.set_default_timeout(60000)
        
        print("Website သို့ ချိတ်ဆက်နေပါသည်...")
        await page.goto("https://quotes.toscrape.com/", wait_until="domcontentloaded")
        
        page_num = 1
        while True:
            print(f"\n=== Page {page_num} ===")
            
            # Data များ ဆွဲထုတ်ခြင်း
            quotes = await page.locator(".quote .text").all_text_contents()
            authors = await page.locator(".quote .author").all_text_contents()
            
            for i in range(len(quotes)):
                print(f"{i+1}. {quotes[i]} - {authors[i]}")
            
            # Next Button ကို စစ်ဆေး၍ နှိပ်ခြင်း
            next_button = page.locator("li.next a")
            if await next_button.count() > 0:
                print("--> Next page သို့ သွားနေပါသည်။")
                await next_button.click()
                await page.wait_for_load_state("domcontentloaded")
                page_num += 1
            else:
                print("\n--> နောက်ဆုံး မျက်နှာသို့ ရောက်ရှိသွားပါပြီ။")
                break
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())