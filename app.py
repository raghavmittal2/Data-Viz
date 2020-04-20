import dash
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output

df_ = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/worldwide-aggregated.csv')
curr_date = df_.iloc[-1, df_.columns.get_loc('Date')]
curr_conf = df_.loc[df_['Date'] == curr_date, 'Confirmed']
curr_recov = df_.loc[df_['Date'] == curr_date, 'Recovered']
curr_deaths = df_.loc[df_['Date'] == curr_date, 'Deaths']

layout = go.Layout(title='Total COVID-19 Cases Worldwide', xaxis=dict(title='Time'),
                   yaxis=dict(title='Number of People Infected'), plot_bgcolor='rgba(0,0,0,0)')

# plotting lines for Worldwide aggregate
confirmed = go.Scatter(x=df_['Date'], y=df_['Confirmed'], line=dict(color='blue', width=1.1),
                     opacity=0.8, name='Confirmed')
recovered = go.Scatter(x=df_['Date'], y=df_['Recovered'],  line=dict(color='green', width=1.1),
                     opacity=0.8, name='Recovered Cases')
dead = go.Scatter(x=df_['Date'], y=df_['Deaths'],  line=dict(color='red', width=1.1),
                     opacity=0.8, name='Deaths')

# worldmap graph
df_country = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv')
curr_date2 = df_country.iloc[-1, df_country.columns.get_loc('Date')]     # extracting current date
df_sep = df_country[df_country['Date'] == curr_date2]

data2 = {'type': 'choropleth',
         'locations': df_sep['Country'],
         'locationmode': 'country names',
         'autocolorscale': False,
         'colorscale': 'Rainbow',
         'text': df_sep['Country'],
         'z': df_sep['Confirmed'],
         'marker': {'line': {'color': 'rgb(255,255,255)', 'width': 1}},
         'colorbar': {'title': 'Colour Range', 'len': 0.25, 'lenmode': 'fraction'}
         }
layout2 = dict(height=600, widht=600, geo=dict(scope='world'), title='Current Active Cases by Country')

# Countries pie chart
labels = df_sep['Country']
values = df_sep['Confirmed']
data3 = go.Pie(labels=labels, values=values, textinfo='label+percent')


# country wise scatter
df_up = df_country.loc[df_country['Country'] == 'Ireland']
df_all_countries = df_country.loc[df_country['Date'] == curr_date]
features = df_all_countries['Country']
opts = [{'label': i, 'value': i} for i in features]

layout_cont = go.Layout(title='Total COVID-19 Cases in the Selected Country', xaxis=dict(title='Time'),
                    yaxis=dict(title='Number of People Infected'), plot_bgcolor='rgba(0,0,0,0)')
confirmed_cont = go.Scatter(x=df_up['Date'], y=df_up['Confirmed'], line=dict(color='blue', width=1.1),
                            opacity=0.8, name='Confirmed')
recovered_cont = go.Scatter(x=df_up['Date'], y=df_up['Recovered'],  line=dict(color='green', width=1.1),
                     opacity=0.8, name='Recovered Cases')
dead_cont = go.Scatter(x=df_up['Date'], y=df_up['Deaths'],  line=dict(color='red', width=1.1),
                     opacity=0.8, name='Deaths')
fig = go.Figure(data=[confirmed_cont, recovered_cont, dead_cont], layout=layout_cont)
fig.update_layout(title_text='Total COVID-19 Cases in the Selected Country', title_x=0.5)


#dbc.themes.BOOTSTRAP
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(
        [html.H1('Novel Coronavirus (COVID-19) Data Visualization'),
         html.H6('School of Computer Science and Statistics, Trinity College Dublin'),
         ],
        style={'padding': '10px', 'backgroundColor': ' #e4e4e7'}
    ),
    html.Div([
        html.H3('Total Cofirmed Cases Worldwide: ' + str(curr_conf.values)),
        html.H3('Total Recovered Cases Worldwide: ' + str(curr_recov.values)),
        html.H3('Total Deaths Worldwide: ' + str(curr_deaths.values))
    ], style={'padding': '10px', 'backgroundColor': '#d6d6db'}
    ),


    html.Div([
        # country wise scatter plot
        html.Div([
            dcc.Graph(
                id='country_scatter',
                figure=fig
            ),
            # dropdown component
            html.P([
                dcc.Dropdown(
                    id='first-dropdown',
                    options=opts,
                    placeholder='Select a Country',
                    value='Ireland'
                )
            ], style={'width': '500px',
                      'fontSize': '20px',
                      'padding-left': '50px',
                      'display': 'inline-block'}
            ),
        ], className='six columns'),

        # worldwide scatter plot
        html.Div([
            dcc.Graph(
                id='wordwide-aggregate',
                figure={
                    'data': [confirmed, recovered, dead],
                    'layout': layout
                },
            ),
        ], className='six columns'),
    ], className="row"),


    html.Div([
        html.Div([
            dcc.Graph(
                id='worldmap',
                figure={
                    'data': [data2],
                    'layout': layout2
                }
            ),
        ], className='six columns'),
        html.Div([
            dcc.Graph(
                id='pie-country',
                figure={
                    'data': [data3],
                    'layout': {'height': 600, 'width': 800, 'title': 'Distribution of SARS-CoV2 across Nations'}
                }
            )
        ], className='six columns'),
    ], className='row'),
])


@app.callback(Output('country_scatter', 'figure'), [Input('first-dropdown', 'value')])
def update_figure(x):
    df_new = df_country.loc[df_country['Country'] == x]
    confirmed_new = go.Scatter(x=df_new['Date'], y=df_new['Confirmed'], line=dict(color='blue', width=1.1),
                                opacity=0.8, name='Confirmed')
    recovered_new = go.Scatter(x=df_new['Date'], y=df_new['Recovered'], line=dict(color='green', width=1.1),
                                opacity=0.8, name='Recovered Cases')
    dead_new = go.Scatter(x=df_new['Date'], y=df_new['Deaths'], line=dict(color='red', width=1.1),
                           opacity=0.8, name='Deaths')
    figgie = go.Figure(data=[confirmed_new, recovered_new, dead_new], layout=layout_cont)
    return figgie


if __name__ == "__main__":
    app.run_server(debug=True)
