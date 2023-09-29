import solara.lab
from solara import *
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import dataclasses
from typing import Any, Dict, Optional, cast
import plotly.express as px

web_data = pd.read_csv("final_df.csv")
wddf = web_data.drop(columns='Unnamed: 0')
wddf.columns = wddf.columns.str.replace('cur_', '')
wddf = wddf.rename(columns={"udisc_name": "Name", "pdga_no": "PDGA#", 'rating':'Rating', 'udisc_rank':'UDisc Rank', 'udisc_index':'UDisc Index','pdga_rank':'PDGA Rank'})
wddf = wddf[['Name', 'PDGA#','Rating','UDisc Rank', 'PDGA Rank']]
wddf[['PDGA#', 'Rating', 'UDisc Rank', 'PDGA Rank']] = wddf[['PDGA#', 'Rating', 'UDisc Rank', 'PDGA Rank']].fillna(0)
wddf[['PDGA#', 'Rating', 'UDisc Rank', 'PDGA Rank']] = wddf[['PDGA#', 'Rating', 'UDisc Rank', 'PDGA Rank']].astype(int)
#board_data = pd.read_csv("cleaned_scores.csv")
#board_data['Player'] = board_data['Player'].str.rstrip('0123456789')
#bd = board_data.drop(columns='Unnamed: 0')
#print('wddf')
#print(wddf)
#print('board_data')
#print(bd)
from typing import Optional, cast
import pandas as pd
import solara.express as solara_px  # similar to plotly express, but comes with cross filters

@dataclasses.dataclass(frozen=True)
class PlayerList:
    name:str
    pdga_num:int
    rating:int
    udisc_rank:int
    pdga_rank:int

player_dict = {}
pdf = pd.DataFrame()
@solara.component
def Page():
    css = """
        .v-sheet.v-sheet--tile.theme--dark.v-toolbar.v-app-bar.v-app-bar--clipped.v-app-bar--fixed.primary {
            background-color: #000000 !important;
            height: 100px !important;
        }
        
        .v-toolbar__content {
            margin: 20px!important;    
        }
        
        .v-content__wrap{
            padding-left: 20px !important;
        }
        
        .v-navigation-drawer__content {
        
            margin-top: 25px;
        }
        
        .solara-data-table__viewport {
            margin-top: 50px !important;
        }
        
        #add-players {
            margin-left: 50px;
        }
        
        code {
            font-size: 25px;
        }
        
        .v-btn.v-btn--contained.theme--light.v-size--default.secondary {
            width: 150px;
        }
        """
    # cell, set_cell = solara.use_state(cast(Dict[str, Any], {}))


    #df_row, set_df_row = solara.use_state(cast(Dict[str, Any], {}))
    df_row, set_df_row = solara.use_state("")
    name, set_name = solara.use_state("")
    pdga_num, set_pdga_num = solara.use_state(0)
    rating, set_rating = solara.use_state(0)
    udisc_rank, set_udisc_rank = solara.use_state(0)
    pdga_rank, set_pdga_rank = solara.use_state(0)
    idselect = use_reactive(0)
    df_idselect = use_reactive(0)

    selected_players = use_reactive([
        PlayerList("", "", "", "", "")
    ])

    plot_data, set_plot_data = use_state(cast([Any], None))


    # wddf = wddf[['Name', 'PDGA#','Rating','UDisc Rank', 'PDGA Rank']]
    def on_action_cell(column, row_index):
        try:
            set_df_row(wddf.iloc[row_index]['Name'])
            set_name(wddf.iloc[row_index]['Name'])
            set_pdga_num(wddf.iloc[row_index]['PDGA#'])
            set_rating(wddf.iloc[row_index]['Rating'])
            set_udisc_rank(wddf.iloc[row_index]['UDisc Rank'])
            set_pdga_rank(wddf.iloc[row_index]['PDGA Rank'])
            idselect.value = row_index

            player_dict[idselect.value] = PlayerList(
                name,
                int(pdga_num),
                int(rating),
                int(udisc_rank),
                int(pdga_rank)
            )
            print("on action cell...")
            selected_players.value = list(player_dict.values())
        except ValueError:
            # Handle the ValueError, e.g., by displaying an error message or logging it
            print("Invalid input. Please enter valid numeric values for PDGA#, Rating, UDisc Rank, and PDGA Rank.")

    def updatedata():
        try:
            newdata = PlayerList(
                name,
                int(pdga_num),
                int(rating),
                int(udisc_rank),
                int(pdga_rank)
            )

            selected_players.value = [*selected_players.value, newdata]

            set_name("")
            set_rating("")
            set_pdga_num("")
            set_udisc_rank("")
            set_pdga_rank("")

        except Exception as e:
            # Handle the ValueError, e.g., by displaying an error message or logging it
            print(e)

    def drop_player(column, row_index):
        try:
            set_df_row(wddf.iloc[row_index]['Name'])
            set_name(wddf.iloc[row_index]['Name'])
            set_pdga_num(wddf.iloc[row_index]['PDGA#'])
            set_rating(wddf.iloc[row_index]['Rating'])
            set_udisc_rank(wddf.iloc[row_index]['UDisc Rank'])
            set_pdga_rank(wddf.iloc[row_index]['PDGA Rank'])
            idselect.value = row_index

            player_dict[idselect.value] = PlayerList(
                name,
                int(pdga_num),
                int(rating),
                int(udisc_rank),
                int(pdga_rank)
            )
            print("on action cell...")
            selected_players.value = list(player_dict.values())
        except ValueError:
            # Handle the ValueError, e.g., by displaying an error message or logging it
            print("Invalid input. Please enter valid numeric values for PDGA#, Rating, UDisc Rank, and PDGA Rank.")
    def dropdata():
        if idselect.value < len(selected_players.value):

            #if df_idselect.value < len(selected_players.value):
            print(f"clicked {df_idselect.value}")
            print(f"dropping {len(selected_players.value)}")
            mydeldata = selected_players.value.copy()
            mydeldata.pop(df_idselect.value)
            selected_players.value = mydeldata
            set_name("")
            set_rating("")
            set_pdga_num("")
            set_udisc_rank("")
            set_pdga_rank("")

    pdf = pd.DataFrame.from_records([dataclasses.asdict(x) for x in selected_players.value])
    print(pdf.dtypes)
    #pdf['avg'] = pdf[['udisc_rank', 'pdga_rank']].mean(axis=1)
    fig = px.scatter(pdf.iloc[1:], x="udisc_rank", y="name")
    set_plot_data(fig)

    #def create_plot():
        #pdf['rank_avg'] = pdf[[int('udisc_rank'), int('pdga_rank')]].mean()


                            #on_selection=set_selection_data, on_click=set_click_data, on_hover=set_hover_data,
            #on_unhover=set_unhover_data, on_deselect=set_deselect_data)


    cell_actions = [
        solara.CellAction(icon="mdi-white-balance-sunny", name="Add player to the board", on_click=on_action_cell)]

    drop_cell_action = [solara.CellAction(icon="mdi-database", name="Drop player", on_click=drop_player)]

    with solara.Column() as main:
        if css:
            solara.Style(css)
        with solara.AppBarTitle():
            solara.Markdown("# <div style='color: #ffffff; margin: 10px !important; padding-top: 20px; padding-bottom: 20px; font-size: 80px;'>Disc Golf Statistics 2023</div>")

        solara.provide_cross_filter()
        with solara.Sidebar():

            solara.DataTable(wddf, cell_actions=cell_actions)

        with solara.Card():
            solara.Markdown(
                f"""
                    # Player: {name} 
                    # Rating: {rating} 
                    # UDisc Rank: {udisc_rank} 
                    # PDGA Rank: {pdga_rank}
                """
            )
            with solara.Column():
                with solara.Row():

                    solara.Button("Add Player", color='primary',
                                  on_click=updatedata
                                  )
                    solara.Button("Drop Player", color='secondary',
                                  on_click=dropdata
                                  )
                solara.DataFrame(pdf.iloc[1:], cell_actions=drop_cell_action, items_per_page=25)

                # solara.Button("Run Analysis", color='secondary',
                #               on_click=create_plot()
                #               )
                solara.FigurePlotly(plot_data)
                # fig = px.scatter(pdf.iloc[1:], x="sepal_width", y="sepal_length", color="species")
                # solara.FigurePlotly(
                #     fig, on_selection=set_selection_data, on_click=set_click_data, on_hover=set_hover_data,
                #     on_unhover=set_unhover_data, on_deselect=set_deselect_data
                # )

                #solara.Select("Select Players for Stat Comparison...", wddf['Name'].values.tolist())
    return main








