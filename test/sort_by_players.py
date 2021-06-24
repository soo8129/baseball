import pymysql
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import joblib


def _for_predict():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    conn.close()


def _all_players_list():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "SELECT player_id FROM players;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    players_list = []
    for row in rows:
        players_list += row
    
    return players_list


def _get_pof(player_id):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM pof WHERE player_id=%s;"
    cursor.execute(sql, player_id)
    rows = cursor.fetchall()
    player_list = []
    for row in rows:
        tmp_list = [row['player_id'],
                    row['temper'],
                    row['humidity'],
                    row['rain_prob'],
                    row['wind'],
                    row['stadium_prob'],
                    row['home_away'],
                    row['oppo_team'],
                    row['last_7day'],
                    row['last_30day'],
                    row['weekly'],
                    row['night'],
                    row['first'],
                    row['second'],
                    row['third'],
                    row['fourth'],
                    row['fifth'],
                    row['sixth'],
                    row['seventh'],
                    row['eighth'],
                    row['ba'],
                    row['hit_num'],
                    row['is_hit']]
        player_list.append(tmp_list)

    tmp_arr = [list(x) for x in zip(*player_list)]
    player_dic = dict(zip(['player_id',
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
                           'hit_num',
                           'is_hit'
                           ], tmp_arr))
    conn.close()
    return player_dic


def _train(player_dic=None, player_id=None):
    if not player_dic:
        return
    df = pd.DataFrame(player_dic)
    try:
        X = df.drop(['player_id', 'is_hit'], axis=1)
        y = df['is_hit']

        # data split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
        rf = RandomForestClassifier(random_state=0)
        rf.fit(X_train, y_train)
        pred = rf.predict(X_test)
        
        model_name = 'players_model/%d_all.pkl' % player_id
        joblib.dump(pred, model_name)
        print(accuracy_score(y_test, pred))

        # extract feature_importances
        feature_importance = rf.feature_importances_

        # sort
        # print(df.sort_values(by=0, ascending=False))

        return feature_importance
    except Exception as e:
        print(e)


# analyze players feature importances
def _statistics(players_array):
    players_df = DataFrame(players_array, columns=['temper', 'humidity', 'rain_prob', 'wind', 'stadium_prob', 'home_away', 'oppo_team', 'last_7days', 'last_30days', 'weekly', 'night', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ba', 'hit_num']).dropna()
    print('features importances')
    print(players_df)
    print(players_df.mean().sort_values(ascending=False))


def main():
    players_list = _all_players_list()
    players_array = np.zeros(shape=(len(players_list), 21))
    idx = 0
    for player in players_list:
        tmp = _train(_get_pof(player), player)
        players_array[idx] = tmp
        idx += 1

    _statistics(players_array)


if __name__ == '__main__':
    main()

