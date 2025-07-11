# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'},
                                                       {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                       {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                       {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                       {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                             value='ALL',
                                             placeholder="Select a Launch Site",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                marks={0: '0 kg', 1000: '1000 kg', 2000: '2000 kg',
                                                       3000: '3000 kg', 4000: '4000 kg', 5000: '5000 kg',
                                                       6000: '6000 kg', 7000: '7000 kg', 8000: '8000 kg',
                                                       9000: '9000 kg', 10000: '10000 kg'},
                                                       value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # If 'ALL' is selected, return the pie chart for all sites
        labels ={'0': 'Failed', '1': 'Success'}
        #spacex_df['class'] = spacex_df['class'].map(labels)
        #spacex_df['Launch Site'] = spacex_df['Launch Site'].astype(str)
        
        # Create a pie chart for all sites
        fig = px.pie(spacex_df, values='class', names='Launch Site', 
                     title='Total Success Launches by Site', labels={'class': 'Launch Success'})
    else:
        # Filter the dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Create a pie chart for the selected site
        fig = px.pie(filtered_df, names='class', 
                     title=f'Success vs Failed Launches for {entered_site}',
                     labels={'class': 'Launch Success'})
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload_range):
    # Filter the dataframe based on the selected site and payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site == 'ALL':
        # If 'ALL' is selected, return the scatter chart for all sites
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Launch Site', title='Payload vs Launch Success for All Sites')
    else:
        # Filter the dataframe for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # Create a scatter chart for the selected site
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         title=f'Payload vs Launch Success for {entered_site}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
