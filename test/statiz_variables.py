from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import pymysql
from statiz_info import stadium_name

URL = 'http://www.statiz.co.kr/player.php'


def _get_team_name(abbrev=None):
    if abbrev == 'OB':
        return '두산'
    elif abbrev == 'LT':
        return '롯데'
    elif abbrev == 'SS':
        return '삼성'
    elif abbrev == 'WO':
        return '키움'
    elif abbrev == 'HH':
        return '한화'
    elif abbrev == 'HT':
        return 'KIA'
    else:
        return abbrev


def _get_day(date_str='2020-07-28'):
    day_str = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    return day_str[datetime.strptime(date_str, '%Y-%m-%d').weekday()]


def _get_player_info(player_id=None):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "SELECT * FROM players WHERE player_id=%s;"
    cursor.execute(sql, player_id)
    conn.commit()
    row = cursor.fetchone()
    try:
        player_info = [row[1], row[2]]
    except TypeError:
        print(player_id)
        return None
    conn.close()
    return player_info


# 상황별 - 상대/구장 탭
def _oppo_var(name='터커', birth='1990-07-06', game_id='20200728LGSK02020', stadium='MH'):
    params = {'opt': '4', 'sopt': '0', 'name': name, 'birth': birth, 're': '0', 'da': '2', 'year': '2020'}
    response = requests.get(URL, params=params)
    html = response.text

    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "SELECT team_name FROM players WHERE (player_name=%s AND birthday=%s)"
    cursor.execute(sql, (name, birth))
    conn.commit()
    row = cursor.fetchone()
    team_name = row[0]

    conn.close()
    if game_id[8:10] == team_name:
        home_away = '원정경기'
        oppo_team = game_id[10:12]
    else:
        home_away = '홈경기'
        oppo_team = game_id[8:10]

    soup = bs(html, 'html.parser')
    oppo_variables = [home_away, 0.0, 0.0, 0.0]
    try:
        table = soup.find_all('table')[2]
    except IndexError:
        print(name, birth, "no statiz oppo data")
        return oppo_variables

    odd_rows = table.find_all('tr', attrs={'class': 'oddrow_stz0'})
    even_rows = table.find_all('tr', attrs={'class': 'evenrow_stz0'})
    rows = odd_rows + even_rows
    for row in rows:
        tds = row.find_all('td')
        try:
            ba = float(tds[19].text)
        except ValueError:
            ba = 0.0
        if tds[0].text == stadium_name(stadium):
            oppo_variables[1] = ba
        elif tds[0].text == home_away:
            oppo_variables[2] = ba
        elif tds[0].text == 'vs '+_get_team_name(oppo_team):
            oppo_variables[3] = ba

    return oppo_variables


# 상황별 - 날짜/시간 탭
def _time_var(date='2020-07-28', name='터커', birth='1990-07-06'):
    params = {'opt': '4', 'sopt': '0', 'name': name, 'birth': birth, 're': '0', 'da': '1', 'year': '2020'}
    response = requests.get(URL, params=params)
    html = response.text

    soup = bs(html, 'html.parser')
    time_variables = [0.0, 0.0, 0.0, 0.0]
    try:
        table = soup.find_all('table')[2]
    except IndexError:
        print(name, birth, "no statiz time data")
        return time_variables
    odd_rows = table.find_all('tr', attrs={'class': 'oddrow_stz0'})
    even_rows = table.find_all('tr', attrs={'class': 'evenrow_stz0'})
    rows = odd_rows + even_rows
    for row in rows:
        tds = row.find_all('td')
        try:
            hit_rate = float(tds[19].text)
        except ValueError as e:
            hit_rate = 0.0
        except Exception as e:
            hit_rate = 0.0
            print(e, date, name, type(tds[19].text))

        if tds[0].text == '최근7일':
            time_variables[0] = hit_rate
        elif tds[0].text == '최근30일':
            time_variables[1] = hit_rate
        elif tds[0].text == _get_day(date):
            time_variables[2] = hit_rate
        elif tds[0].text == '밤(16시이후)':
            time_variables[3] = hit_rate

    return time_variables


def get_statiz_var(date='2020-08-02', player_id=None, game_id='20200802HTLT02020', stadium='SJ'):
    player_info = _get_player_info(player_id)
    if player_info is None:
        return None
    else:
        name = player_info[0]
        birth = player_info[1]
        return _oppo_var(name, birth, game_id, stadium) + _time_var(date, name, birth)


def get_statiz_variables(name, birth, game_id, stadium, date):
    return _oppo_var(name, birth, game_id, stadium)[1:] + _time_var(date, name, birth)
