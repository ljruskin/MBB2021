
import pandas as pd
pd.options.display.max_rows=100
pd.options.display.max_columns=100

from sportsreference.ncaab.roster import Roster
from sportsreference.ncaab.roster import Player


#pulling player data into one dataframe

team = Roster('ARIZONA-STATE') #get team roster object
team_players=[]
for player in team.players:
    team_players.append(player.player_id) #add team player_ids to a list
    
player_dfs=[] #eventually store player dataframes
for name in team_players:
    player=Player(name)
    #use try catch because some players have null values 
    try:
        test=player.field_goal_attempts
        player_df=player.dataframe
        player_df['name']=player.name #add name column
        player_dfs.append(player_df)
    except:
        continue 
        
player_data=pd.concat(player_dfs) #concaatenate all player dfs into one  

player_data['year']=player_data.index  #add year column, which was previously the index
player_data=player_data.reset_index(drop=True)

#for some reason, year is added as a tuple. strip the relevant year string
for row in range(player_data.shape[0]):
    player_data.at[row,'year']=player_data.at[row,'year'][0]

#reorder columns (put name and year first)
cols=player_data.columns.to_list()
player_data=player_data[cols[-2:]+cols[:-2]]

player_data



#defining functions to create data for report 

def who_to_foul(df,year): #enter year as string (example :'2018-19')
    df=df.query('year==@year') #filter by year
    df=df.query('minutes_played/games_played > 8') #filter players with more than 8 mpg
    df=df.sort_values(by=['free_throw_percentage'],ascending=True)
    return_df=df[['name','free_throw_percentage']]
    return(return_df)

def who_draws_fouls(df,year):
    df=df.query('year==@year') #filter by year
    df=df.query('minutes_played/games_played > 8') #filter players with more than 8 mpg
    
    df=df.reset_index()
    df['fta_per_40']=''
    for row in range(df.shape[0]):
        df.at[row,'fta_per_40']=40*(df.at[row,'free_throw_attempts']/df.at[row,'minutes_played'])
    
    df=df.sort_values(by=['fta_per_40'],ascending=False)
    return_df=df[['name','fta_per_40']]
    return(return_df)

def three_shooters(df,year):
    df=df.query('year==@year') #filter by year
    df=df.query('minutes_played/games_played > 8') #filter players with more than 8 mpg
    
    df=df.reset_index()
    df['three_att_per_game']=''
    for row in range(df.shape[0]):
        df.at[row,'three_att_per_game']=df.at[row,'three_point_attempts']/df.at[row,'games_played']
    
    df=df.sort_values(by=['three_point_percentage'],ascending=False)
    return_df=df[['name','three_att_per_game','three_point_percentage']]
    return(return_df[0:4])

def who_turns_ball_over(df,year):
    df=df.query('year==@year') #filter by year
    df=df.query('minutes_played/games_played > 8') #filter players with more than 8 mpg
    df=df.sort_values(by=['turnover_percentage'],ascending=False)
    return_df=df[['name','turnover_percentage']]
    return(return_df)

def who_grabs_offensive_rebounds(df,year):
    df=df.query('year==@year') #filter by year
    df=df.query('minutes_played/games_played > 8') #filter players with more than 8 mpg
    
    df=df.reset_index()
    df['oreb_per_game']=''
    for row in range(df.shape[0]):
        df.at[row,'oreb_per_game']=df.at[row,'offensive_rebounds']/df.at[row,'games_played']
    
    df=df.sort_values(by=['oreb_per_game'],ascending=False)
    return_df=df[['name','oreb_per_game']]
    return(return_df[0:4])
    


who_grabs_offensive_rebounds(player_data,'2018-19')
    

