from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import sqlite3

# connecting to database
connection = sqlite3.connect('yummy_data.db')
cursor = connection.cursor()

# changing user-agent
user_agent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={user_agent.chrome}')

# disable webdriver mode
options.add_argument('--disable-blink-features=AutomationControlled')

# enable headless mode
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path=r'some path to selenium web driver', options=options)


try:
    for page_number in range(1, 49):

        time.sleep(2)

        driver.get(url=f'https://yummyanime.club/filter?status=-1&season=0&from_year=&to_year=&from_num_episodes=&to_num_episodes=&selected_age=0&sort=3&sort_order=0&page={page_number}')
        urls_list = [url.get_attribute('href') for url in driver.find_elements(By.CLASS_NAME, 'image-block')]
        types = [anime_type.text.split('\n')[1] for anime_type in driver.find_elements(By.CLASS_NAME, 'anime-column-info')]

        print(f'Page: {page_number}')

        driver.implicitly_wait(5)

        for current_url, anime_type in zip(urls_list, types):
            driver.get(current_url)
            name = driver.find_element(By.XPATH, '//*[@id="main-page"]/div[2]/div[3]/div/div/h1').text
            rating = driver.find_element(By.CLASS_NAME, 'main-rating').text
            status = driver.find_element(By.CLASS_NAME, 'badge').text
            year = driver.find_element(By.XPATH, '//*[@id="main-page"]/div[2]/div[3]/div/div/ul[2]/li[3]').text.split()[1]
            categories_list = ', '.join([category.text for category in driver.find_elements(By.CLASS_NAME, 'categories-list')][0].split('\n')[1:])
            description = driver.find_element(By.ID, 'content-desc-text').text
            img_poster = driver.find_element(By.CLASS_NAME, 'poster-block').find_element(By.TAG_NAME, 'img').get_attribute("src")

            driver.implicitly_wait(10)

            cursor.execute('INSERT INTO yummybot VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           [name, rating, status, year, categories_list, anime_type, description, current_url, img_poster]

            connection.commit()

            # # break
        # break

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


connection.close()
