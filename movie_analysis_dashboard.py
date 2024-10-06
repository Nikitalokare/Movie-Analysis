from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import dash_daq as daq


movies_data = pd.read_csv(r"C:\Users\user\Desktop\PLOTLY DASH\moviw_2024_list.csv")
movies_data.columns = movies_data.columns.str.strip()
geners_wise_movie_data = pd.read_csv(r"C:\Users\user\Desktop\PLOTLY DASH\genres_wise_data.csv")

load_figure_template("darkly")
print(movies_data.head())
filtered_columns = [col for col in movies_data.columns if (movies_data[col] == '60 crore').any()]

# Generate options for dcc.Checklist
checklist_options = [{'label': col, 'value': col} for col in filtered_columns]

# Default value for checklist
default_value = [filtered_columns[0]] if filtered_columns else []

movie_app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

movie_app.layout = html.Div([
    html.H1(children='Bollywood Movies Analysis', style={'text-align': 'center'}),

    dbc.Row([
        dbc.Col(dcc.Graph(id="graph", style={'width': '100%', 'height': '70vh'}), width=6),
        dbc.Col(dcc.Graph(id='graph2', style={'width': '100%', 'height': '70vh'}), width=6)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.P("Values:"),
            dcc.Dropdown(
                id='my_dropdown',
                options=[
                    {'label': 'Verdict', 'value': 'Verdict'},
                    {'label': 'Box Office Collection', 'value': 'Box Office Collection'},
                    {'label': 'Budget (Cost+ P&A)', 'value': 'Budget (Cost+ P&A)'}
                ],
                value='Verdict',
                multi=False,
                clearable=False,
                style={"width": "100%", 'background-color': 'Black'}
            ),
        ], width=3),
        
        dbc.Col([
            html.P("Genres:"),
            dcc.Dropdown(
                id='my_dropdown_genres',
                options=[
                    {'label': 'Genre', 'value': 'Genre'},
                    {'label': 'Movies', 'value': 'Movies'},
                    {'label': 'Share', 'value': 'Share'}
                ],
                value='Genre',
                multi=False,
                clearable=False,
                style={"width": "100%", 'background-color': 'Black'}
            ),
        ], width=3)
    ]),
    html.Div([
    dbc.Row([
        dbc.Col([
            daq.ToggleSwitch(
                id='my-toggle-switch',
                value=False,
            ),
            html.Div(id='my-toggle-switch-output'),
                    dcc.Checklist(
                        id='my-checklist',
                        options=[{'label': movie_name, 'value': movie_name} for movie_name in movies_data['Movie Name']],
                        value=[movies_data['Movie Name'].iloc[0]],  # Default selected movie
                        inline=True
                    ),
                ])
            ]),
            html.Div(id='checklist-output')
        ]),
    html.Br(),
    html.Div([
        html.H4(children='Below Table Shows all Movies Collection released in the year of 2024'),
        dash_table.DataTable(
            movies_data.to_dict('records'), 
            [{"name": i, "id": i} for i in movies_data.columns],
            id='inline_data',
            selected_rows=[],
            selected_row_ids=[],
            page_size=10,
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'background-color': 'grey',
                'text-align': 'center'
            }
        )
    ])
])

@movie_app.callback(
    [Output('my-checklist', 'options'),
     Output('my-toggle-switch-output', 'children')],
    [Input('my-toggle-switch', 'value'),
     Input('my-checklist', 'value')]
)
def update_output(switch_value, selected_movies):
    print(f"Switch value: {switch_value}")
    print(f"Selected movies: {selected_movies}")

    if switch_value:
        # Update the checklist options based on a condition
        options = [{'label': movie_name, 'value': movie_name} for movie_name in movies_data['Movie Name']]
        return options, f"Toggle Switch is ON. Selected movies: {', '.join(selected_movies)}"
    else:
        options = [{'label': movie_name, 'value': movie_name} for movie_name in movies_data['Movie Name']]
        return options, "Toggle Switch is OFF"

    #     print("+++++++++++++++++True++++++++++++")
    # else:
    #     print("+++++++++++++++False+++++++++++++")
    #     filtered_data = movies_data
    
    # return filtered_data.to_dict('records'), f'Toggle Switch is {"ON" if switch_value else "OFF"}'


@movie_app.callback(
    Output("graph", "figure"),
    Input("my_dropdown", "value")
)
def generate_movie_chart(value):
    fig = px.pie(
        data_frame=movies_data, names=value, hole=.3, title='Rating movie success in 2024')
    return fig

@movie_app.callback(
    Output("graph2", "figure"),
    Input("my_dropdown_genres", "value")
)
def generate_movie_bar_chart(value):
    bar_chart = px.bar(
        data_frame=geners_wise_movie_data, x=value, y='Movies', title='Genres Wise Movies Record')
    return bar_chart

if __name__ == '__main__':
    movie_app.run(debug=True)
