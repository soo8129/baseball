import game_id_to_pass_or_fail_id
import date_to_game_id
import datetime
import save_pof_db


# today date
def _today():
    today = datetime.datetime.now().strftime('%Y-%m-%d').split('-')
    now_year = int(today[0])
    now_month = int(today[1])
    now_date = int(today[2])
    return [now_year, now_month, now_date]


# get past pof data
def _get_past_data():
    start_date = datetime.datetime.strptime('2020-08-05', '%Y-%m-%d')
    for i in range(4):
        cur_date = (start_date + datetime.timedelta(days=i)).date()
        cur_date_str = cur_date.strftime('%Y-%m-%d')
        cur_date_list = cur_date_str.split('-')
        print(cur_date_str)

        game_info = date_to_game_id.get_game_id(int(cur_date_list[0]), int(cur_date_list[1]), int(cur_date_list[2]))
        if game_info is None:
            continue

        for game in game_info:
            players_pof_list = game_id_to_pass_or_fail_id.info(game[0])
            save_pof_db.save(players_pof_list, game[1], cur_date_str, game[0])


def main():
    today = _today()
    yesterday = [today[0], today[1], today[2] - 1]
    _yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    game_info = date_to_game_id.get_game_id(yesterday[0], yesterday[1], yesterday[2])

    for game in game_info:
        players_pof_list = game_id_to_pass_or_fail_id.info(game[0])
        save_pof_db.save(players_pof_list, game[1], _yesterday, game[0])


if __name__ == '__main__':
     main()

