from selenium import webdriver
import pymysql
import datetime


# save in db
def _save_in_weather_db(date=None, env_list=None):
    try:
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='chldlstns1!',
                             charset='utf8',
                             db='baseball')
    except Exception as e:
        print(e)
        return

    cursor = db.cursor()
    for env in env_list:
        sql = "INSERT INTO weather (date, stadium, time, temperature, humidity, rain_prob, wind)" \
              "VALUES(%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (date, env[0], env[1], env[2], env[3], env[4], env[5]))
        db.commit()

    db.close()


def get_weather_today():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = 'C:/Users/soo81/webcrawling/chromedriver.exe'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    URL = 'https://www.koreabaseball.com/Schedule/Weather.aspx#none'
    driver.get(URL)
    driver.implicitly_wait(3)

    weather_list = []
    stadium_list = driver.find_element_by_xpath('//*[@id="ulStadiumList"]').find_elements_by_tag_name('li')
    for stadium in stadium_list:
        stadium.click()
        tmp_table = stadium.find_element_by_xpath('//*[@id="tblForecast"]')
        tmp_table_trs = tmp_table.find_elements_by_tag_name('tr')
        tmp_list = [stadium.get_attribute('data-stadium')]
        for tr in tmp_table_trs:
            tmp_tr = tr.text.split()[-1:]
            tmp_list.append(tmp_tr[0])

        weather_list.append(tmp_list)

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    _save_in_weather_db(today, weather_list)


get_weather_today()
