import sys
import csv
import json
import datetime
import pandas as pd
import numpy as np
from easymoney.money import EasyPeasy

ep = EasyPeasy()


def inflation_budget(row):
    return ep.normalize(amount=float(row['budget']), region="US", from_year=row['year'], to_year="latest",
                        base_currency="USD", pretty_print=False)


def inflation_revenue(row):
    return ep.normalize(amount=float(row['revenue']), region="US", from_year=row['year'], to_year="latest",
                        base_currency="USD", pretty_print=False)

def revenue_budget_ratio(row):
    return row["revenue"]/row["budget"]


def get_genres(row):
    parsed_genres = json.loads(row['genres'])
    act_adv = 0
    fantasy_scifi = 0
    family_animation = 0
    drama = 0
    comedy = 0
    thril_crime = 0
    doc = 0
    for genre in parsed_genres:
        if genre["name"] == 'Action' or genre["name"] == 'Adventure':
            act_adv = 1
        elif genre["name"] == 'Fantasy' or genre["name"] == 'Science Fiction':
            fantasy_scifi = 1
        elif genre["name"] == 'Animation' or genre["name"] == 'Family':
            family_animation = 1
        elif genre["name"] == 'Drama':
            drama = 1
        elif genre["name"] == 'Comedy':
            comedy = 1
        elif genre["name"] == 'Thriller' or genre["name"] == 'Crime':
            thril_crime = 1
        elif genre["name"] == 'Documentary':
            doc = 1
    return pd.Series([act_adv, fantasy_scifi, family_animation, drama, comedy, thril_crime, doc])


def get_cast(row):
    parsed_cast = json.loads(row['cast'])
    cast_list = []
    count = 0
    for actor in parsed_cast:
        if count >= 5:
            break
        count += 1
        gendercheck = int(actor["gender"])
        if gendercheck == 2:
            cast_list.append(0)
        else:
            cast_list.append(1)

    if len(cast_list) < 5:
        while len(cast_list) < 5:
            cast_list.append('NA')
        actor_sum = 'NA'
        weighted_actor_sum = 'NA'
    else:
        actor_sum = cast_list[0] + cast_list[1] + cast_list[2] + cast_list[3] + cast_list[4]
        weighted_actor_sum = 10 * cast_list[0] + 8 * cast_list[1] + 6 * cast_list[2] + 5 * cast_list[3] + 5 * cast_list[4]

    cast_list.append(actor_sum)
    cast_list.append(weighted_actor_sum)

    return pd.Series(cast_list)


def main():
    credits_data = pd.read_csv("tmdb_5000_credits.csv")
    movie_data = pd.read_csv("tmdb_5000_movies.csv")
    actor_awards = pd.read_csv("actor_awards.csv")
    film_awards = pd.read_csv("film_awards.csv")
    filename1 = "Analysis.csv"
    filename2 = "AnalysisBinned.csv"

    # col = ['ID','Title','Budget','Revenue','Revenue/Budget','Vote_Average','Film_Awards','Actor1','Actor2',
    #     'Actor3','Actor4','Actor5','Acting_Awards','Actor_Sum','Weighted_Actor_Sum']
    # final_data = pd.DataFrame(columns = col)
    # final_data_binned = pd.DataFrame(columns = col)

    credits_data = credits_data[['id','title','cast','crew']]
    movie_data = pd.merge(movie_data, credits_data, on = 'title', suffixes = ('', '_new'))
    movie_data = movie_data.set_index('title', drop=False)
    movie_data = movie_data.drop(['homepage', 'original_title', 'keywords', 'overview', 'production_companies', 'production_countries',
         'runtime', 'popularity','spoken_languages', 'status', 'tagline', 'vote_count','id_new','crew','id'], axis=1)

    english = movie_data['original_language'] == "en"
    movie_data = movie_data[english]

    movie_data['release_date'] = pd.to_datetime(movie_data['release_date'], format = '%Y-%m-%d')
    movie_data['year'] = movie_data['release_date'].dt.year
    recent = movie_data['year'] >= 1970
    before2010 = movie_data['year'] <= 2010
    movie_data = movie_data[recent & before2010]

    budget = movie_data['budget'] > 0
    movie_data = movie_data[budget]
    movie_data['budget'] = movie_data.apply(inflation_budget, axis = 1)

    movie_data['revenue'] = movie_data.apply(inflation_revenue, axis = 1)
    rev_min = movie_data['revenue'] >= 10000000
    movie_data = movie_data[rev_min]
    movie_data['Revenue_to_Budget'] = movie_data.apply(revenue_budget_ratio,axis = 1)

    movie_data[['Action_Adventure','Fantasy_SciFi','Family_Animation','Drama','Comedy','Thriller_Crime','Documentary']] = \
        movie_data.apply(get_genres,axis=1)
    filter_genres = movie_data["Action_Adventure"] | movie_data['Fantasy_SciFi'] | movie_data['Family_Animation'] | \
                    movie_data['Drama'] | movie_data['Comedy'] | movie_data['Thriller_Crime']
    not_doc = movie_data['Documentary'] == 0
    movie_data = movie_data[filter_genres & not_doc]
    movie_data = movie_data.drop(['genres','Documentary','original_language','release_date','year'], axis=1)

    movie_data[['Actor1','Actor2','Actor3','Actor4','Actor5','Actor_Sum','Weighted_Actor_Sum']] = movie_data.apply(get_cast,axis=1)
    enough_cast = movie_data['Actor_Sum'] != "NA"
    movie_data = movie_data[enough_cast]
    movie_data = movie_data.drop('cast',axis = 1)

    print(movie_data.head())
    print(movie_data.keys())
    print(movie_data.loc['Avatar'])
    print(len(movie_data.index))


if __name__ == "__main__":
	sys.exit(main())