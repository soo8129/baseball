from selenium import webdriver


def get_lineup_vars(game_id='20200802HTLT02020', home_away='away', player_id='69652'):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = 'C:/Users/soo81/webcrawling/chromedriver.exe'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    URL = 'https://sports.news.naver.com/gameCenter/gameRecord.nhn?gameId='+game_id+'&category=kbo'
    driver.get(URL)
    driver.implicitly_wait(3)
    tables = driver.find_elements_by_tag_name('table')

    if home_away == '홈경기':
        hitters_table = tables[3]
    else:
        hitters_table = tables[2]

    player_order = 0
    player_ba = 0.0
    tmp_idx = 0
    lineup_prob_list = []
    trs = hitters_table.find_elements_by_tag_name('tr')[2:]
    for idx, tr in enumerate(trs):
        tr_list = tr.text.split()
        if tr_list[0] != '교':
            tmp_idx += 1
            tmp_link = tr.find_element_by_tag_name('a').get_attribute('href')
            if tmp_link[tmp_link.find('playerId=')+9:] != player_id:
                lineup_prob_list.append(float(tr_list[-1]))
            else:
                player_order = tmp_idx
                player_ba = float(tr_list[-1])
        else:
            tmp_link = tr.find_element_by_tag_name('a').get_attribute('href')
            if tmp_link[tmp_link.find('playerId=')+9:] == player_id:
                lineup_prob_list = lineup_prob_list[:-1]
                player_order = tmp_idx
                player_ba = float(tr_list[-1])

    lineup_prob_list.append(player_ba)
    lineup_prob_list.append(player_order)

    driver.close()

    return lineup_prob_list
