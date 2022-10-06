from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service
import pandas as pd
import lxml

driver_service = Service(
    executable_path='C:\\Users\\38971\\Documents\\scraping\\chromedriver.exe')
driver = webdriver.Chrome(service=driver_service)
driver.get('https://indeed.com/')

search = driver.find_element(By.XPATH, '//*[@id="text-input-what"]')
search.send_keys('Data Scientist')
search.send_keys(Keys.ENTER)

soup = BeautifulSoup(driver.page_source, 'lxml')

df = pd.DataFrame(
    {'Job_Title': [''], 'Company': [''], 'Raiting': [''], 'Location': [''], 'Salary': [''], 'Post_Date': [''],
     'Links': ['']})

link = []
for body in soup.find_all('tbody'):
    tr = body.find('tr')
    for links in tr.find_all('a', href=True):
        if links.find('a', href=True):
            link.append(links['href'])
postings = soup.find_all('div', class_='job_seen_beacon')

counter = 0
while counter < 5:
    for post in postings:
        link0 = post.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0').get('href')
        link = 'https://in.indeed.com' + link0
        job_title = post.find('h2', class_='jobTitle').text
        company = post.find('span', class_='companyName').text
        rating = post.find('a', class_='ratingLink')
        #rating = rating1['aria-label']
        location = post.find('div', class_='companyLocation').text
        disc = post.find('table', class_='jobCardShelfContainer big6_visualChanges')
        try:
            salary = post.find('span', class_='estimated-salary').text
        except:
            salary = 'N/A'
        post_date = post.find('span', class_='date').text
        df = df.append(
            {'Job_Title': job_title, 'Company': company, 'Raiting': rating, 'Location': location, 'Salary': salary,
             'Post_Date': post_date,
             'Links': link}, ignore_index=True)

    try:
        next_page = soup.find('a', attrs={'aria-label': 'Next'}).get('href')
        driver.get('https://in.indeed.com' + next_page)
    except:
        df.to_csv("C:\\Users\\38971\\Desktop\\web_scraper\\scraping\\jobs.csv", encoding='utf-8-sig')

    counter += 1

print('what')