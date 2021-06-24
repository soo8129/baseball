from selenium import webdriver


# 당일경기만, 아니면 None return
def get_var(stadium='JS'):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')

    path = 'C:/Users/soo81/webcrawling/chromedriver.exe'
    driver = webdriver.Chrome(path, options=options)
    URL = 'https://www.koreabaseball.com/Schedule/Weather.aspx'
    driver.get(URL)
    driver.implicitly_wait(3)
    env_list = []

    stadium_all_list = driver.find_element_by_xpath('//*[@id="ulStadiumList"]')
    stadium_lists = stadium_all_list.find_elements_by_tag_name('li')
    for s in stadium_lists:
        if s.get_attribute('data-stadium') == stadium:
            s.click()
            tmp_table = s.find_element_by_xpath('//*[@id="tblForecast"]')
            tmp_table_trs = tmp_table.find_elements_by_tag_name('tr')
            for i in tmp_table_trs:
                tmp_tr = i.text.split()[-1:]
                env_list.append(tmp_tr[0])

            return env_list
