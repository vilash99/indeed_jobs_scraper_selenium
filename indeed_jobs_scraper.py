import time
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException,
                                        ElementNotInteractableException)

OP_CSV = "scraped_data_indeed.csv"


def save_in_csv(data):
    with open(OP_CSV, 'a', newline='') as fileobj:
        writer = csv.writer(fileobj)
        writer.writerow(data)


def scrape_job_posting(driver):
    """
    Scrape all jobs list in given page
    """
    jobs = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")

    for job in jobs:
        get_job_detail(job)


def get_job_detail(job):
    """
    Scrape single job with fields:
    job title, company, location, date posted and url
    """
    try:
        url = job.find_element(
            By.CSS_SELECTOR, 'a.jcs-JobTitle'
        ).get_attribute('href')
    except NoSuchElementException:
        url = ''

    try:
        title = job.find_element(
            By.CSS_SELECTOR, "a.jcs-JobTitle"
        ).get_attribute("innerText")
    except NoSuchElementException:
        title = ''

    try:
        company = job.find_element(
            By.CSS_SELECTOR, 'span[data-testid="company-name"]'
        ).get_attribute("innerText")
    except NoSuchElementException:
        company = ''

    try:
        location = job.find_element(
            By.CSS_SELECTOR, 'div[data-testid="text-location"]'
        ).get_attribute("innerText")
    except NoSuchElementException:
        location = ''

    try:
        posted = job.find_element(
            By.CSS_SELECTOR, 'table span.date'
        ).get_attribute("innerText")
        posted = posted.split('\n')[1]
    except:
        posted = ''

    save_in_csv([title, company, location, posted, url])


if __name__ == "__main__":
    chrome_option = Options()
    chrome_option.add_experimental_option('useAutomationExtension', False)
    chrome_option.add_experimental_option(
        'excludeSwitches', ['enable-automation']
    )
    chrome_option.add_argument('--ignore-certificate-errors')
    chrome_option.add_argument('--test-type')

    driver = webdriver.Chrome(
        service=Service('chromedriver.exe'),
        options=chrome_option
    )

    while True:
        scrape_job_posting(driver)

        # Check if there is next page
        try:
            next_button = driver.find_element(
                By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]'
            )
        except NoSuchElementException:
            # No more job available
            print('All jobs are scrapped successfully, exiting script.')
            break

        # Click on next page button
        try:
            next_button.click()
            time.sleep(2)
        except ElementNotInteractableException:
            print('Unable to click on next button, exiting script.')
            break

    driver.close()
    driver.quit()
