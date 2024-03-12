import pandas as pd


resources_path = "../../resources/"

def save_table_to_csv(table, filename):
    df = pd.DataFrame(table[1:], columns = table[0])
    df.to_csv(resources_path + filename + ".csv")

def save_df_to_csv(df, filename):
    df = df.round(4)
    df.to_csv(resources_path + filename + ".csv")

def load_csv_file(path):
    return pd.read_csv(resources_path + path + ".csv")

def clean_dataframes(df : pd.DataFrame):
    if df.__contains__("Unnamed: 0"):
        df.__delitem__("Unnamed: 0")
    if df.__contains__("Unnamed: 0.1"):
        df.__delitem__("Unnamed: 0.1")
    if df.__contains__("Unnamed: 0.1.1"):
        df.__delitem__("Unnamed: 0.1.1")
    if df.__contains__("\xa0"):
        df.__delitem__("\xa0")
    if df.__contains__("\xa0.1"):
        df.__delitem__("\xa0.1")
    df = df.dropna(how='all')
    df = df.round(4)
    return df

def get_duplicate_columns(df1: pd.DataFrame, df2 : pd.DataFrame):
    df1_columns = df1.columns.values
    df2_columns = df2.columns.values
    return list(set(df1_columns) & set(df2_columns))

def combine_dataframes(df1 : pd.DataFrame, df2 : pd.DataFrame, filename):
    df1 = clean_dataframes(df1)
    df2 = clean_dataframes(df2)
    merge_df = pd.merge(df1, df2, how="left", on=get_duplicate_columns(df1, df2))
    save_df_to_csv(merge_df, filename)

def append_dataframes(df1 : pd.DataFrame, df2 : pd.DataFrame, filename):
    df1 = clean_dataframes(df1)
    df2 = clean_dataframes(df2)
    merge_df = df1.append(df2)
    merge_df = merge_df.reset_index()
    merge_df.__delitem__("index")
    save_df_to_csv(merge_df, filename)

def add_air_yards():
    df = load_csv_file("football/2020/2020_advanced_receiving.csv")
    df["AirYards"] = df["ADOT"] * df["Tgt"]
    save_df_to_csv(df, "football/2020/2020_advanced_receiving")

def clean_players_names(filename):
    df = load_csv_file(filename)
    df["Player"] = list(map(lambda x : x.replace("*","")
                            .replace("+","")
                            .replace(" ","")
                            .replace("IV","")
                            .replace("III","")
                            .replace("II","")
                            .replace("Jr.","")
                            .replace("Sr.","")
                            .replace(".","")
                            .replace("'",""), df["Player"].values.tolist()))
    df = clean_dataframes(df)
    save_df_to_csv(df, filename)

'''
type is either "qb", "wr" or "rb"
'''
def create_master_csv(year, type):
    verb = ""
    path = "football/" + str(year) + "/"
    if type == "qb":
        verb = "passing"
        path = path + "qb_stats/"
    elif type == "wr":
        verb = "receiving"
        path = path + "rb_stats/"
    else:
        verb = "rushing"
        path = path + "receiving_stats/"

    clean_players_names(path + str(year) + "_advanced_" + verb)
    clean_players_names(path + str(year) + "_standard_" + verb)
    combine_dataframes(load_csv_file(path + str(year) + "_advanced_" + verb),
                       load_csv_file(path + str(year) + "_standard_" + verb),
                       path + "master_" + verb + "_" + str(year))

    clean_players_names("football/2020/snap_count_all")
    clean_players_names(path + "master_" + verb + "_" + str(year))
    combine_dataframes(load_csv_file(path + "master_" + verb + "_" + str(year)),
                       load_csv_file("football/2020/snap_count_all"),
                       path + "master_" + verb + "_" + str(year))
    if type == "rb":
        add_receiving_stats_to_rushing_master()

def add_receiving_stats_to_rushing_master():
    master_rushing = load_csv_file("football/2020/rb_stats/master_rushing_2020")
    receiving_stats = load_csv_file("football/2020/receiving_stats/master_receiving_2020")[["Player", "Rec", "Yds"]]
    receiving_stats = receiving_stats.rename({"Yds": "ReceivingYds"}, axis='columns')
    clean_players_names("football/2020/rb_stats/master_rushing_2020")
    clean_players_names("football/2020/receiving_stats/master_receiving_2020")
    combine_dataframes(master_rushing, receiving_stats, "football/2020/rb_stats/master_rushing_2020")


def get_TEs():
    df = load_csv_file("football/2020/receiving_stats/master_receiving_2020")
    df = df.query("Pos == 'te' | Pos == 'TE'")
    clean_dataframes(df)
    save_df_to_csv(df, "football/2020/receiving_stats/te_receiving_2020")
def get_WRs():
    df = load_csv_file("football/2020/receiving_stats/master_receiving_2020")
    df = df.query("Pos == 'wr' | Pos == 'WR'")
    clean_dataframes(df)
    save_df_to_csv(df, "football/2020/receiving_stats/wr_receiving_2020")

def get_Rbs():
    df = load_csv_file("football/2020/rb_stats/master_rushing_2020")
    df = df.query("Pos == 'rb' | Pos == 'RB'")
    clean_dataframes(df)
    save_df_to_csv(df, "football/2020/rb_stats/rb_rushing_2020")

def csv_to_excel(filename):
    df = load_csv_file(filename)
    df.to_excel(resources_path + filename +  ".xlsx")


# def get_gameStats

############# To recreate the master csv's with advanced/standard, and snap count ############
# create_master_csv(2020,"qb")
# csv_to_excel("football/2020/position_grades/rb_grade")
# csv_to_excel("football/2020/position_grades/te_grade")
# csv_to_excel("football/2020/position_grades/wr_grades")
# csv_to_excel("football/2020/position_grades/qb_grade")
#######################################################################################################