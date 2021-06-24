import pymysql


# create weather table
def create_weather_table():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='chldlstns1!',
                         db='baseball',
                         charset='utf8')
    cursor = db.cursor()
    sql = "CREATE TABLE weather (" \
          "idx INT PRIMARY KEY NOT NULL AUTO_INCREMENT," \
          "date DATE NOT NULL," \
          "stadium VARCHAR(2) NOT NULL," \
          "time VARCHAR(5) NOT NULL," \
          "temperature VARCHAR(5) NOT NULL," \
          "humidity VARCHAR(5) NOT NULL," \
          "rain_prob VARCHAR(5) NOT NULL," \
          "wind VARCHAR(5) NOT NULL)"
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
    finally:
        db.close()
