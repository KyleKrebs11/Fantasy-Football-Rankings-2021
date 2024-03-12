import pandas as pd
from src.main import file_maker
from src.main.file_maker import save_df_to_csv
from src.main.file_maker import load_csv_file

'''
TS% - True Shooting Percentage; the formula is PTS / (2 * TSA). TSA = FGA + 0.44 * FTA
True shooting percentage is a measure of shooting efficiency that takes into account field goals, 
3-point field goals, and free throws.
'''

def calculate_true_shooting_percentage(df: pd.DataFrame):
    df["TS%"] = round(df["PTS"] / (2 * (df["FGA"] + 0.44 * df["FTA"])), 2)
    df = df.sort_values(by=["TS%"], ascending=False)
    print(df[["Player", "TS%"]])
'''
Players who took over 100 3PA and made 35% of them
'''


def great_shooters(df: pd.DataFrame, filename):
    df = df.rename({"3PA": "ThreeA", "3P%": "ThreeP"}, axis='columns')
    filter_df = df.query("ThreeA >= 100 & ThreeP >= .35")
    filter_df = filter_df.sort_values(by=["ThreeP"], ascending=False)
    filter_df = filter_df[["Player", "ThreeP"]]
    save_df_to_csv(filter_df, filename)



'''
Kyles Personal Fantasy Football Rankings
'''

def wr_stats(df: pd.DataFrame, filename):
    max_yards = df["Yds"].max()
    max_targets = df["Tgt"].max()
    max_rec = df["Rec"].max()
    max_air_yards = df["AirYards"].max()
    max_yards_after_catch = df["YAC"].max()
    max_snaps = df["TTL"].max()
    max_tds = df["TD"].max()

    df["YdsG"] = (df["Yds"] / max_yards * .96)
    df["TgtG"] = (df["Tgt"] / max_targets * .95)
    df["RecG"] = (df["Rec"] / max_rec * .94)
    df["AirYardsG"] = (df["AirYards"] / max_air_yards * .91)
    df["YACG"] = (df["YAC"] / max_yards_after_catch * .88)
    df["TtlG"] = (df["TTL"] / max_snaps * .89)
    df["TdG"] = (df["TD"] / max_tds * .87)
    df["WRG"] = df["YdsG"] + df["TgtG"] + df["RecG"] + df["AirYardsG"] + df["YACG"] + df["TtlG"] + df["TdG"]
    df["WRG"] = df["WRG"] / 6.4 * 100
    filter_df = df[["Player", "WRG"]]
    filter_df = filter_df.sort_values(by=["WRG"], ascending=False)
    save_df_to_csv(filter_df, filename)
wr_stats(load_csv_file("football/2020/receiving_stats/master_receiving_2020"), "football/2020/position_grades/wr_grades")


def rb_stats(df: pd.DataFrame, filename):
    df["Touches"] = df["Rec"] + df["Att"]

    max_snaps = df["TTL"].max()
    max_touches = df["Touches"].max()
    max_rYds = df["Yds"].max()
    max_snapP = df["AVG"].max()
    max_rec = df["Rec"].max()
    max_rcYds = df["ReceivingYds"].max()
    max_Att = df["Att"].max()
    max_rTds = df["TD"].max()

    df["SnapsG"] = (df["TTL"] / max_snaps * .93)
    df["TouchesG"] = (df["Touches"] / max_touches * .92)
    df["rYdsG"] = (df["Yds"] / max_rYds * .91)
    df["snapPG"] = (df["AVG"] / max_snapP * .89)
    df["RecG"] = (df["Rec"] / max_rec * .88)
    df["rcYdsG"] = (df["ReceivingYds"] / max_rcYds * .88)
    df["AttG"] = (df["Att"] / max_Att * .86)
    df["rTds"] = (df["TD"] / max_rTds * .86)
    df["RBG"] = df["SnapsG"] + df["rYdsG"] + df["snapPG"] + df["RecG"] + df["rcYdsG"] + df["AttG"] + df["rTds"]
    df["RBG"] = df["RBG"] / 7.13 * 100
    filter_df = df[["Player", "RBG"]]
    filter_df = filter_df.sort_values(by=["RBG"], ascending=False)
    save_df_to_csv(filter_df, filename)

rb_stats(load_csv_file("football/2020/rb_stats/rb_rushing_2020"), "football/2020/position_grades/rb_grade")


def qb_stats(df: pd.DataFrame, filename):
    max_pTDs = df["TD"].max()
    max_pYds = df["Yds"].max()
    max_CAY = df["CAY"].max()
    max_IAY = df["IAY"].max()
    max_pATT = df["Att"].max()
    max_AYA = df["AY/A"].max()
    max_QBR = df["QBR"].max()

    df["pTDG"] = (df["TD"] / max_pTDs * .88)
    df["pYdsG"] = (df["Yds"] / max_pYds * .82)
    df["CAYG"] = (df["CAY"] / max_CAY * .80)
    df["IAYG"] = (df["IAY"] / max_IAY * .73)
    df["pATTG"] = (df["Att"] / max_pATT * .67)
    df["AY/AG"] = (df["AY/A"] / max_AYA * .42)
    df["QBRG"] = (df["QBR"] / max_QBR * .46)
    df["QBG"] = df["pTDG"] + df["pYdsG"] + df["CAYG"] + df["IAYG"] + df["pATTG"] + df["AY/AG"] + df["QBRG"]
    df["QBG"] = df["QBG"] / 4.78 * 100

    filter_df = df[["Player", "QBG"]]
    filter_df = filter_df.sort_values(by=["QBG"], ascending=False)
    save_df_to_csv(filter_df, filename)

qb_stats(load_csv_file("football/2020/qb_stats/master_passing_2020"),"football/2020/position_grades/qb_grade")


def te_stats(df: pd.DataFrame, filename):
    max_Yds = df["Yds"].max()
    max_Rec = df["Rec"].max()
    max_Tgts = df["Tgt"].max()
    max_AirYards = df["AirYards"].max()
    max_Yac = df["YAC"].max()
    max_TD = df["TD"].max()
    max_snaps = df["TTL"].max()

    df["YdsG"] = (df["Yds"] / max_Yds * .99)
    df["RecG"] = (df["Rec"] / max_Rec * .98)
    df["TgtsG"] = (df["Tgt"] / max_Tgts * .98)
    df["AirYardsG"] = (df["AirYards"] / max_AirYards * .94)
    df["YacG"] = (df["YAC"] / max_Yac * .91)
    df["TDG"] = (df["TD"] / max_TD * .88)
    df["SnapsG"] = (df["TTL"] / max_snaps * .84)
    df["TEG"] = df["YdsG"] + df["RecG"] + df["TgtsG"] + df["AirYardsG"] + df["YacG"] + df["TDG"] + df["SnapsG"]
    df["TEG"] = df["TEG"] / 6.52 * 100

    filter_df = df[["Player", "TEG"]]
    filter_df = filter_df.sort_values(by=["TEG"], ascending=False)
    save_df_to_csv(filter_df, filename)

te_stats(load_csv_file("football/2020/receiving_stats/te_receiving_2020"), "football/2020/position_grades/te_grade")





