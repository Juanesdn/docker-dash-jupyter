import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

conn = create_engine("postgresql://admin:secret@postgres:5432/postgres")


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

query = pd.read_sql_query(
    """SELECT edad, "Ubicación del caso", estado,
    "Nombre departamento", "Fecha de inicio de síntomas",
    "Fecha de muerte", "Fecha de recuperación", sexo, recuperado FROM covid_data""",
    conn,
)

df = pd.DataFrame(
    query,
    columns=[
        "edad",
        "Ubicación del caso",
        "estado",
        "Nombre departamento",
        "Fecha de inicio de síntomas",
        "Fecha de muerte",
        "Fecha de recuperación",
        "sexo",
        "recuperado",
    ],
).dropna()

sexo = df["sexo"].value_counts()
newDf = pd.DataFrame({"sexo": sexo.index, "cantidad": sexo.values})

recuperados = df["recuperado"].value_counts()
df_recuperados = pd.DataFrame(
    {"recuperacion": recuperados.index, "cantidad": recuperados.values}
)

box_fig = px.box(df, x="edad", y="estado", color="estado")
bar_fig = px.bar(newDf, y="sexo", x="cantidad", color="sexo")
recuperados_fig = px.bar(
    df_recuperados, y="cantidad", x="recuperacion", color="recuperacion"
)

app.layout = html.Div(
    children=[
        html.H1(children="Gráficas COVID-19 Colombia"),
        dcc.Graph(id="box-graph", figure=box_fig),
        dcc.Graph(id="bar-graph", figure=bar_fig),
        dcc.Graph(id="recuperados-graph", figure=recuperados_fig),
    ]
)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)

