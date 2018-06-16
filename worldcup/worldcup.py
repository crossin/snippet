import itertools
import pandas as pd

# 调试输出
def pp(*args):
    print(*args)
    pass


WIN_THRESHOSH = 0.7
WIN_RATE_THRESHOSH = 0.1
YEAR = 2016
YEAR_LONG = 2012

TEAMS = [
['Russia', 'Saudi Arabia', 'Egypt', 'Uruguay'],
['Portugal', 'Spain', 'Morocco', 'Iran'],
['France', 'Australia', 'Peru', 'Denmark'],
['Argentina', 'Iceland', 'Croatia', 'Nigeria'],
['Brazil', 'Switzerland', 'Costa Rica', 'Serbia'],
['Germany', 'Mexico', 'Sweden', 'Korea Republic'],
['Belgium', 'Panama', 'Tunisia', 'England'],
['Poland', 'Senegal', 'Colombia', 'Japan']
]

ALL_TEAMS = [t for g in TEAMS for t in g]

def load_data(year=1800):
    df = pd.read_csv('results.csv')
    return df[df['date'] > str(year)]

# 计算某支球队对战其他球队的历史战绩
def calc_rate(team, df):
    df_home = df[(df['home_team']==team) & (df['away_team'].isin(ALL_TEAMS))]
    df_away = df[(df['away_team']==team) & (df['home_team'].isin(ALL_TEAMS))]
    win = len(df_home[df_home['home_score'] > df_home['away_score']]) + len(df_away[df_away['away_score'] > df_away['home_score']])
    draw = len(df_home[df_home['home_score'] == df_home['away_score']]) + len(df_away[df_away['away_score'] == df_away['home_score']])
    win_rate = (win + draw / 2) / (len(df_home) + len(df_away))
    if team == 'Russia':
        win_rate += 0.5  # 东道主加成
    return win_rate

# 根据两支球队的历史战绩计算相互间的胜率
def match_rate(home, away):
    win_rate1 = calc_rate(home, data)
    win_rate2 = calc_rate(away, data)
    pp(win_rate1, win_rate2)
    if win_rate1 - win_rate2 > WIN_RATE_THRESHOSH:
        return 1
    elif win_rate2 - win_rate1 > WIN_RATE_THRESHOSH:
        return -1
    else:
        if win_rate1 > win_rate2:
            return 0.5
        elif win_rate1 < win_rate2:
            return -0.5
        else:
            return 0

# 计算两支球队相互间的胜率
def match(home, away, long=False):
    if long:
        df = data_long
    else:
        df = data
    df1 = df[(df['home_team']==home) & (df['away_team']==away)]
    df2 = df[(df['home_team']==away) & (df['away_team']==home)]
    count = len(df1) + len(df2)
    if count == 0:
        if not long:
            return match(home, away, True)  # 使用更早的数据
        else:
            return match_rate(home, away)  # 使用间接对战数据
    win = len(df1[df1['home_score'] > df1['away_score']]) + len(df2[df2['away_score'] > df2['home_score']])
    lose = len(df1[df1['home_score'] < df1['away_score']]) + len(df2[df2['away_score'] < df2['home_score']])
    draw = len(df1[df1['home_score'] == df1['away_score']]) + len(df2[df2['away_score'] == df2['home_score']])
    pp(count, win, lose, draw)
    if (win + draw / 2) / count > WIN_THRESHOSH:
        return 1
    elif (lose + draw / 2) / count > WIN_THRESHOSH:
        return -1
    else:
        if win > lose:
            return 0.5
        elif lose > win:
            return -0.5
        else:
            return 0.5 * match_rate(home, away)

result = {}
for offset in range(11):  # 年限循环
    for offset_l in range(4):  # 更早年限循环
        data = load_data(YEAR - offset)
        data_long = load_data(YEAR - offset - 4 - offset_l)
        teams_rate = []
        teams_ko = []

        # 小组赛
        for group in TEAMS:
            scores = {}
            for t in group:
                scores[t] = 0
            for home, away in itertools.combinations(group, 2):
                # 两两对战
                s = match(home, away)
                pp(home, away, s)
                if s == 1:
                    scores[home] += 3
                elif s == -1:
                    scores[away] += 3
                else:
                    scores[home] += 1
                    scores[away] += 1

            pp(scores)
            rank = sorted(scores.items(), key=lambda x: -x[1])
            # 处理平分情况
            for i in range(3):
                for j in range(i+1, 4):
                    if rank[i][1] == rank[j][1]:
                        # 平分球队直接比较历史胜率
                        s = match_rate(rank[i][0], rank[j][0])
                        if s > 0:
                            scores[rank[i][0]] += 0.1
                        elif s < 0:
                            scores[rank[j][0]] += 0.1
                        else:
                            pp('DRAW ERROR!')

            rank = sorted(scores.items(), key=lambda x: -x[1])
            pp(rank)

            # 输出小组赛结果
            for i in rank:
                print(i[0], i[1], end=' | ')
            print()
            teams_ko.append([rank[0][0], rank[1][0]])
        pp(teams_ko)

        # 淘汰赛分配
        ko_list = []
        for j in [0, 1]:
            for i in range(8):
                ko_list.append(teams_ko[i][(i+j)%2])
        pp(ko_list)
        # 4轮淘汰赛
        for rd in range(4):
            for vs in range(8//2**rd):
                home = ko_list[vs*2]
                away = ko_list[vs*2+1]
                win = match(home, away)
                pp(win)
                if win > 0:
                    ko_list[vs] = home
                elif win < 0:
                    ko_list[vs] = away
                else:
                    pp('ko', home, away, 'DRAW ERROR!')
            # 输出淘汰赛结果
            for i in ko_list[:vs+1]:
                print(i, end='  ')
            print()
        result[ko_list[0]] = result.get(ko_list[0], 0) + 1
        # 最终结果累计
        print(YEAR-offset, ko_list[0], result)
    print()
