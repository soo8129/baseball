import pymysql
import requests
from bs4 import BeautifulSoup as bs


def main():
    URL = 'https://www.koreabaseball.com/Record/Player/HitterDetail/Basic.aspx?'
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM players WHERE ba=0;"
    cursor.execute(sql)
    players = cursor.fetchall()
    for player in players:
        params = {'playerId': player['player_id']}
        response = requests.get(URL, params=params)
        html = response.text
        soup = bs(html, 'html.parser')
        table = soup.select_one('#contents > div.sub-content > div.player_records > div.tbl-type02.mb10')
        try:
            tr = table.find_all('tr')[1]
            ba = tr.find_all('td')[1].text
            if ba == '-':
                ba = 0.0
            else:
                ba = float(ba)
        except Exception as e:
            print(e)
            ba = 0.0

        print(player['player_id'], ba)
        sql = "UPDATE players SET ba=%s WHERE player_id=%s;"
        cursor.execute(sql, (ba, player['player_id']))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
