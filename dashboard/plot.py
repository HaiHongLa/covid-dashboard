import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from creds import API_KEY as ak

df = pd.read_csv("https://api.covidactnow.org/v2/states.csv?apiKey={}".format(ak))

fig_new_cases = go.Figure(data=go.Choropleth(
    locations=df['state'],
    z = df['actuals.newCases'].astype(float),
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "New Cases",
))

fig_new_cases.update_layout(
    title_text = "New Cases in the US today",
    geo_scope='usa', # limite map scope to USA
)
fig_new_cases.write_html("../templates/newCases.html")