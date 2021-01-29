#imports
import jinja2
import pandas as pd

#load dataframe that's gonna populate the html template
df=pd.read_csv('sports_reference_sample_df.csv')
df['oreb_per_game']=df['oreb_per_game'].round(1)
df=df.rename(columns={'name':'Name','oreb_per_game':'OReb/Game'})

#load and render html template
templateLoader = jinja2.FileSystemLoader(searchpath="../Documents/")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.txt"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(df=df)

#write and save html file
html_file = open('../Documents/hell_yeah_brother' + '.html', 'w')
html_file.write(outputText)
html_file.close()

