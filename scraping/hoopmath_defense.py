import requests
import pandas as pd
import csv
import io
import time
import os


#function: given a list of team names, 
#write CSVs with defense stats from hoopmath for each team

#parameters: 
#teams: a list of strings of team names used by hoopmath 
#temp_path: a full path where a temp csv can be written. don't include suffixes
#write_path: where you want the CSVs to go

def write_hoopmath_defense_CSVs(teams, temp_path, write_path):
    teams=teams
    temp_path=temp_path
    write_path=write_path
    
    if type(teams)!=list:
        print('CSV writing failed. Please enter teams as a list of strings')
        return
    
    post_login_url='https://www.hoop-math.com/index.php'
    def_request_url='https://www.hoop-math.com/csvhandle.php?id=def1_2020' #defense
    
    payload = { 'email' : 'brandon.rosenthal@asu.edu',
                'pass': 'Fr33throw'
              }
    #get csv from hoopmath as raw text
    with requests.Session() as session2:
        post = session2.post(post_login_url, data=payload)
        time.sleep(10)
        r1=session2.get(post_login_url)
        r = session2.get(def_request_url)
        response_text=(r.text)
        session2.close()
        
    #create temp csv    
    temp_file=os.path.join(temp_path,'temp.csv')
    
    with open(temp_file, "w") as my_empty_csv:
        pass 
    
    #convert csv raw text to rows and write to temp csv
    two_d_array=[]
    for line in response_text.splitlines():
        word=line.split(',')
        two_d_array.append(word)
        
    with io.open(temp_file, "w", newline="",encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(two_d_array)
    f.close()
    
    #read temp csv, filter by team, write team csv
    hoopmath_df_defense=pd.read_csv(temp_file)
    
    
    for team in teams:
        df=hoopmath_df_defense[hoopmath_df_defense['Team']==team]
        team_name=team.replace(" ", "_")
        df.to_csv(os.path.join(write_path,'hoopmath'+'_defense_'+team_name+'.csv'),index=False)
    
    os.remove(temp_file)