import pymysql
import statiz_variables
import joblib
import pandas as pd
import numpy as np
import datetime


# get stadium id
def _get_stadium_id(stadium_name):
    if stadium_name == '잠실':
        return 'JS'
    elif stadium_name == '고척':
        return 'GC'
    elif stadium_name == '사직':
        return 'SJ'
    elif stadium_name == '대구':
        return 'DK'
    elif stadium_name == '수원':
        return 'SW'
    elif stadium_name == '광주':
        return 'KC'
    elif stadium_name == '문학':
        return 'MH'
    elif stadium_name == '대전':
        return 'DJ'
    elif stadium_name == '창원':
        return 'CW'
    elif stadium_name == '포항':
        return 'PH'
    elif stadium_name == '청주':
        return 'CJ'
    else:
        return 'NO'


def _get_today_match(today_date):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM today_games WHERE date=%s;"
    cursor.execute(sql, today_date)
    games_list = cursor.fetchall()
    conn.close()

    return games_list


def _get_players_list(away_id, home_id):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM players WHERE is_enroll=1 AND team_name=%s;"
    cursor.execute(sql, away_id)
    away_players = cursor.fetchall()
    sql = "SELECT * FROM players WHERE is_enroll=1 AND team_name=%s;"
    cursor.execute(sql, home_id)
    home_players = cursor.fetchall()

    return [away_players, home_players]


def _get_weather_info(date, stadium):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM weather WHERE date=%s AND stadium=%s;"
    cursor.execute(sql, (date, stadium))
    buf = cursor.fetchone()
    result = [buf['temperature'][:-1], buf['humidity'][:-1], buf['rain_prob'][:-1], buf['wind'][:-3]]
    conn.close()

    return list(result)


def _get_lineup_info(team_id, player_name):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "SELECT * FROM today_lineup WHERE team_name=%s;"
    cursor.execute(sql, team_id)
    lineup = list(cursor.fetchone())[2:]

    lineup_list = []

    for player in lineup:
        sql = "SELECT ba FROM players WHERE player_name=%s AND team_name=%s;"
        cursor.execute(sql, (player, team_id))
        try:
            lineup_list.append(float(cursor.fetchone()[0]))
        except Exception as e:
            print(e, team_id, player)

    try:
        player_idx = lineup.index(player_name)
        del lineup_list[player_idx]
        lineup_list.append(player_idx)
    except ValueError:
        lineup_list[8] = 9
    except IndexError:
        print(team_id, player_name)

    sql = "SELECT ba FROM players WHERE player_name=%s AND team_name=%s;"
    cursor.execute(sql, (player_name, team_id))
    lineup_list.append(float(cursor.fetchone()[0]))
    conn.close()
    tmp = lineup_list[-1]
    lineup_list[-1] = lineup_list[-2]
    lineup_list[-2] = tmp
    return lineup_list


def _get_players_info(game_info):
    players_list = _get_players_list(game_info['away_id'], game_info['home_id'])
    date = str(game_info['date'])
    stadium = _get_stadium_id(game_info['stadium'])
    game_id = game_info['game_id']

    tmp_list = []

    weather_info = _get_weather_info(date, stadium)

    # away team
    for player in players_list[0]:
        statiz_info = statiz_variables.get_statiz_variables(player['player_name'], str(player['birthday']),
                                                            game_id, stadium, date)
        lineup_info = _get_lineup_info(game_info['away_id'], player['player_name'])
        tmp_list.append([player['player_id']] + weather_info + statiz_info + lineup_info)

    # home team
    for player in players_list[1]:
        statiz_info = statiz_variables.get_statiz_variables(player['player_name'], player['birthday'],
                                                            game_id, stadium, date)
        lineup_info = _get_lineup_info(game_info['home_id'], player['player_name'])
        tmp_list.append([player['player_id']] + weather_info + statiz_info + lineup_info)

    tmp_arr = [list(x) for x in zip(*tmp_list)]
    players_dic = dict(zip(['player_id',
                            'temper',
                            'humidity',
                            'rain_prob',
                            'wind',
                            'stadium_prob',
                            'home_away',
                            'oppo_team',
                            'last_7day',
                            'last_30day',
                            'weekly',
                            'night',
                            'first',
                            'second',
                            'third',
                            'fourth',
                            'fifth',
                            'sixth',
                            'seventh',
                            'eighth',
                            'ba',
                            'hit_num'
                            ], tmp_arr))

    players_df = pd.DataFrame(players_dic)

    return players_df


def _predict(players_df):
    X = players_df.drop(['player_id'], axis=1)
    md = joblib.load('test_train.pkl')
    pred_prob = md.predict_proba(X)
    pred = md.predict(X)
    prob_arr = pred_prob[:, 1:]
    tmp_arr = np.hstack((prob_arr, pred.reshape(-1, 1))).tolist()
    predict_dic = dict(zip(players_df['player_id'], tmp_arr))
    series = pd.Series(data=pred, index=players_df['player_id'])
#    print(series)

    return predict_dic


def _save(date, dic):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    arg = "INSERT INTO predict_prob (date, player_id, prob, hit) values(%s, %s, %s, %s);"
    for key, value in dic.items():
        print(key, value[0], value[1])
        cursor.execute(arg, (date, key, value[0], int(value[1])))
    conn.commit()
    conn.close()


def main():
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    today_games = _get_today_match(today_date)
    if today_games:
        for game in today_games:
            players_df = _get_players_info(game)
            dic = _predict(players_df)
            _save(today_date, dic)

        print(today_date, " all done!")
    else:
        print(today_date, ' has no game')


if __name__ == '__main__':
    main()
