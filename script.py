from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta


def select_date(page, year, month, day):
    page.click('#race-nav-datepicker')
    page.select_option('.pika-select-year', str(year))
    page.select_option('.pika-select-month', str(month - 1))
    page.click(f'button.pika-button[data-pika-day="{day}"][data-pika-year="{year}"][data-pika-month="{month - 1}"]')

    page.wait_for_selector('div.race-nav__meetings')
    child_devs = page.locator('.meetings .reveal')
    page.wait_for_timeout(30000)
    
    
    
def generate_dates(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    delta = end - start
    date_list = [(start + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]
    return date_list


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://www.attheraces.com/home', timeout=60000)

    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    date_list = generate_dates(start_date, end_date)

    for date in date_list:
        year, month, day = map(int, date.split('-'))
        print(f"Selecting date: {date}")
        select_date(page, year, month, day)
        page.wait_for_timeout(1000)  # Consider reducing or replacing this with wait_for_selector

    page.wait_for_timeout(3000)  
    browser.close()
