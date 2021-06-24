from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql

teams_enroll_name = ['NONE',
                     'NC 다이노즈 선수등록명단',
                     '키움 히어로즈 선수등록명단',
                     '두산 베어스 선수등록명단',
                     'LG 트윈스 선수등록명단',
                     'KIA 타이거즈 선수등록명단',
                     'KT 위즈 선수등록명단',
                     '삼성 라이온즈 선수등록명단',
                     '롯데 자이언츠 선수등록명단',
                     'SK 와이번스 선수등록명단',
                     '한화 이글스 선수등록명단']

cur_teams = ['NONE', 'NC', 'WO', 'OB', 'LG', 'HT', 'KT', 'SS', 'LT', 'SK', 'HH']


def _teams_list_make():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = 'usr/local/bin/chromedriver'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    URL = 'https://www.koreabaseball.com/Player/Register.aspx'
    driver.get(URL)
    driver.implicitly_wait(3)

    teams_list_div = driver.find_element_by_xpath('//*[@id="cphContents_cphContents_cphContents_udpRecord"]/div[1]')
    teams_list = teams_list_div.find_elements_by_tag_name('li')
    idx = 1
    for team in teams_list:
        if team.text == 'NC':
            cur_teams[idx] = 'NC'
            teams_enroll_name[idx] = 'NC 다이노즈 선수등록명단'
        elif team.text == '키움':
            cur_teams[idx] = 'WO'
            teams_enroll_name[idx] = '키움 히어로즈 선수등록명단'
        elif team.text == '두산':
            cur_teams[idx] = 'OB'
            teams_enroll_name[idx] = '두산 베어스 선수등록명단'
        elif team.text == 'LG':
            cur_teams[idx] = 'LG'
            teams_enroll_name[idx] = 'LG 트윈스 선수등록명단'
        elif team.text == 'KIA':
            cur_teams[idx] = 'HT'
            teams_enroll_name[idx] = 'KIA 타이거즈 선수등록명단'
        elif team.text == 'KT':
            cur_teams[idx] = 'KT'
            teams_enroll_name[idx] = 'KT 위즈 선수등록명단'
        elif team.text == '롯데':
            cur_teams[idx] = 'LT'
            teams_enroll_name[idx] = '롯데 자이언츠 선수등록명단'
        elif team.text == '삼성':
            cur_teams[idx] = 'SS'
            teams_enroll_name[idx] = '삼성 라이온즈 선수등록명단'
        elif team.text == 'SK':
            cur_teams[idx] = 'SK'
            teams_enroll_name[idx] = 'SK 와이번스 선수등록명단'
        elif team.text == '한화':
            cur_teams[idx] = 'HH'
            teams_enroll_name[idx] = '한화 이글스 선수등록명단'
        else:
            cur_teams[idx] = 'NO'
            teams_enroll_name[idx] = 'NONE'
        idx += 1

    driver.close()


# add players info in db
def _add_players(players_list, cur_team='TEAM_ERROR'):
    try:
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='chldlstns1!',
                             charset='utf8',
                             db='baseball')
    except Exception as e:
        print(e, 'db_error')
        return

    cursor = db.cursor()

    for player in players_list:
        sql = "UPDATE players set is_enroll = true, team_name=%s where player_id = %s;"
        cursor.execute(sql, (cur_team, player[0]))
        db.commit()

        sql = "INSERT INTO players (player_id, player_name, birthday, team_name, is_enroll)" \
              "VALUES (%s, %s, %s, %s, true) ON DUPLICATE KEY UPDATE is_enroll = true;"
        cursor.execute(sql, (player[0], player[1], player[2], cur_team))
        db.commit()

    db.close()


# [NONE, NC, WO, OB, HT, LG, KT, SS, LT, SK, HH]
def _team_players_info(team=1):

    print('current team: '+cur_teams[team])
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = 'C:/Users/soo81/webcrawling/chromedriver.exe'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
    URL = 'https://www.koreabaseball.com/Player/Register.aspx'
    driver.get(URL)
    driver.implicitly_wait(3)

    driver.find_element_by_xpath(
        '//*[@id="cphContents_cphContents_cphContents_udpRecord"]/div[1]/ul/li['+str(team)+']/a').click()
    driver.implicitly_wait(3)
    try:
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element_value((By.XPATH,
                                                    '//*[@id="cphContents_cphContents_cphContents_udpRecord"]/div[3]/h4'),
                                                   teams_enroll_name[team])
        )
    except Exception as e:
        print(e, 'team click loading...')

    tot_table = driver.find_element_by_xpath('//*[@id="cphContents_cphContents_cphContents_udpRecord"]/div[3]')
    tables = tot_table.find_elements_by_tag_name('table')[3:]
    catchers = tables[0].find_elements_by_tag_name('tr')[1:]
    infielders = tables[1].find_elements_by_tag_name('tr')[1:]
    outfielders = tables[2].find_elements_by_tag_name('tr')[1:]
    players_trs = catchers+infielders+outfielders
    players_list = []
    for row in players_trs:
        tds = row.find_elements_by_tag_name('td')
        player_id = row.find_element_by_tag_name('a').get_attribute('href')[-5:]
        players_list.append([player_id, tds[1].text, tds[3].text])

    for p in players_list:
        print(p)
    _add_players(players_list, cur_teams[team])

    driver.quit()


def get_players_info():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='chldlstns1!',
                         charset='utf8',
                         db='baseball')
    cursor = db.cursor()
    sql = "UPDATE players set is_enroll = false"
    cursor.execute(sql)
    db.commit()
    db.close()
    for i in range(1, 11):
        _team_players_info(i)
    print('ALL DONE!')


_teams_list_make()
print(teams_enroll_name)
print(cur_teams)
get_players_info()
