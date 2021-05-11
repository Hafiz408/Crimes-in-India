import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import seaborn as sns
import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
# ------------------------------------------------------------------------------
# Dash layout 
app.layout = html.Div([

    dcc.Location(id='url', refresh=False),
    html.H1("Data Visualization Project", style={'text-align': 'center','color':'white','backgroundColor':'black'}),
    html.H2("Analysis on various crimes in India", style={'text-align': 'center','color':'white','backgroundColor':'black'}),
    html.P(dcc.Link('Go to page-1', href='/page-1'),style={'text-align':'center','color':'white'}),
    html.P(dcc.Link('Go to page-2', href='/page-2'),style={'text-align':'center','color':'white'}),
    html.Div(id='Page-content'),
    html.H3("Done by Tarun and Hafiz", style={'text-align':'right','color':'white','backgroundColor':'black','font-size':'120%'}),
])
# ------------------------------------------------------------------------------
# Data manipulation to produce each graphs
df=pd.read_csv(r'E:/Sem-4/Data Visualization Lab/crime/01_District_wise_crimes_committed_IPC_2001_2012.csv')
df=df[df['DISTRICT']=='TOTAL']
df.drop(['DISTRICT'],axis=1,inplace=True)
df=df.set_index(['STATE/UT'])
df=df.reset_index()
df=df.groupby(['STATE/UT','YEAR']).sum().reset_index()

fig1 = px.sunburst(df,path=['STATE/UT','YEAR'],values='TOTAL IPC CRIMES',title="State and year wise segregation of total crimes")

df.groupby(['YEAR']).sum().reset_index()
fig2=px.treemap(df,path=['STATE/UT','YEAR'],values='TOTAL IPC CRIMES')

fig3=plt.figure(figsize=(8,12))
plt.bar(df['YEAR'], df['TOTAL IPC CRIMES'])

murder=df['MURDER'].sum()
rape=df['RAPE'].sum()
kidnapping=df['KIDNAPPING & ABDUCTION'].sum()
robbery=df['ROBBERY'].sum() 
riots=df['RIOTS'].sum() 
dacoity=df['DACOITY'].sum() 
burglary=df['BURGLARY'].sum() 
theft=df['THEFT'].sum() 
cheating=df['CHEATING'].sum() 
counterfieting=df['COUNTERFIETING'].sum() 
dowry=df['DOWRY DEATHS'].sum() 
others=df['TOTAL IPC CRIMES'].sum() - (murder+rape+kidnapping+robbery+riots+dacoity+burglary+theft+cheating+counterfieting+dowry)
crime_type = ['Murder','Rape','Kidnapping','Robbery','Riots','Dacoity','Burglary','Theft','Cheating','Counterfieting','Dowry','Others']
crime_type_vals = [murder,rape,kidnapping,robbery,riots,dacoity,burglary,theft,cheating,counterfieting,dowry,others]

fig4 = go.Figure(data=[go.Pie(labels=crime_type, values=crime_type_vals,sort=False,marker=dict(colors=px.colors.qualitative.G10),textfont_size=12)])

crimes = ['MURDER', 'RAPE', 'KIDNAPPING & ABDUCTION',
        'DACOITY', 'ROBBERY', 'BURGLARY', 'THEFT',
       'AUTO THEFT', 'RIOTS', 'CHEATING', 'COUNTERFIETING', 'ARSON', 'HURT/GREVIOUS HURT',
       'DOWRY DEATHS', 'ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY',
       'INSULT TO MODESTY OF WOMEN', 'CRUELTY BY HUSBAND OR HIS RELATIVES',
       'IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES',
       'CAUSING DEATH BY NEGLIGENCE']

scy = df.groupby(['YEAR'])[crimes].sum().reset_index()

fig5 = px.line(scy, x='YEAR', y=crimes)

dff = df.copy()
dff = df.groupby('YEAR')['TOTAL IPC CRIMES'].sum().reset_index()
fig6 = px.bar(dff, x='YEAR', y='TOTAL IPC CRIMES')

# dff = merged.copy()
# dff = dff.groupby('state')['TOTAL IPC CRIMES'].sum().sort_values(ascending=True).reset_index()
# fig7 = px.bar(dff, y='state', x='TOTAL IPC CRIMES')

victims = pd.read_csv(r'E:/Sem-4/Data Visualization Lab/crime/20_Victims_of_rape.csv')
# fig, ax = plt.subplots(1, figsize=(10, 10))
# ax.axis('off')
# ax.set_title('State-wise Rape-Cases Reported (2001-2010)', fontdict={'fontsize': '15', 'fontweight' : '3'})
# fig11 = merged.plot(column='RAPE', cmap='Reds', linewidth=0.5, ax=ax, edgecolor='0.2',legend=True)
safe1 = victims.groupby('Area_Name')['Rape_Cases_Reported'].sum().sort_values(ascending=True).reset_index()
s_state = safe1.head(10)
fig12 = px.bar(s_state, x='Rape_Cases_Reported', y='Area_Name',title='Most Safe States for Women')
unsafe=safe1.tail(10)
fig13=px.pie(unsafe, names='Area_Name', values='Rape_Cases_Reported',title='Most UnSafe States for Women')

tr_victims = victims[victims['Subgroup']=='Total Rape Victims']
s1 = tr_victims.groupby('Year')['Rape_Cases_Reported'].sum().reset_index()
fig14 = px.bar(s1, x='Year', y='Rape_Cases_Reported',title='Victims Of Rape Yearly')
inc_victims = victims[victims['Subgroup']=='Victims of Incest Rape']
sum_cases=inc_victims.groupby('Year')['Rape_Cases_Reported'].sum().reset_index()
fig15 = px.bar(sum_cases,x='Year',y='Rape_Cases_Reported', title='Victims Of Incest Rape Yearly')

above_50 = inc_victims['Victims_Above_50_Yrs'].sum()
ten_to_14 = inc_victims['Victims_Between_10-14_Yrs'].sum()
fourteen_to_18 = inc_victims['Victims_Between_14-18_Yrs'].sum()
eighteen_to_30 = inc_victims['Victims_Between_18-30_Yrs'].sum()
thirty_to_50 = inc_victims['Victims_Between_30-50_Yrs'].sum()
upto_10 = inc_victims['Victims_Upto_10_Yrs'].sum()

age_grp = ['Upto 10','10 to 14','14 to 18','18 to 30','30 to 50','Above 50']
age_group_vals = [upto_10,ten_to_14,fourteen_to_18,eighteen_to_30,thirty_to_50,above_50]

fig16 = go.Figure(data=[go.Pie(labels=age_grp, values=age_group_vals,sort=False,
                            marker=dict(colors=px.colors.qualitative.G10),textfont_size=8)])
       
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
     Output('Page-content', 'children'),
    [Input('url', 'pathname')]
)

def display_page(pathname):
    if pathname=='/page-1':

            return html.Div(children=[
            html.Div([
               html.Div([
                    html.H2("General Crimes in India Visuals", style={'text-align': 'center','color':'white','backgroundColor':'black'}),
                    html.H1(children='Sunburst Graph',style={'text-align':'center','backgroundColor':'white'}),
                    
                    dcc.Graph(
                        id='graph1',
                        figure=fig1
                    ),  
                    html.Div(children='''
                        Sunburst graph for easier visualization of various types of crimes in India from 2001-2012
                '''),
                ], className='six columns'),
                html.Div([
                    html.H1(children='Tree map',style={'text-align':'center','backgroundColor':'white'}),

                    dcc.Graph(
                        id='graph2',
                        figure=fig2
                    ),  
                     html.Div(children='''
                        Tree map for easier visualization of various types of crimes in India from 2001-2012
                '''),
                ], className='six columns'),
            ], className='row'),
            html.Div([
                html.Br(),
                html.H1(children='Piechart',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph3',
                    figure=fig4
                ),  
                html.Div(children='''
                        From this piechart we can see that out of all the named crimes, Theft is having highest number of victims and Dowry is having the least victims.
                '''),
            ], className='row'),
            html.Div([
                html.Br(),
                html.H1(children='Linechart',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph4',
                    figure=fig5
                ),  
                html.Div(children='''
                        From 2000-07 Hurt/Grevious hurt is having highest number of victims and then after 2007 it was over taken by Theft.
                        Auto theft and Burglary are followed after Hurt and Theft.
                '''),
            ], className='row'),
            html.Div([
                html.Br(),
                html.H1(children='Bar graph',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph5',
                    figure=fig6
                ),  
                html.Div(children='''
                        Year wise total cases
                '''),
            ], className='row'),
        ])
    elif pathname=='/page-2':

            return html.Div(children=[
            html.Div([
                html.Div([
                    html.H2("Rape Analysis", style={'text-align': 'center','color':'white','backgroundColor':'black'}),
                    html.H1(children='Barchart',style={'text-align':'center','backgroundColor':'white','font-family': "Times New Roman"}),

                    dcc.Graph(
                        id='graph1',
                        figure=fig12
                    ),  
                    html.Div(children='''
                        
                '''), 
                ], className='six columns'),
                html.Div([
                    html.H1(children='Piechart',style={'text-align':'center','backgroundColor':'white','font-family': "Times New Roman"}),
                    dcc.Graph(
                        id='graph2',
                        figure=fig13
                    ),  
                     html.Div(children='''
                        
                '''), 
                ], className='six columns'),
            ], className='row'),
            html.Div([
                html.Br(),
                html.H1(children='Bar graph',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph3',
                    figure=fig14
                ),  
                html.Div(children='''
                        
                '''),
            ], className='row'),
            html.Div([
                html.Br(),
                html.H1(children='Bar graph',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph4',
                    figure=fig15
                ),  
                html.Div(children='''
                        In 2005, around 750 cases were reported which is the highest number of that decade.
                        The year 2010 recorded the lowest number of cases i.e 288.
                '''),
            ], className='row'),
            html.Div([
                html.Br(),
                html.H1(children='Piechart',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph5',
                    figure=fig16
                ),  
                html.Div(children='''
                        
                '''),
            ], className='row'),
        ])
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
