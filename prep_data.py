"""
Get data from API
nym 2020
"""

import requests
import pandas as pd
import numpy as np
import json

def get_data(url):
    """ 
    Get data from Fantasy Football API and save to a local file:
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    """
    r = requests.get(url)
    json_data = r.json()
    with open('../data/api/json_data.json',mode='w') as J:
        json.dump(json_data,J)

def load_data(json_file):
    """ load data files """
    data = []
    with open(json_file,'r') as J:
        data = json.load(J)
    return data

def prepare_dataframes(d, team):
    """ Prepare data frames for a team """
    elements_df = pd.DataFrame(d['elements'])
    elements_types_df = pd.DataFrame(d['element_types'])
    teams_df = pd.DataFrame(d['teams'])
    slim_elements_df = elements_df[['second_name','team','element_type','selected_by_percent','now_cost','minutes','transfers_in','value_season','total_points']]
    slim_elements_df['position'] = slim_elements_df.element_type.map(elements_types_df.set_index('id').singular_name)
    slim_elements_df['team'] = slim_elements_df.team.map(teams_df.set_index('id').name)
    slim_elements_df['value'] = slim_elements_df.value_season.astype(float)
    team_df = slim_elements_df[slim_elements_df['team'] == team] 
    team_df = team_df.loc[team_df.value > 0]
    pivot = team_df.pivot_table(index='position',values='value',aggfunc=np.mean).reset_index()
    team_pivot = slim_elements_df.pivot_table(index='team',values='value',aggfunc=np.mean).reset_index()
    print(team_pivot.sort_values('value',ascending=False))

if __name__ == "__main__":
    json_file = '../data/api/json_data.json'
    d = load_data(json_file)
    prepare_dataframes(d,'Man Utd')