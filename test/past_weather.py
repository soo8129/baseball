from bs4 import BeautifulSoup, Comment
import requests
import calendar
import pymysql
import time

URL = 'https://www.weather.go.kr/weather/climate/past_tendays.jsp?'


def _get_stadium(stn='0'):
    if stn == '156':
        return 'KC'
    elif stn == '119':
        return 'SW'
    elif stn == '143':
        return 'DK'
    elif stn == '155':
        return 'CW'
    elif stn == '159':
        return 'SJ'
    elif stn == '133':
        return 'DJ'
    elif stn == '131':
        return 'CJ'
    elif stn == '138':
        return 'PH'
    elif stn == '108':
        return 'GC'
    elif stn == '112':
        return 'MH'
    else:
        return 'NO'


def _save_in_weather_db(stadium, date_list, temper_list, humidity_list, rain_prob_list, wind_list):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = 'INSERT INTO weather (date, stadium, time, temperature, humidity, rain_prob, wind) ' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s)'

    for i in range(0, len(date_list)):
        arg = [date_list[i], stadium, '19시', temper_list[i] + '℃',
               humidity_list[i] + '%', rain_prob_list[i] + '%', wind_list[i] + 'm/s']
        cursor.execute(sql, arg)

    conn.commit()
    conn.close()


def _get_weather_10days(stn='156', year='2020', month='7'):
    obs_list = ['1', '11', '21']
    last_day = calendar.monthrange(int(year), int(month))[1]
    tot_date = []
    for i in range(1, last_day + 1):
        tmp_str = '-'.join([year, month.zfill(2), str(i).zfill(2)])
        tot_date += [tmp_str]

    tot_temper = []
    tot_humidity = []
    tot_rain_prob = []
    tot_wind = ['4' for i in range(1, last_day + 1)]

    for obs in obs_list:
        params = {'stn': stn, 'yy': year, 'mm': month, 'obs': obs}
        response = requests.get(URL, params=params)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        while len(soup.find_all('table')) < 2:
            time.sleep(1)

            response = requests.get(URL, params=params)
            html = response.text

            soup = BeautifulSoup(html, 'html.parser')

        table = soup.find_all('table')[1]

        for element in table(text=lambda text: isinstance(text, Comment)):
            element.extract()

        trs = table.find_all('tr')

        # temper
        temper_tds = trs[1].find_all('td')
        temper_list = []
        for td in temper_tds:
            temper_list.append(td.text.strip())
        temper_list = temper_list[:-2]
        tot_temper += temper_list

        # humidity
        humidity_tds = trs[9].find_all('td')
        humidity_list = []
        for td in humidity_tds:
            humidity_list.append(td.text.strip())
        humidity_list = humidity_list[:-2]
        tot_humidity += humidity_list

        # rain_prob
        rain_prob_tds = trs[23].find_all('td')
        rain_prob_list = []
        for td in rain_prob_tds:
            rain_prob_list.append(td.text.strip())
        rain_prob_list = rain_prob_list[:-2]
        idx = 0
        for rain in rain_prob_list:
            if rain == '':
                rain_prob_list[idx] = '5'
            else:
                if round(float(rain)) < 100:
                    rain_prob_list[idx] = str(round(float(rain) * 0.9))
                elif round(float(rain)) >= 100:
                    rain_prob_list[idx] = '90'
            idx += 1

        tot_rain_prob += rain_prob_list

    _save_in_weather_db(_get_stadium(stn), tot_date, tot_temper, tot_humidity, tot_rain_prob, tot_wind)


stn_list = ['156', '119', '143', '155', '159', '133', '131', '138', '112', '108']

#for stn1 in stn_list:
#    print(_get_stadium(stn1))
#    _get_weather_10days(stn=stn1, month='5')
#for stn2 in stn_list:
#    print(_get_stadium(stn2))
#    _get_weather_10days(stn=stn2, month='6')
#for stn3 in stn_list:
#    print(_get_stadium(stn3))
#    _get_weather_10days(stn=stn3, month='7')
_get_weather_10days(stn='108', month='5')
_get_weather_10days(stn='108', month='6')
_get_weather_10days(stn='108', month='7')
print('all done!')
