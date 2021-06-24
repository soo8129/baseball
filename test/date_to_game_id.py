from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# korean to english stadium name
def stadium_name(std_name='문학'):
    if std_name == '문학':
        return 'MH'
    elif std_name == '잠실':
        return 'JS'
    elif std_name == '사직':
        return 'SJ'
    elif std_name == '대구':
        return 'DK'
    elif std_name == '광주':
        return 'KC'
    elif std_name == '창원':
        return 'CW'
    elif std_name == '수원':
        return 'SW'
    elif std_name == '고척':
        return 'GC'
    elif std_name == '대전':
        return 'DJ'
    elif std_name == '청주':
        return 'CJ'
    elif std_name == '포항':
        return 'PH'
    else:
        return 'NO'


# date to game_id and stadium_name
def get_game_id(year=2020, month=1, date=1):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = 'C:/Users/soo81/webcrawling/chromedriver.exe'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    URL = 'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx'
    driver.get(URL)
    driver.implicitly_wait(3)

    # month select
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/ul/li[2]/img').click()
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]'))
        )
    except EC as e:
        print(e)

    month_picker = Select(driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]'))
    month_picker.select_by_value(str(month-1))

    # year select
    year = str(year)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[2]'))
        )
    except EC as e:
        print(e)

    year_picker = Select(driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[2]'))
    year_picker.select_by_value(year)

    # date search and click
    date_picker = driver.find_elements_by_xpath('//a[@class="ui-state-default"]')
    for i in date_picker:
        if int(i.text) == date:
            i.click()
            break

    # whether game exist today or not
    selected_date = driver.find_element_by_xpath('//*[@id="lblGameDate"]').text
    today = year+'.'+str(month).zfill(2)+'.'+str(date).zfill(2)
    if selected_date[0:-3] != today:
        print(today + ' no game')
        driver.quit()
        return None
    else:
        # if games exists return games_id list
        today_games = driver.find_element_by_xpath('//*[@id="contents"]/div[3]/div/div[1]/ul')
        today_games_list = today_games.find_elements_by_class_name('list-review')
        today_games_id_list = []
        for i in today_games_list:
            today_games_id_list.append([i.get_attribute('g_id')+i.get_attribute('season'),
                                        stadium_name(i.get_attribute('s_nm'))])
        driver.quit()
        return today_games_id_list
