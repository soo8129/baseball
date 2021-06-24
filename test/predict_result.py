import pymysql
import datetime


def _model_all(date='2020-08-16'):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "SELECT predict_prob.player_id, players.player_name, players.team_name, predict_prob.prob, predict_prob.hit from predict_prob left join players on predict_prob.player_id=players.player_id where predict_prob.date=%s order by predict_prob.prob;"
    cursor.execute(sql, date)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def main():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    _model_all(today)
    print(today, ' 예측결과')


if __name__ == '__main__':
    main()

