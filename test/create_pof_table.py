import pymysql


# create pass of fail table
def create_pof_table():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='chldlstns1!',
                         db='baseball',
                         charset='utf8')
    cursor = db.cursor()
    sql = "CREATE TABLE pof (" \
          "idx INT PRIMARY KEY NOT NULL AUTO_INCREMENT," \
          "player_id INT(6) NOT NULL," \
          "date DATE NOT NULL," \
          "stadium VARCHAR(2) NOT NULL," \
          "temper INT(4) NULL," \
          "humidity INT(2) NULL," \
          "rain_prob INT(2) NULL," \
          "wind INT(1) NULL," \
          "stadium_prob FLOAT NOT NULL," \
          "home_away FLOAT NOT NULL," \
          "oppo_team FLOAT NOT NULL," \
          "last_7day FLOAT NOT NULL," \
          "last_30day FLOAT NOT NULL," \
          "weekly FLOAT NOT NULL," \
          "night FLOAT NOT NULL," \
          "first FLOAT NOT NULL," \
          "second FLOAT NOT NULL," \
          "third FLOAT NOT NULL," \
          "fourth FLOAT NOT NULL," \
          "fifth FLOAT NOT NULL," \
          "sixth FLOAT NOT NULL," \
          "seventh FLOAT NOT NULL," \
          "eighth FLOAT NOT NULL," \
          "ba FLOAT NULL," \
          "hit_num INT(2) NOT NULL," \
          "is_hit BOOL NOT NULL)"
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
    finally:
        db.close()


create_pof_table()
