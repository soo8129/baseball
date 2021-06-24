import pymysql
from datetime import date, timedelta
import pandas as pd


def _all_players_result(date):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = ("SELECT predict_prob.player_id, players.team_name, players.player_name, predict_prob.prob, predict_prob.hit, pof.is_hit FROM predict_prob LEFT JOIN pof ON predict_prob.player_id=pof.player_id AND predict_prob.date=pof.date LEFT JOIN players ON predict_prob.player_id=players.player_id WHERE predict_prob.date=%s ORDER BY predict_prob.prob DESC;")
    cursor.execute(sql, date)
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print(date, ' no predict_prob info')


# for make dict
def _all_players_load(date):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # all predict players list when date
    sql = "SELECT * FROM predict_prob where date=%s ORDER BY prob;"
    cursor.execute(sql, date)
    dic = cursor.fetchall()
    tmp_list = []
    for i in dic:
        tmp_sql = "SELECT is_hit FROM pof WHERE player_id=%s AND date=%s;"
        cursor.execute(tmp_sql, (i['player_id'], i['date']))
        buf = cursor.fetchone()

        # 미출전 제외
        if buf != None:
            tmp_list.append([i['player_id'], i['prob'], i['hit'], buf['is_hit']])
    tmp_dic = dict(zip(['player_id', 'prob', 'hit', 'is_hit'], [list(x) for x in zip(*tmp_list)]))
    df = pd.DataFrame(tmp_dic, columns=['player_id', 'prob', 'hit', 'is_hit'])
    print(df)
    print('correct', df[df.hit==df.is_hit].count())
    print('incorrect', df[df.hit!=df.is_hit].count())


# dict print
def _all_players(date):
    pred_dic = _all_players_load(date)


def main():
    yesterday = (date.today()-timedelta(1)).strftime('%Y-%m-%d')
    _all_players_result('2020-08-22')
    print(yesterday, "predict prob")

    # for dict
    # _all_players(yesterday)


if __name__ == '__main__':
    main()

