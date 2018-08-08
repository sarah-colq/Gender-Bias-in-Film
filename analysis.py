import sys 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main(): 
  plt.style.use('ggplot')
  df = pd.read_csv("AnalysisNew.csv", encoding = 'latin1')
 
  genres = ['Action/Adventure', 'Fantasy/SciFi', 'Animation/Family','Drama','Comedy','Thriller/Crime'] 
    
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
    
if __name__ == "__main__":
	sys.exit(main())
