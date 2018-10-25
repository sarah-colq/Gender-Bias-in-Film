import sys
import csv
import json
import pandas as pd


def main():
    credits_data = pd.read_csv("tmdb_5000_credits.csv")
    movie_data = pd.read_csv("tmdb_5000_movies.csv")
    awards_data = pd.read_csv("database.csv")

if __name__ == "__main__":
	sys.exit(main())