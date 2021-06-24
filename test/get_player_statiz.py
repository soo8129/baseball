from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# get player url for statiz searching
def get_player_statiz(kbo_url=''):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = 'C:/Users/soo81/webcrawling/chromedriver.exe'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)

    driver.get(kbo_url)
    driver.implicitly_wait(3)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cphContents_cphContents_cphContents_playerProfile_lblBirthday"]'))
        )
    except EC as e:
        print(e)
    tot_birthday = driver.find_element_by_xpath('//*[@id="cphContents_cphContents_cphContents_playerProfile_lblBirthday"]').text
    year = tot_birthday[:4]
    month = tot_birthday[6:8]
    date = tot_birthday[10:12]
    driver.quit()
    return year+'-'+month+'-'+date
