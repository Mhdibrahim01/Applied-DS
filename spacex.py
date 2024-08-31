import pandas as pd
import datetime as dt
import plotly.express as px
from dash import Dash, dcc, html, Output, Input



#load data
spacex_df=pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
app=Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',value='all',options=[
                                    {'label': 'All Sites', 'value':'all'},
                                    {'label': 'CCAFS LC-40','value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40','value': 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A','value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E','value': 'VAFB SLC-4E'}
                                    
                                ]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=min_payload,max=max_payload,step=1000,
                                                value=[min_payload, max_payload],
                                                marks={int(min_payload): str(int(min_payload)), 
                                                int(max_payload): str(int(max_payload))},
                                                tooltip={"placement": "bottom", "always_visible": True},),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider',component_property='value'))
def get_graph(site,payload):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload[1])]
    if site=='all':
        pie_fig=px.pie(filtered_df,values='class',names='Launch Site',title='Total Success Launch By Site')
        scatter_fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Launch Site',title='Correlation between Payload and Success for all Sites')
    else:
        site_df=filtered_df[filtered_df['Launch Site']==site]
        success_count=site_df['class'].value_counts().reset_index()
        pie_fig=px.pie(success_count,values='count',names='class',color='class',color_discrete_map={1:'green',0:'red'},title=f'Total Success Launches for site {site}')
        scatter_fig=px.scatter(site_df,x='Payload Mass (kg)',y='class',color='Booster Version',title=f'Correlation between Payload and Success for site {site}')
    return pie_fig,scatter_fig,
if __name__ == '__main__':
    app.run_server(debug=True)