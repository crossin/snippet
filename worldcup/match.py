#coding:utf8
import pandas as pd

ALL_TEAMS = [
'Russia', 'Saudi Arabia', 'Egypt', 'Uruguay',
'Portugal', 'Spain', 'Morocco', 'Iran',
'France', 'Australia', 'Peru', 'Denmark',
'Argentina', 'Iceland', 'Croatia', 'Nigeria',
'Brazil', 'Switzerland', 'Costa Rica', 'Serbia',
'Germany', 'Mexico', 'Sweden', 'Korea Republic',
'Belgium', 'Panama', 'Tunisia', 'England',
'Poland', 'Senegal', 'Colombia', 'Japan'
]

def load_data(year=1800):
    df = pd.read_csv('results.csv')
    return df[df['date'] > str(year)]

# 计算某支球队对战其他球队的历史战绩
def calc_rate(team, df):
    df_home = df[(df['home_team']==team) & (df['away_team'].isin(ALL_TEAMS))]
    df_away = df[(df['away_team']==team) & (df['home_team'].isin(ALL_TEAMS))]
    win = len(df_home[df_home['home_score'] > df_home['away_score']]) + len(df_away[df_away['away_score'] > df_away['home_score']])
    draw = len(df_home[df_home['home_score'] == df_home['away_score']]) + len(df_away[df_away['away_score'] == df_away['home_score']])
    lose = len(df_home[df_home['home_score'] < df_home['away_score']]) + len(df_away[df_away['away_score'] < df_away['home_score']])
    count = len(df_home) + len(df_away)
    print('%s 对阵本届世界杯中球队历史战绩赔率：%d 胜, %d 平, %d 负' % (team, win, draw, lose))
    odds = count / win, count / draw, count / lose
    print('参考赔率：%.2f, %.2f, %.2f\n' % odds)
    return count, win, draw, lose

# 根据两支球队的历史战绩计算相互间的胜率
def match_rate(home, away, data):
    count1, win1, draw1, lose1 = calc_rate(home, data)
    count2, win2, draw2, lose2 = calc_rate(away, data)
    count = count1 + count2
    odds = count / (win1 + lose2), count / (draw1 + draw2), count / (lose1 + win2)
    print('历史综合参考赔率：%.2f, %.2f, %.2f\n' % odds)

# 计算两支球队相互间的胜率
def match(home, away, year=2014):
    df = load_data(year)
    df1 = df[(df['home_team']==home) & (df['away_team']==away)]
    df2 = df[(df['home_team']==away) & (df['away_team']==home)]
    count = len(df1) + len(df2)
    if count > 0:
        win = len(df1[df1['home_score'] > df1['away_score']]) + len(df2[df2['away_score'] > df2['home_score']])
        lose = len(df1[df1['home_score'] < df1['away_score']]) + len(df2[df2['away_score'] < df2['home_score']])
        draw = len(df1[df1['home_score'] == df1['away_score']]) + len(df2[df2['away_score'] == df2['home_score']])
        print('%d 年以来，%s 与 %s 交战 %d 场，%d 胜 %d 平 %d 负' % (year, home, away, count, win, draw, lose))
        try:
            odds = count / win, count / draw, count / lose
            print('参考赔率：%.2f, %.2f, %.2f\n' % odds)
        except:
            print('场次太少，难以计算赔率\n')
    match_rate(home, away, df)


match('England', 'Brazil', 2010)

