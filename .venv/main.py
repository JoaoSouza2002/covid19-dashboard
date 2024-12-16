import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# 1. Carregar os dados
data = pd.read_csv("data/covid_data.csv")

# Filtrar dados relevantes
data = data[['location', 'date', 'new_cases', 'new_deaths', 'total_vaccinations']]

# 2. Inicializar o app Dash
app = dash.Dash(__name__)

# 3. Layout do dashboard
app.layout = html.Div(
    style={
        "backgroundColor": "#1e1e1e",  # Fundo escuro
        "color": "#FFFFFF",  # Texto branco
        "fontFamily": "Arial, sans-serif",
    },
    children=[
        html.H1(
            "COVID-19 Dashboard",
            style={"textAlign": "center", "color": "#FFFFFF"}
        ),

    # Dropdown para selecionar o país
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in data['location'].unique()],
        value=['Brazil'],  # Valor inicial
        multi=True,
        style={"width": "50%", "margin": "auto"},
    ),

    # Gráfico de casos novos
    dcc.Graph(id='cases-graph'),

    # Gráfico de mortes novas
    dcc.Graph(id='deaths-graph'),

    # Gráfico de vacinas
    dcc.Graph(id='total_vaccinations-graph'),
])

# 4. Callbacks para interatividade
@app.callback(
    [Output('cases-graph', 'figure'),
     Output('deaths-graph', 'figure')],
    [Output('total_vaccinations-graph', 'figure')],
    [Input('country-dropdown', 'value')]
)
def update_graphs(selected_country):
    filtered_data = data[data['location'].isin(selected_country)]

    if len(selected_country) == 1:
        country_name = selected_country[0]
        cases_title = f"Casos Novos em {country_name}"
        death_title = f"Mortes Novas em {country_name}"
        total_vaccinations_title = f"Total de Vacinas em {country_name}"
    elif len(selected_country) == 2:
        country1, country2 = selected_country
        cases_title = f"Casos Novos Comparados entre {country1} e {country2}"
        death_title = f"Mortes Novas Comparadas entre {country1} e {country2}"
        total_vaccinations_title = f"Total de Vacinas entre {country1} e {country2}"
    else:
        cases_title = "Casos Novos Comparados"
        death_title = "Mortes Novas Comparadas"
        total_vaccinations_title = f"Total de Vacinas Comparadas"


        
    # Gráfico de casos novos
    cases_fig = px.line(
        filtered_data,
        x='date', y='new_cases', color='location',
        title=cases_title,
        template="plotly_dark"
    )

    # Gráfico de mortes novas
    deaths_fig = px.line(
        filtered_data,
        x='date', y='new_deaths', color='location',
        title=death_title,
        template="plotly_dark"
    )
    #gráfico de vacinas
    total_vaccinations_fig = px.line(
        filtered_data,
        x='date', y='total_vaccinations', color='location',
        title=total_vaccinations_title,
        template="plotly_dark"
    )
    return cases_fig, total_vaccinations_fig, deaths_fig

# 5. Rodar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
