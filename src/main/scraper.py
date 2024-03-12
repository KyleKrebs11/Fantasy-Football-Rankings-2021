# -*- coding: utf-8 -*-

import re
import time
from bs4 import BeautifulSoup
from bs4 import Comment
import requests
import file_maker

def parse_url(url, tableId):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")

    if len(tableId) >0 :
        table = soup.find_all('table', id=tableId)
        print(table)
    else :
        table = soup.find_all('table')
    if len(table)>0:
        return [(1, parse_html_table(t)) for t in table]
    else:
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        rx = re.compile(r'<table.+?id="'+ tableId +'".+?>[\s\S]+?</table>')
        for comment in comments:
            try:
                found = rx.search(comment.string).group(0)
                soup2 = BeautifulSoup(found)
                table = soup2.find_all('table')
                if len(table)>0:
                    return [(1, parse_html_table(t)) for t in table]
            except:
                pass

def parse_html_table(table):
    n_columns = 0
    n_rows = 0

    c_names = []

    for col in table.find_all('th'):
        c_names.append(col.get_text())

    for row in table.find_all('tr'):
        # Determine the number of rows in the table
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            if n_columns == 0:
                # Set the number of columns for our table
                n_columns = len(td_tags)


    # Safeguard on Column Titles
    if len(c_names) > 0 and len(c_names) < n_columns:
        raise Exception("Column titles do not match the number of columns")

    c_names = c_names[1:n_columns+1]
    data = []
    data.append(c_names)
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        r = []
        for column in columns:
            r.append(column.get_text())
        if(len(r)>0):
            data.append(r)
    return data

def crawl(url,id, filename):
    table = parse_url(url, id)
    t = table[0][1]
    file_maker.save_table_to_csv(t, filename)

def test(start, end):
    for year in range(start, end +1):
        for week in range (1,2):
            crawl(
        "https://stathead.com/football/drive_finder.cgi?request=1&year_min=" + str(year) + "&year_max=" + str(year) + " &game_type=R&exclude_kneels=1&drive_st_gtlt=lt&drive_st_own_opp=Own&drive_end_gtlt=lt&drive_end_own_opp=Own&drive_num_gtlt=gt&minutes_max=15&seconds_max=0&minutes_min=0&seconds_min=0&game_num_min=0&game_num_max=99&week_num_min=" + str(week) + "&week_num_max=" + str(week),
        "drive_results", "test_" + str(week) )


start = time.time()
# crawl("https://www.basketball-reference.com/leagues/NBA_2021_totals.html#totals_stats::pts","", "totals_2021")
# crawl("https://www.basketball-reference.com/leagues/NBA_2007_totals.html#totals_stats::pts","", "totals_2007")
# crawl("https://www.ftnfantasy.com/air-yards", "", "all_wr_stats")
# crawl("https://www.pro-football-reference.com/years/2020/passing_advanced.htm", "advanced_passing", "2020_advanced_passing")
# crawl("https://www.espn.com/nfl/stats/player/_/table/passing/sort/passingYards/dir/desc","")
# Change the above url to any webpage with a table on the screen and this will get its data
# crawl("https://stathead.com/football/drive_finder.cgi?request=1&order_by_asc=0&order_by=play_count&year_min=2021&year_max=2021&game_type=R&exclude_kneels=1&drive_st_gtlt=lt&drive_st_own_opp=Own&drive_end_gtlt=lt&drive_end_own_opp=Own&drive_num_gtlt=gt&minutes_max=15&seconds_max=0&minutes_min=0&seconds_min=0&game_num_min=0&game_num_max=99&week_num_min=1&week_num_max=1", "drive_results", "test")
test(2021,2021)
end = time.time()
print(end-start)

