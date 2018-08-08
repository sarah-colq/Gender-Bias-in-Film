import sys 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def main(): 
  # sns.set()
  plt.style.use('ggplot')
  df = pd.read_csv("AnalysisNew.csv",encoding = 'latin1')
  # print(df.info())
  # df_num_female_top2 = df.groupby(['Actor1','Actor2'])
  # print(df['ActorSum'].corr(df['Vote_Average']))
  # df.plot(x='ActorSum', y='Vote_Average', style='o')
  # plt.ylabel('Average Rating')
  # plt.xlabel('Number of Women in Top 5')
  # plt.title('Number of Women in Top 5 vs Vote_Average')
  # plt.show()
  
  # df.hist(column = 'Number of Women in the Top 5', label = 'Distribution of the number of women in main cast')
  # plt.show()
  
  # df.plot(x='WeightedSum',y='Vote_Average',style='o')
  # plt.show()

  # for name,group in df_num_female_top2:
    # plt.hist(group['Vote_Average'], label=str(name))
  
  # plt.legend(loc='upper right')
  # plt.title('Distribution of Movie Scores by Top 2 Actors')
  # plt.show()

  genres = ['Action/Adventure', 'Fantasy/SciFi', 'Animation/Family','Drama','Comedy','Thriller/Crime'] 
  
  # for genre in genres: 
    #df_num_genre = df.groupby([genre,'ActorSum'])
    # for name, group in df_num_genre: 
      # if name[0] == 1: 
        # plt.hist(group['Vote_Average'], bins = 50, label = str(name[1])) 
    # plt.title('Grouping by Genre: ' + genre)
    # plt.legend(loc = 'upper right') 
    # plt.show()
    
  for genre in genres:  
    df_group_genre = df.groupby(['Budget','FilmAwards','ActingAwards',genre,'Revenue','Revenue/Budget']) 
    for name,group in df_group_genre: 
      if name[3] == 1: 
        t = 'Budget: ' + name[0] + ' ,Revenue: ' + name[4] + ', FilmAwards: ' + name[1] + ', Acting Awards: ' + name[2] + ' in ' + genre + 'Revenue/Budget' + name[5]
        print(t)
        print('ActorSum') 
        x='ActorSum'
        y='Vote_Average'
        group.plot(x,y,style = 'o',legend = None) 
        plt.xlabel('Number of Women in Top Four Billed Actors')
        plt.ylabel('Average Viewer Rating')
        plt.show() 
        print('WeightedSum') 
        x='WeightedSum'
        y='Vote_Average'
        group.plot(x,y,style = 'o',legend = None) 
        plt.xlabel('Weighted Sum of Women in Top Four Billed Actors')
        plt.ylabel('Average Viewer Rating')
        plt.show()
  
  
  # # df_num_female = df.groupby(['ActorSum'])
  
  # for name,group in df_num_female: 
    # plt.hist(group['Vote_Average']) 
    # if 
    
if __name__ == "__main__":
	sys.exit(main())