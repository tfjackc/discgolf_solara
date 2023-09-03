import requests
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

round1 = "https://www.pdga.com/apps/tournament/live/event?view=Scores&eventId=68748&round=1&division=MPO"
round2 = "https://www.pdga.com/apps/tournament/live/event?view=Scores&eventId=68748&round=2&division=MPO"
round3 = "https://www.pdga.com/apps/tournament/live/event?view=Scores&eventId=68748&round=3&division=MPO"
round4 = "https://www.pdga.com/apps/tournament/live/event?view=Scores&eventId=68748&round=4&division=MPO"

pdgapage = "https://www.pdga.com/tour/event/68748"

# tourney = [round1, round2, round3, round4]
#
# response = requests.get(round1)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# print(soup.find(attrs = {'id': 'pool-A'}))

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

df_draft_board = pd.read_excel("draft_board.xlsx")
df_draft_board['Player'] = df_draft_board['Player'].str.rstrip('0123456789')
print(df_draft_board)