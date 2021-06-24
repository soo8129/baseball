import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_condition as EC


# team name to team id
def _get_team_id(team_name='NO'):
    if team_name == 'KIA':
        return 'HT'
    elif team_name == '키움':
        return 'WO'
    elif team_name == '한화':
        return 'HH'
    elif team_name == 'KT':
        return 'KT'
    elif team_name == 'SK':
        return 'SK'
    elif team_name == '삼성':
        return 'SS'
    elif team_name == '두산':
        return 'OB'
    elif team_name == '롯데':
        return 'LT'
    elif team_name == 'NC':
        return 'NC'
    elif team_name == 'LG':
        return 'LG'
    else:
        return team_name


# delete previous today_lineup
def _delete_pre_lineup():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM today_lineup;")
    conn.commit()
    conn.close()


# save in today_lineup
def _save_lineup(team_id, players_list):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "INSERT INTO today_lineup (team_name, first, second, third, fourth, fifth, sixth, seventh, eighth, ninth) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, (team_id, players_list[0], players_list[1], players_list[2],
                         players_list[3], players_list[4], players_list[5],
                         players_list[6], players_list[7], players_list[8]))
    conn.commit()
    conn.close()


# save in today_match
def _save_match(game_list):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "INSERT INTO today_games (date, time, game_id, stadium, away_id, home_id, away_pitcher_id, home_pitcher_id) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    for game in game_list:
        cursor.execute(sql, game)
    conn.commit()
    conn.close()


# today's match up
def _today_match():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    URL = 'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx'
    driver.get(URL)
    driver.implicitly_wait(3)

    # page's current date
    cur_date = driver.find_element_by_xpath('//*[@id="lblGameDate"]')
    cur_date = cur_date.text[:-3].replace('.', '-')

    # today's game list
    today_game_ul = driver.find_element_by_xpath('//*[@id="contents"]/div[3]/div/div[1]/ul')
    today_game_list = today_game_ul.find_elements_by_tag_name('li')
    today_games = []
    for game in today_game_list:
        tmp_list = [cur_date, '18:30', '', '', '', '', '', '']
        tmp_list[2] = game.get_attribute('g_id') + game.get_attribute('season')
        tmp_list[3] = game.get_attribute('s_nm')
        tmp_list[4] = game.get_attribute('away_id')
        tmp_list[5] = game.get_attribute('home_id')
        tmp_list[6] = game.get_attribute('away_p_id')
        tmp_list[7] = game.get_attribute('home_p_id')
        today_games.append(tmp_list)

    _save_match(today_games)

    # today's lineup
    _delete_pre_lineup()
    for game in today_game_list:
        game.click()
        try:
            WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '


# get from db
def get_today_match():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM today_games;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    games_list = []
    for row in rows:
        game_list = [row['date'], row['time'], row['game_id'], row['stadium'],
                     row['away_id'], row['home_id'], row['away_pitcher_id'], row['home_pitcher_id']]
        games_list.append(game_list)

    return games_list


def main():
    _today_match()


if __name__ == '__main__':
    main()
