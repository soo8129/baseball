import pymysql


# create baseball table and players table
def main():
    # create baseball database query
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='chldlstns1!',
                         charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("CREATE DATABASE baseball;")
        db.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.execute("USE baseball;")

    sql = "CREATE TABLE players (" \
          "player_id INT(6) PRIMARY KEY NOT NULL," \
          "player_name VARCHAR(32) NOT NULL," \
          "birthday DATE NOT NULL, " \
          "team_name VARCHAR(32) NULL," \
          "is_enroll BOOL NOT NULL)"

    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
    finally:
        db.close()
