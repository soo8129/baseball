from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime


# date to day
def get_day(cur_year=2020, cur_month=1, cur_date=33):
    print(cur_year, cur_month, cur_date)
    day_str = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    return day_str[datetime.date(cur_year, cur_month, cur_date).weekday()]


# stadium english to korean
def stadium_name(name='MH'):
    if name == 'MH':
        return '인천문학'
    elif name == 'JS':
        return '잠실'
    elif name == 'SJ':
        return '부산사직'
    elif name == 'DK':
        return '라이온즈파크'
    elif name == 'KC':
        return '챔피언스필드'
    elif name == 'CW':
        return '창원NC파크'
    elif name == 'SW':
        return '케이티위즈파크'
    elif name == 'GC':
        return '고척돔'
    elif name == 'DJ':
        return '대전한밭'
    else:
        return '천연잔디'


# get stadium/opponent tab contents
def get_relative_variables(name='서건창', opponent_team='KIA', home_or_away='홈경기', stadium='MH'):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = 'C:/Users/soo81/webcrawling/chromedriver.exe'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    URL = 'http://www.statiz.co.kr/player.php?name='+name+'&search='
    driver.get(URL)
    driver.implicitly_wait(3)
    relative_list = [0.0, 0.0, 0.0]
    tmp_list = []

    driver.find_element_by_xpath(
        '/html/body/div[1]/div[1]/div/section[2]/div/div[1]/div/div[3]/div/div[2]/table/tbody/tr/td/a[5]'
    ).click()
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div/section[2]/div/div[2]/div/div[2]/div'))
        )
    except EC as e:
        print(e)
    tmp_tab = driver.find_element_by_xpath('/html/body/div/div[1]/div/section[2]/div/div[2]/div/div[2]/div/a[2]')
    driver.execute_script('arguments[0].click();', tmp_tab)
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div/section[2]/div/div[2]/div/div[3]/'
                                                      'div/div/table/tbody/tr[24]/td[26]'))
        )
    except EC as e:
        print(e)
    tmp_table = driver.find_element_by_xpath('/html/body/div/div[1]/div/section[2]/div/div[2]/div/div[3]/div/div/table')
    even_rows = tmp_table.find_elements_by_class_name('evenrow_stz0')
    odd_rows = tmp_table.find_elements_by_class_name('oddrow_stz0')
    for even in even_rows:
        tmp_element = even.find_elements_by_tag_name('td')
        tmp_list.append([tmp_element[0].text, tmp_element[19].text])
    for odd in odd_rows:
        tmp_element = odd.find_elements_by_tag_name('td')
        tmp_list.append([tmp_element[0].text, tmp_element[19].text])
    for i in tmp_list:
        if i[0] == home_or_away:
            relative_list[0] = float(i[1])
        elif i[0] == 'vs '+opponent_team:
            relative_list[1] = float(i[1])
        elif i[0] == stadium_name(stadium):
            relative_list[2] = float(i[1])
        else:
            continue

    return relative_list


# get date/time tab contents
def get_time_variables(name='서건창', date='20200728'):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = 'C:/Users/soo81/webcrawling/chromedriver.exe'
    driver = webdriver.Chrome(executable_path='usr/local/bin/chromedriver', chrome_options=options)
    URL = 'http://www.statiz.co.kr/main.php'
    driver.get(URL)
    driver.implicitly_wait(3)

    # search player_name and click
    driver.find_element_by_xpath('//*[@id="search_text"]').send_keys(name)
    driver.find_element_by_xpath('//*[@id="search-btn"]').click()
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/section[2]/div/div[1]/'
                                                      'div/div[3]/div/div[2]/table/tbody/tr/td/a[5]'))
        )
    except EC as e:
        print(e)

    # click '상황별'
    driver.find_element_by_xpath(
        '/html/body/div[1]/div[1]/div/section[2]/div/div[1]/div/div[3]/div/div[2]/table/tbody/tr/td/a[5]').click()
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/section[2]/div/div[2]/'
                                                      'div/div[3]/div/div/table/tbody/tr[26]/td[26]'))
        )
    except EC as e:
        print(e)

    # date/time tab table contents
    table_div = driver.find_element_by_xpath('/html/body/div/div[1]/div/section[2]/div/div[2]/div/div[3]/div')
    table_even_rows = table_div.find_elements_by_class_name('evenrow_stz0')
    table_odd_rows = table_div.find_elements_by_class_name('oddrow_stz0')
    tmp_list = []
    for even in table_even_rows:
        tmp_list.append([even.find_elements_by_tag_name('td')[0].text, even.find_elements_by_tag_name('td')[19].text])
    for odd in table_odd_rows:
        tmp_list.append([odd.find_elements_by_tag_name('td')[0].text, odd.find_elements_by_tag_name('td')[19].text])
    day = get_day(int(date[:4]), int(date[4:6]), int(date[6:]))
    con_var = [0.0, 0.0, 0.0, 0.0]
    for i in tmp_list:
        if i[0] == '최근7일':
            con_var[0] = float(i[1])
        elif i[0] == '최근30일':
            con_var[1] = float(i[1])
        elif i[0] == day:
            con_var[2] = float(i[1])
        elif i[0] == '밤(16시이후)':
            con_var[3] = float(i[1])
        else:
            continue

    driver.quit()
    return con_var


# time + relative var return
def get_condition_variables(name='서건창', date='20200728', opponent_team='KIA', home_or_away='홈경기', stadium='MH'):
    condition_variables_list = get_time_variables(name, date) + \
                               get_relative_variables(name, opponent_team, home_or_away, stadium)
    return condition_variables_list


# for test
# print(get_condition_variables())
