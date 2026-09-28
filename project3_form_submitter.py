import asyncio
import csv
import os
from playwright.async_api import async_playwright

async def main():
    print("Script စတင် အလုပ်လုပ်နေပါပြီ...")
    
    # input_data.csv ဖိုင် ရှိမရှိ စစ်ဆေးခြင်း
    if not os.path.exists("input_data.csv"):
        print("\n--> Error: 'input_data.csv' ဖိုင်ကို ရှာမတွေ့ပါ။ Folder အပြင်ဘက်မှာ ရှိမရှိ စစ်ပေးပါဗျာ။")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(60000)
        
        users = []
        with open("input_data.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)
                
        print(f"CSV ဖိုင်မှ စုစုပေါင်း လူဦးရေ {len(users)} ယောက်၏ Data ကို ဖတ်ယူပြီးပါပြီ။\n")
        
        await page.goto("https://quotes.toscrape.com/login", wait_until="domcontentloaded")
        
        success_count = 0
        for user in users:
            print(f"Form ဖြည့်နေပါသည်: Name={user['Name']}")
            
            await page.fill("#username", user["Name"])
            await page.fill("#password", user["Message"])
            await page.wait_for_timeout(1000)
            
            await page.click("input[type='submit']")
            await page.wait_for_load_state("domcontentloaded")
            
            success_count += 1
            await page.goto("https://quotes.toscrape.com/login", wait_until="domcontentloaded")
            
        print(f"\n--> လုပ်ဆောင်ချက် အားလုံး ပြီးစီးပါပြီ။ စုစုပေါင်း Form {success_count} ခု အောင်မြင်စွာ တင်ပြီးပါပြီ!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())