import numpy as np
from pandas import Series, DataFrame
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_predict, cross_val_score
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import learning_curve, GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql
import joblib


def print_score(classifier, X_train, y_train, X_test, y_test, train=True):
    if train:
        print("Training results:\n")
        print('Accuracy Score: {0:.4f}\n'.format(accuracy_score(y_train, classifier.predict(X_train))))
        print('Classification Report:\n{}\n'.format(classification_report(y_train, classifier.predict(X_train))))
        print('Confusion Matrix:\n{}\n'.format(confusion_matrix(y_train, classifier.predict(X_train))))
        res = cross_val_score(classifier, X_train, y_train, cv=10, n_jobs=-1, scoring='accuracy')
        print('Average Accuracy:\t{0:.4f}\n'.format(res.mean()))
        print('Standard Deviation:\t{0:.4f}'.format(res.std()))
    elif not train:
        print("Test results:\n")
        print('Accuracy Score: {0:.4f}\n'.format(accuracy_score(y_test, classifier.predict(X_test))))
        print('Classification Report:\n{}\n'.format(classification_report(y_test, classifier.predict(X_test))))
        print('Confusion Matrix:\n{}\n'.format(confusion_matrix(y_test, classifier.predict(X_test))))


def _get_players_info():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM pof;"
    cursor.execute(sql)
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


def _test1():
    players_dic = _get_players_info()
    data_frame = pd.DataFrame(players_dic)
    X = data_frame.drop(['player_id', 'is_hit'], axis=1)
    y = data_frame['is_hit']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    sc = StandardScaler()

    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    pca = PCA(n_components=2)

    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

    classifier = RandomForestClassifier(n_estimators=50, criterion='entropy', random_state=42)
    classifier.fit(X_train, y_train)

    print_score(classifier, X_train, y_train, X_test, y_test, train=True)


def _test2():
    players_dic = _get_players_info()
    data_frame = pd.DataFrame(players_dic)
    X = data_frame.drop(['player_id', 'is_hit'], axis=1)
    y = data_frame['is_hit']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    rf = RandomForestClassifier(random_state=0)
    rf.fit(X_train, y_train)
    RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini', max_depth=None, max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=2, min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=None, oob_score=False, random_state=0, verbose=0, warm_start=False)
    pred = rf.predict(X_test)
    joblib.dump(rf, 'test_train.pkl')
    print(accuracy_score(y_test, pred))

#    rf_param_grid = {
#            'n_estimators' : [100, 200],
#           'max_depth' : [6, 8 ,10, 12],
#            'min_samples_leaf' : [3, 5, 7, 10],
#            'min_samples_split' : [2, 3, 5, 10]
#            }
#    rf_grid = GridSearchCV(rf, param_grid = rf_param_grid, scoring='accuracy', n_jobs=-1, verbose = 1)
#    rf_grid.fit(X_train, y_train)

#    print("acc", rf_grid.best_score_)
#    print("param", rf_grid.best_params_)

    # extract feature_importances
    feature_importances = rf.feature_importances_
    tmp_df = pd.DataFrame(feature_importances, X_train.columns)
    print(tmp_df.sort_values(by=0, ascending=False))


def main():
    _test2()


if __name__ == '__main__':
    main()

