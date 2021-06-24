import pymysql
import statiz_variables
import lineup_variables


def _save_in_db(pof_list=None, stadium='NO', cur_date=None, statiz_list=None, lineup_list=None):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')

    cursor = conn.cursor()
    sql = "SELECT * FROM weather WHERE stadium=%s AND date=%s;"
    cursor.execute(sql, (stadium, cur_date))
    weather_info = cursor.fetchone()

    arg = [pof_list[0],
           cur_date,
           stadium,
           int(float(weather_info[4][:-1])),
           int(float(weather_info[5][:-1])),
           int(float(weather_info[6][:-1])),
           int(float(weather_info[7][:-3])),
           statiz_list[0],
           statiz_list[1],
           statiz_list[2],
           statiz_list[3],
           statiz_list[4],
           statiz_list[5],
           statiz_list[6],
           lineup_list[0],
           lineup_list[1],
           lineup_list[2],
           lineup_list[3],
           lineup_list[4],
           lineup_list[5],
           lineup_list[6],
           lineup_list[7],
           lineup_list[8],
           lineup_list[9],
           pof_list[1]]
    sql = "INSERT INTO pof (player_id, date, stadium, temper, humidity, rain_prob, wind, " \
          "stadium_prob, home_away, oppo_team, last_7day, last_30day, weekly, night, " \
          "first, second, third, fourth, fifth, sixth, seventh, eighth, ba, hit_num, is_hit)" \
          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], arg[7], arg[8], arg[9], arg[10],
                         arg[11], arg[12], arg[13], arg[14], arg[15], arg[16], arg[17], arg[18], arg[19], arg[20],
                         arg[21], arg[22], arg[23], arg[24]))
    conn.commit()
    conn.close()


def save(pof_list=None, stadium=None, date=None, game_id=None):
    for player in pof_list:
        statiz_list = statiz_variables.get_statiz_var(date=date, player_id=player[0], game_id=game_id, stadium=stadium)
        if statiz_list is None:
            continue
        lineup_list = lineup_variables.get_lineup_vars(game_id=game_id, home_away=statiz_list[0], player_id=player[0])
        _save_in_db(player, stadium, date, statiz_list[1:], lineup_list)
    return
