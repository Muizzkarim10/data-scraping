from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta


def select_date(page, year, month, day):
    page.click('//a[@href="#sidebar-racecards"]')

    # Wait for the date picker to become visible
    page.wait_for_selector('#sidebar-racecards-datepicker', state='attached')
    page.click('#sidebar-racecards-datepicker')
    
    page.select_option('.pika-select-year', str(year))
    page.select_option('.pika-select-month', str(month - 1))
    page.click(f'button.pika-button[data-pika-day="{day}"][data-pika-year="{year}"][data-pika-month="{month - 1}"]')

    # Wait until the meetings container is fully loaded
    page.wait_for_selector('.padded--x-small')
    
    # Locate parent and child elements
    child = page.locator('.padded--x-small .meetings .meetings-group')

    # Count the number of child elements
    count = child.count()
    print(f'Number of meetings: {count}')

    # Print the values of all child elements
    for i in range(count):
        meeting_value = child.nth(i).locator('.meetings_group')
        meeting_value.click()
        
        # page.wait_for_selector('//*[@id="tab-race-nav--uk"]/div/div/div[1]/div/div[1]/div/div/ul/li[1]/a').click()


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
