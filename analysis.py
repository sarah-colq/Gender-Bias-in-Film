import sys 
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def main(): 
 
  plt.style.use('ggplot')
  df = pd.read_csv("AnalysisNew.csv",encoding = 'latin1')

  genres = ['Action/Adventure', 'Fantasy/SciFi', 'Animation/Family','Drama','Comedy','Thriller/Crime'] 
  
  for genre in genres:  
    filtered = df.groupby(['Budget','FilmAwards','ActingAwards',genre,'Revenue','Revenue/Budget']).filter(lambda x: len(x) >= 15)  
    df_group_genre = filtered.groupby(['Budget','FilmAwards','ActingAwards',genre,'Revenue','Revenue/Budget'])
    for name,group in df_group_genre: 
      if name[3] == 1: 
        x='ActorSum'
        t = 'Budget: ' + name[0] + ' ,Revenue: ' + name[4] + ', FilmAwards: ' + name[1] + ', Acting Awards: ' + name[2] + ' in ' + genre + 'Revenue/Budget' + name[5]
        y='Vote_Average'
        # slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        # line = slope*x+intercept
        group.plot(x,y,style = 'o',legend = None) 
        plt.title(t)
        plt.xlabel('Weighted Sum of Women in Top Four Billed Actors')
        plt.ylabel('Average Viewer Rating')
        plt.show()
    
if __name__ == "__main__":
	sys.exit(main())