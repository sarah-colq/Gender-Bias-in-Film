import sys 
import csv 
import json
import pandas as pd 
import matplotlib.pyplot as plt 
from easymoney.money import EasyPeasy

def get_cast(parsed_cast,awards):
  ep = EasyPeasy() 
  cast_list = [] 
  count = 0  
  awardscount = 0 
  for actor in parsed_cast: 
    if count >= 5: 
      break
    count += 1 
    if actor["name"] in awards.keys(): 
      awardscount += awards[actor["name"]]
    gendercheck = int(actor["gender"])
    if gendercheck == 2: 
      cast_list.append(0)
    else :  
      cast_list.append(1) 
  
  weight_actor_sum = 0 
  actor_sum = 0 
  
  if len(cast_list) < 5: 
    while len(cast_list) < 5: 
      cast_list.append('NA')
    actor_sum = 0 
    weighted_actor_sum = 0 
  else: 
    actor_sum = cast_list[0] + cast_list[1] + cast_list[2] + cast_list[3] + cast_list[4]
    weight_actor_sum = 10*cast_list[0] + 8*cast_list[1] + 6*cast_list[2] + 5*cast_list[3] + 5*cast_list[4]
    
  cast_list.append(actor_sum)
  cast_list.append(weight_actor_sum)
  cast_list.append(binActingAwards(awardscount))
  return cast_list
  
def actors_awards_list(file): 
  
  csv3_init = open(file,encoding='utf-8')
  awardsCSV = csv.reader(csv3_init) 
  header = next(awardsCSV)
  name_index = header.index('Name')
  award_index = header.index('Award')
  winner_index = header.index('Winner')
  actorscount = {}
  for row in awardsCSV:
    if row[award_index][:3] == 'Act': 
      if row[name_index] not in actorscount.keys(): 
        if row[winner_index] == '1': 
          actorscount[row[name_index]] = 1
        else: 
          actorscount[row[name_index]] = 1 
      else: 
        if row[winner_index] == '1': 
          actorscount[row[name_index]] += 1
        else: 
          actorscount[row[name_index]] += 1 
          
  csv3_init.close()
  return actorscount 
       
def film_awards_list(file): 
  csv3_init = open(file,encoding='utf-8')
  awardsCSV = csv.reader(csv3_init) 
  header = next(awardsCSV)
  film_index = header.index('Film')
  winner_index = header.index('Winner')
  name_index = header.index('Name')
  award_index = header.index('Award')
  filmcount = {}
  for row in awardsCSV:
    if row[award_index][:3] == 'Act': 
      index = film_index 
    else: 
      index = name_index
    input = row[index].strip()
    if input not in filmcount.keys(): 
      if row[winner_index] is not None: 
        filmcount[input] = 1
      else: 
        filmcount[input] = 1 
    else: 
      if row[winner_index] is not None: 
        filmcount[input] += 1
      else: 
        filmcount[input] += 1 
          
  csv3_init.close()
  return filmcount
    
def binBudget(budget): 
  if budget <= 35000000: 
    budget_bin = 'Under 35 mil' 
  elif budget <= 120000000: 
    budget_bin = '35mil to 120mil'   
  else: 
    budget_bin = '>= 120mil' 
  return (budget_bin) 
  
def binFilmAwards(award_num):
  if award_num < 3: 
    award_bin = '0 to 2' 
  else:
    award_bin = '>=3' 
  return(award_bin) 

def binRevenue(revenue):

  if revenue <= 80000000: 
    revenue_bin = '10 to 80 mil' 
  elif revenue <= 200000000: 
    revenue_bin = '120mil to 200mil'     
  else: 
    revenue_bin = '>= 200mil' 
  return (revenue_bin) 

def binActingAwards(award_num): 
  if award_num < 4: 
    award_bin = '0 to 3' 
  else:
    award_bin = '>=4' 
  return(award_bin) 

def binRatio(ratio): 
  if ratio < 1: 
    ratio_bin = '<1' 
  elif ratio <3: 
    ratio_bin ='1 to 3' 
  elif ratio < 6: 
    ratio_bin = '3 to 6' 
  else: 
    ratio_bin = '>6'
  return(ratio_bin) 
  
def genresParse(string): 
  genre_list = [0,0,0,0,0,0]
  parsed_genres = json.loads(string) 
  for genre in parsed_genres: 
    if genre["name"] == 'Action' or genre["name"] == 	'Adventure': 
      genre_list[0] = 1 
    elif  genre["name"] == 'Fantasy'or genre["name"] =='Science Fiction': 
      genre_list[1] = 1
    elif genre["name"] == 'Animation' or genre["name"] ==	'Family': 
      genre_list[2] = 1 
    elif genre["name"] == 'Drama': 
      genre_list[3] = 1 
    elif genre["name"] == 'Comedy': 
      genre_list[4] = 1 
    elif genre["name"] == 'Thriller' or genre["name"] == 'Crime': 
      genre_list[5] = 1 
    if genre["name"] == 'Documentary': 
      genre_list = [-1,-1] 
      break 
  if max(genre_list) == 0: 
    genre_list = [-1,-1]
  return(genre_list)
      
def main(): 
  file1 = "tmdb_5000_movies.csv"
  file2 = "tmdb_5000_credits.csv"
  file3 = "database.csv"
  csv1_init = open(file1,encoding='utf-8')
  csv2_init = open(file2,encoding='utf-8')
  moviesCSV = csv.reader(csv1_init)
  creditsCSV = csv.reader(csv2_init) 
  
  ep = EasyPeasy()
  
  acting_awards = actors_awards_list(file3)  
  film_awards = film_awards_list(file3)
  
  movies_header = next(moviesCSV) 
  title_index = movies_header.index("original_title")
  budget_index = movies_header.index("budget") 
  genre_index = movies_header.index("genres")
  id_index = movies_header.index("id") 
  language_index = movies_header.index("original_language")
  popularity_index = movies_header.index("popularity") 
  release_date_index = movies_header.index("release_date")
  revenue_index = movies_header.index("revenue") 
  vote_average_index = movies_header.index("vote_average")
  vote_count_index = movies_header.index("vote_count")

  newlist = []  
  newlist.append(['"ID"','Title','Budget','Revenue','Revenue/Budget','Vote_Average','FilmAwards','Action/Adventure','Fantasy/SciFi','Animation/Family','Drama','Comedy','Thriller/Crime','Actor1','Actor2','Actor3','Actor4','Actor5','ActorSum','WeightedSum','ActingAwards'])
  
  headings = newlist[0] 
  ids = [] 
  
  for movie in moviesCSV: 
    if movie[0] == '': 
      break 
    date = int(movie[release_date_index][:4])
    language = movie[language_index] 
    budget = float(movie[budget_index])
    if 1970 <= date <= 2010 and language == 'en' and budget > 0: 
      revenue = ep.normalize(amount = float(movie[revenue_index]), region = "US", from_year = date, to_year = "latest", base_currency = "USD",pretty_print = False)
      if revenue >= 10000000:  
        budget = ep.normalize(amount = float(movie[budget_index]), region = "US", from_year = date, to_year = "latest", base_currency = "USD",pretty_print = False)
        ratio = revenue/budget
        entry = [movie[id_index],movie[title_index],binBudget(budget),binRevenue(revenue),binRatio(ratio),movie[vote_average_index]]
        if movie[title_index] in film_awards.keys(): 
          entry.append(binFilmAwards(film_awards[movie[title_index]])) 
        else: 
          entry.append('0 to 2')
        genres = genresParse(movie[genre_index]) 
        entry.extend(genres)
        if max(genres) != -1:
          newlist.append(entry) 
          ids.append(movie[id_index])

  credits_header = next(creditsCSV) 
  cast_index = credits_header.index('cast')
  creditsid_index = credits_header.index('movie_id') 
  creditstitle_index = credits_header.index('title')
  count = 0 
  
  for movie in creditsCSV: 
    if movie[creditsid_index] in ids:   
      count += 1
      parsed_cast = json.loads(movie[cast_index]) 
      newlist[count].extend(get_cast(parsed_cast,acting_awards)) 

  with open("AnalysisNew.csv","w",newline ="",encoding = "utf-8") as f:
    csvfinal = csv.writer(f) 
    csvfinal.writerows(newlist)

  csv1_init.close()
  csv2_init.close()  
  
if __name__ == "__main__":
	sys.exit(main())