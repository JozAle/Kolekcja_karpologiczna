import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

DATA_FOLDER = '..\data'
DATA_FILENAME = 'db.csv'
COUNTRY_DATA = 'Kraje.csv'
DATA_PATH = DATA_FOLDER + '/' + DATA_FILENAME
COUNTRY_PATH = DATA_FOLDER + '/' + COUNTRY_DATA

dataframe = pd.read_csv(DATA_PATH, sep=',', encoding="windows-1250")

countries = pd.read_csv(COUNTRY_PATH, sep=',', encoding="windows-1250")

dataframe = dataframe.drop(columns=['Unnamed: 14', 'Unnamed: 15'])

dataframe = dataframe.rename(columns={'Unnamed: 0': 'Row'})

dataframe['kraj'] = dataframe['kraj'].str.strip('\n')

print(dataframe.columns)

# def create_table(data):
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in data.columns])] +
#
#         # Body
#         [html.Tr([
#             html.Td(data.iloc[i][col], style={'border': '1px solid black'}) for col in data.columns
#         ],
#             style={'border': '1px solid black'}) for i in range(len(data))],
#         style={'border': '2px solid black'}
#     )

# word = 'nasiona'
# for column in dataframe.columns:
#     print(dataframe.loc[dataframe[column] == word, 'Unnamed: 0'].values)

wordsList = []
for column in dataframe.columns[1:]:
    wordsList = wordsList + list((dataframe[column].unique()))

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        id='hidden_data'
    ),
    dash_table.DataTable(
        id='table',
        data=dataframe.to_dict('records'),
        columns=[{'id': c, 'name': c, "selectable": True} for c in dataframe.columns],
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        selected_columns=[],
        selected_rows=[],
        style_cell={
        'textAlign': 'left',
        'minWidth': '0px',
        'maxWidth': '180px',
        'whiteSpace': 'normal'
        },
        fixed_rows={'headers': True, 'data': 0},
        style_table={'overflowX': 'scroll',
                     'maxHeight': '50%',
                     'overflowY': 'scroll'
                     },
    ),
    html.Div([
        dcc.Dropdown(
            id='wordList',
            options=[{'label': i, 'value': i} for i in dataframe['takson w bazie']],
            multi=True
        ),
    ]),
    html.Div(id='pie-tab'),
    html.Div(id='world-tab'),
])

# @app.callback(
#         Output('table-wrapper', 'children'),
#         [Input('wordList', 'value')])
# def update_table(words):
#     listy_indeksy = []
#     indeksy = []
#     if len(words):
#         # getting data for date
#         for column in dataframe.columns:
#             for word in words:
#                 listy_indeksy.append(list(dataframe.loc[dataframe[column] == word, 'Numer Wiersza'].values))
#         for lista in listy_indeksy:
#             if len(lista):
#                 for element in lista:
#                     indeksy.append(element - 1)
#         data = dataframe.loc[indeksy, :]
#         # create table
#         table = create_table(data)
#
#         return table

@app.callback(
        Output('hidden_data', 'children'),
        [Input('wordList', 'value')])
def update_data(words):
    if len(words):
        data = dataframe.loc[dataframe['takson w bazie'].isin(words)]
    else:
        data = dataframe
    return data.to_dict('records')

# @app.callback(
#         Output('table', 'data'),
#         [Input('hidden_data', 'children')])
# def update_table(data):
#     return data

@app.callback(Output('pie-tab', 'children'),
              [Input('hidden_data', 'children'),
               Input('wordList', 'value')])
def display_pie_charts(filtered_data, words):
    if len(words):
        filtered_data = pd.DataFrame(filtered_data)
        typ = filtered_data[filtered_data.columns[3]]
        kraj = filtered_data[filtered_data.columns[4]]
        region = filtered_data[filtered_data.columns[5]]
        miejsc = filtered_data[filtered_data.columns[6]]
        data = filtered_data[filtered_data.columns[7]]
        stanowisko = filtered_data[filtered_data.columns[8]]
        kto = filtered_data[filtered_data.columns[9]]
        kolekcja = filtered_data[filtered_data.columns[12]]

        fig = make_subplots(rows=2, cols=4, specs=[[{'type': 'domain'},
                                                    {'type': 'domain'},
                                                    {'type': 'domain'},
                                                    {'type': 'domain'}],
                                                   [
                                                    {'type': 'domain'},
                                                    {'type': 'domain'},
                                                    {'type': 'domain'},
                                                    {'type': 'domain'}]])

        data_typ = go.Pie(labels=[element for element in typ.unique()],
                          values=[list(typ).count(element) for element in typ.unique()],
                          name='Typ')
        fig.add_trace(data_typ, 1, 1)
        data_kraj = go.Pie(labels=[element for element in kraj.unique()],
                           values=[list(kraj).count(element) for element in kraj.unique()],
                           name='Kraj')
        fig.add_trace(data_kraj, 1, 2)
        data_region = go.Pie(labels=[element for element in region.unique()],
                             values=[list(region).count(element) for element in region.unique()],
                             name='Region')
        fig.add_trace(data_region, 1, 3)
        data_miejsc = go.Pie(labels=[element for element in miejsc.unique()],
                             values=[list(miejsc).count(element) for element in miejsc.unique()],
                             name='Miejscowość')
        fig.add_trace(data_miejsc, 1, 4)
        data_data = go.Pie(labels=[element for element in data.unique()],
                           values=[list(data).count(element) for element in data.unique()],
                           name='Rok')
        fig.add_trace(data_data, 2, 1)
        data_stanowisko = go.Pie(labels=[element for element in stanowisko.unique()],
                                 values=[list(stanowisko).count(element) for element in stanowisko.unique()],
                                 name='Stanowisko')
        fig.add_trace(data_stanowisko, 2, 2)
        data_kto = go.Pie(labels=[element for element in kto.unique()],
                          values=[list(kto).count(element) for element in kto.unique()],
                          name='Oznaczył/Zebrał')
        fig.add_trace(data_kto, 2, 3)
        data_kolekcja = go.Pie(labels=[element for element in kolekcja.unique()],
                               values=[list(kolekcja).count(element) for element in kolekcja.unique()],
                               name='Kolekcja')
        fig.add_trace(data_kolekcja, 2, 4)
        fig.update(layout_showlegend=False)
        return html.Div([
            dcc.Graph(
                id='pie_graphs',
                figure=fig
            )
        ])


@app.callback(Output('world-tab', 'children'),
              [Input('hidden_data', 'children'),
               Input('wordList', 'value')])
def display_world_chart(filtered_data, words):
    if len(words):
        filtered_data = pd.DataFrame(filtered_data)
        filtered_data = filtered_data[['takson w bazie', 'kraj']]
        amount = [1 for i in range(len(filtered_data))]
        filtered_data['amount'] = amount
        filtered_data = filtered_data.groupby(['takson w bazie', 'kraj'])['amount'].sum()
        print(filtered_data)
        filtered_data = pd.merge(filtered_data, countries, on='kraj')
        print(filtered_data)
        fig = px.scatter_geo(filtered_data, locations='value', color='kraj',
                         hover_name='kraj', size='amount',
                         projection="natural earth")

        return html.Div([
            dcc.Graph(
                id='world_map',
                figure=fig
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=False)
