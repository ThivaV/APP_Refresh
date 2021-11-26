import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

app = dash.Dash(__name__)
server = app.server

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the automobiles data into pandas dataframe
app_data = pd.read_csv('app_refreshing.csv', encoding="ISO-8859-1")
countries = app_data['Country'].unique()

ifa_data = pd.read_csv('new_app_users.csv', encoding="ISO-8859-1")

# Layout Section of Dash
app.layout = html.Div(children=[
    html.Div(
        html.H2('BRQ APP Refreshing Dashboard',
                style={
                    'margin-right': '2em',
                    'textAlign': 'center',
                    'color': '#503D36',
                    'font-size': 24
                }),
    ),

    html.Div([
        # First inner divsion for  adding dropdown helper text for Selected Drive wheels
        html.Div(
            html.H2('Choose a Country:', style={
                    'margin-left': '8em', 'margin-right': '2em'}),
        ),

        dcc.Dropdown(
            id='dd_country',
            options=[{'label': i, 'value': i} for i in countries],
            value='MY',
            searchable=False,
            clearable=False,
            placeholder='Select a Country',
            style={
                'width': '50%',
                'font-size': '20px',
                'padding': '3px',
                'text-align-last': 'center'
            }
        ),
    ], style={'display': 'flex', 'justify-content': 'center'}),

    # Second Inner division for adding 2 inner divisions for 2 output graphs
    html.Div(children=[
        html.Div([], id='plot1', style={'justify-content': 'center', 'display': 'inline-block'}),
        html.Div([], id='plot2', style={'justify-content': 'center', 'display': 'inline-block'})
    ]),

    html.Div(children=[
        html.Div([], id='plot3', style={'justify-content': 'center', 'display': 'inline-block'}),
        html.Div([], id='plot4', style={'justify-content': 'center', 'display': 'inline-block'})
    ])
])
# layout ends

# Place to add @app.callback Decorator
@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children'),
               Output(component_id='plot3', component_property='children'),
               Output(component_id='plot4', component_property='children')],
              [Input(component_id='dd_country', component_property='value')])
# Place to define the callback function .
def display_selected_drive_charts(country):
    filtered_app_df = app_data[app_data['Country'] == country]
    filtered_app_df['Month'] = filtered_app_df['Month'].map(str)
    filtered_app_df['Month'] = filtered_app_df['Month'].str[:-2] + "-" + filtered_app_df['Month'].str[-2:]
    filtered_app_df['Old_APPS'] = filtered_app_df['Total_APPS'] - filtered_app_df['New_APPS']

    fig1 = px.bar(filtered_app_df, x='Month', y=['Old_APPS', 'New_APPS'], title='Old & New apps', width=1000, height=500)

    fig2 = px.line(filtered_app_df, x='Month', y='New_APPS', title='New apps', width=850, height=500)
    fig2.update_traces(line_color='#FF0000')

    ifa_df = ifa_data[ifa_data['Country'] == country]
    ifa_df['Month'] = ifa_df['Month'].map(str)
    ifa_df['Month'] = ifa_df['Month'].str[:-2] + "-" + ifa_df['Month'].str[-2:]
    ifa_df['Old_App_Users'] = ifa_df['Total_Users'] - ifa_df['New_App_Users']

    fig3 = px.bar(ifa_df, x='Month', y=['Old_App_Users', 'New_App_Users'], title="Old & New app users", width=1000, height=500)

    fig4 = px.line(ifa_df, x='Month', y='New_App_Users', title='New app users', width=850, height=500)
    fig4.update_traces(line_color='#00FF00')

    return [
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4)
    ]


if __name__ == '__main__':
    app.run_server()
