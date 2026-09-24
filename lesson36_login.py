import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(60000)

        print("Login Page သို့ သွားနေပါသည်...")
        await page.goto("https://quotes.toscrape.com/login", wait_until="domcontentloaded")

        print("Username နှင့် Password ရိုက်ထည့်နေပါသည်...")
        await page.fill("#username", "admin")

        await page.fill("#password", "password123")

        print("Login Button ကို နှိပ်နေပါသည်...")
        await page.click("input[type='submit']")

        await page.wait_for_load_state("domcontentloaded")

        logout_button = page.locator("a[href='/logout']")
        if await logout_button.count() > 0:
            print("\n--> Login အောင်မြင်စွာ ဝင်ရောက်ပြီးပါပြီ!")
        else:
            print("\n--> Login ဝင်ရောက်ခြင်း မအောင်မြင်ပါ။")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())                