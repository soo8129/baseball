from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from get_player_statiz import get_player_statiz
import pymysql


def _url_maker(game_id='20200728WOOB02020'):
    tot_url = 'https://sports.news.naver.com/gameCenter/gameRecord.nhn?'
    tot_url = tot_url + 'gameId=' + game_id + '&category=kbo'
    return tot_url


def _pof_id(game_id='20200728WOOB02020'):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = 'C:/Users/soo81/webcrawling/chromedriver.exe'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    URL = _url_maker(game_id)
    driver.get(URL)
    driver.implicitly_wait(3)

    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "UPDATE players SET ba=%s WHERE player_id=%s;"

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="result_area"]/div/table[2]'))
        )
    except EC as e:
        print(e)
    away_team = driver.find_element_by_xpath('//*[@id="result_area"]/div/table[2]')
    tmp_table = away_team.find_elements_by_tag_name('tr')
    tmp_table = tmp_table[2:]

    home_team = driver.find_element_by_xpath('//*[@id="result_area"]/div/table[3]')
    tmp2_table = home_team.find_elements_by_tag_name('tr')
    tmp2_table = tmp2_table[2:]

    tmp_table += tmp2_table
    pof_list = []

    for i in tmp_table:
        tmp_list = i.text.split()

        tmp_link = i.find_element_by_tag_name('a').get_attribute('href')
        tmp_idx = tmp_link.find('playerId=')
        tmp_id = tmp_link[tmp_idx+9:]
        cursor.execute(sql, (tmp_list[-1], tmp_id))

        if int(tmp_list[-5]) > 0 and int(tmp_list[-4]) == 0:

            # tmp_birthday is temporal function before get player_id to information
            tmp_birthday = get_player_statiz(tmp_link)
            pof_list.append([tmp_id, False])
            print('Fail ' + tmp_list[1] + tmp_id + ' ' + tmp_birthday)
        elif int(tmp_list[-5]) > 0 and int(tmp_list[-4]) > 0:

            # tmp_birthday is temporal function before get player_id to information
            tmp_birthday = get_player_statiz(tmp_link)
            pof_list.append([tmp_id, True])
            print('Pass ' + tmp_list[1] + tmp_id + ' ' + tmp_birthday)
        else:
            continue

    driver.quit()
    conn.close()

    return pof_list


def info(game_id='20200728WOOB02020'):
    return _pof_id(game_id)
