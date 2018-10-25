import sys
import csv
import json
import pandas as pd
import numpy as np


def main():
    awards_data = pd.read_csv("database.csv")
    awards_data.loc[awards_data['Winner'] == 1.0, 'Winner'] = 2.0
    awards_data['Winner'] = awards_data['Winner'].replace(np.nan,1.0)

    actor_awards = pd.DataFrame(columns = ['Actor','Nominations','Wins','Sum'])
    act_data = awards_data.loc[awards_data['Award'].isin(['Actress','Actor','Actor in a Supporting Role',
                                                         'Actress in a Supporting Role', 'Actor in a Lead Role',
                                                         'Actress in a Lead Role'])]
    actors = act_data.groupby(by = "Name")

    for actor,group in actors:
        new_row = pd.DataFrame({'Actor': actor,'Nominations': (group.Winner == 1.0).sum() ,
                                'Wins': (group.Winner == 2.0).sum(),'Sum': sum(group.Winner)}, index = [1])
        actor_awards = pd.concat([actor_awards,new_row],ignore_index = True )

    actor_awards.to_csv('actor_awards.csv',columns = ['Actor','Nominations','Wins','Sum'])

    film_awards = pd.DataFrame(columns=['Film', 'Nominations', 'Wins', 'Sum'])
    films = awards_data.groupby(by = "Film")

    for film,group in films:
        new_row = pd.DataFrame({'Film': film, 'Nominations': (group.Winner == 1.0).sum(),
                                'Wins': (group.Winner == 2.0).sum(), 'Sum': sum(group.Winner)}, index=[1])
        film_awards = pd.concat([film_awards, new_row], ignore_index=True)

    film_awards.to_csv('film_awards.csv', columns=['Film', 'Nominations', 'Wins', 'Sum'])

if __name__ == "__main__":
	sys.exit(main())