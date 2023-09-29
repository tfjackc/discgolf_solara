import solara
import solara.lab
from solara import *
import requests
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import dataclasses
from typing import Any, Dict, Optional, cast
import plotly
from solara.website.utils import apidoc

# round1 = "https://www.pdga.com/apps/tournament/live/event?view=Scores&eventId=68748&round=1&division=MPO"
# round2 = "https://www.pdga.com/apps/tournament/live/event?view=Scores&eventId=68748&round=2&division=MPO"
# round3 = "https://www.pdga.com/apps/tournament/live/event?view=Scores&eventId=68748&round=3&division=MPO"
# round4 = "https://www.pdga.com/apps/tournament/live/event?view=Scores&eventId=68748&round=4&division=MPO"

# worlds data ----------------------------------
pdgapage = "https://www.pdga.com/tour/event/68748"
r = requests.get(pdgapage)
soup = BeautifulSoup(r.content, 'html5lib')

table = soup.find('div', attrs= {'class' : 'leaderboard singles mode-live'})

df_data = []
if table is not None:
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 0:
            place = cols[0].text.strip()
            pool = cols[1].text.strip()
            event = cols[2].text.strip()
            player = cols[3].text.strip()
            pdga_number = cols[4].text.strip()
            rating = cols[5].text.strip()
            under_par = cols[6].text.strip()
            round1_score = cols[7].text.strip()
            round1_rating = cols[8].text.strip()
            round2_score = cols[9].text.strip()
            round2_rating = cols[10].text.strip()
            round3_score = cols[11].text.strip()
            round3_rating = cols[12].text.strip()
            round4_score = cols[13].text.strip()
            round4_rating = cols[14].text.strip()
            total = cols[15].text.strip()

            df_data.append([place, pool, event, player, pdga_number, rating, under_par,
                         round1_score, round1_rating, round2_score, round2_rating,
                         round3_score, round3_rating, round4_score, round4_rating, total])

    df = pd.DataFrame(df_data, columns=['Place', 'Pool', 'Event', 'Player', 'PDGA Number', 'Rating',
                                     'Under Par', 'Round 1 Score', 'Round 1 Rating', 'Round 2 Score',
                                     'Round 2 Rating', 'Round 3 Score', 'Round 3 Rating', 'Round 4 Score',
                                     'Round 4 Rating', 'Total'])
    #print(df.head(15))
    #df.to_csv("worlds.csv")
else:
    print("Table element not found.")
# worlds data ----------------------------------

# copy/pasted excel sheet from draft board------
df_draft_board = pd.read_excel("draft_board.xlsx")
df_draft_board['Player'] = df_draft_board['Player'].str.rstrip('0123456789')
dude_list = list(df_draft_board['Dude'].unique())
select_dude = solara.reactive([dude_list[0]])
# copy/pasted excel sheet from draft board------

# potential draft board CRUD application tab-----


# potential draft board CRUD application tab-----

@dataclasses.dataclass(frozen=True)
class FakeData:
    name:str
    age:int

mysample = pd.DataFrame()

@solara.component
def Page():
    # html = f"""
    # <h1>Hello World</h1>
    # <ul>
    #     <li>Hello World</li>
    # </ul>
    # """

    name, set_name = solara.use_state("")
    age, set_age = solara.use_state(0)
    mycell, set_mycell = solara.use_state(cast(Dict[str, Any], {}))
    idselect = use_reactive(0)

    #print(mycell)
    #print(set_mycell)

    mydata = use_reactive([
        FakeData("jul", 12),
        FakeData("dw", 34),
        FakeData("gr", 54)
    ])
    def youactioncell(column, row_index):
        print("firing you action cell")
        # click a dataframe row, then get data returned in another component
        set_mycell(dict(column=column, row_index=row_index))
        for i, x in enumerate(mydata.value):
            if i == row_index:
                set_name(x.name)
                set_age(x.age)
                idselect.value = row_index

    def updatedata():
        myeditdata = mydata.value.copy()
        for i, x in enumerate(mydata.value):
            if i == idselect.value:
                myeditdata[idselect.value] = FakeData(name, age)
                print(x)

        mydata.value = myeditdata
        set_name("")
        set_age("")

    def deletedata():
        if idselect.value < len(mydata.value):
            mydeldata = mydata.value.copy()
            mydeldata.pop(idselect.value)
            mydata.value = mydeldata
            set_name("")
            set_age(0)


    def addnewdata():
        # add fake data to the table
        newdata = FakeData(name, int(age))
        # and push to mydata.value
        mydata.value = [*mydata.value, newdata]
        # and clear input
        set_name("")
        set_age("")

    mycellactions = [solara.CellAction(icon="mdi-white-balance-sunny", name="Select Values", on_click=youactioncell)]
    mysample = pd.DataFrame.from_records([dataclasses.asdict(x) for x in mydata.value])
    #print(mysample)

    solara.provide_cross_filter()
    with solara.Column() as main:
        #solara.HTML(tag='div', unsafe_innerHTML=html)
        with solara.AppBarTitle(): #background_color="#084685", dark=True
            solara.Text("Disc Golf Stats 2023")

        with solara.lab.Tabs(): #background_color="#084685", dark=True
            with solara.lab.Tab("Live Results", icon_name="mdi-chart-line"):


                with solara.Card():
                    Markdown("Table")
                    InputText(label="name",value=name,
                              on_value=set_name)
                    InputText(label="age",value=age,
                              on_value=set_age)

                    with Row(justify="space-around"):
                        Button("edit",color='primary',
                               on_click=updatedata
                               )
                        Button("add new", color='green',
                               on_click=addnewdata
                               )
                        Button("delete", color='secondary',
                               on_click=deletedata
                               )
                    DataFrame(mysample,cell_actions=mycellactions)

                    filtered_df = df[['Place','Player', 'PDGA Number', 'Rating',
                                     'Under Par', 'Round 1 Score', 'Round 1 Rating', 'Round 2 Score',
                                     'Round 2 Rating', 'Round 3 Score', 'Round 3 Rating', 'Round 4 Score',
                                     'Round 4 Rating', 'Total']]
                    solara.DataFrame(filtered_df, items_per_page=25)

        with solara.Sidebar():
            solara.CrossFilterReport(df_draft_board)
            solara.CrossFilterSelect(df_draft_board, "Dude")
            solara.CrossFilterDataFrame(df_draft_board, items_per_page=54)

            #solara.DataFrame(df_draft_board, items_per_page=54)

    return main



