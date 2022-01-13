from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.urls import reverse

from dashboard.data import SingleState
from dashboard.creds import API_KEY as ak
from dashboard.usStates import US_STATES

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import re

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    def get(self, request):
        data = json.loads(open('dashboard/data.json', 'r').read())
        return render(request, 'index.html', context=data)


def format_commas(num):
    return "{:,}".format(num)

class SingleStateView(TemplateView):
    template_name = 'StateData.html'
    def get(self, request, **kwargs):
        state = request.GET.get('q')

        if len(state) <= 0:
            return HttpResponseRedirect(reverse('dashboard:index'))

        df = pd.read_csv("https://api.covidactnow.org/v2/states.csv?apiKey={}".format(ak))

        data = df[df['state'] == state]

        c = pd.read_csv("https://api.covidactnow.org/v2/counties.csv?apiKey={}".format(ak))
        c = c[c['state'] == state]
        display = pd.DataFrame()
        display['County'] = c['county']
        display['Cases'] = c['actuals.cases']
        display['Deaths'] = c['actuals.deaths']
        res = display.values.tolist()

        context = dict(
            date_updated = data['lastUpdatedDate'].iloc[0],
            cases_today = format_commas(int(data['actuals.newCases'].iloc[0])),
            deaths_today = format_commas(int(data['actuals.newDeaths'].iloc[0])),
            total_cases = format_commas(int(data['actuals.cases'].iloc[0])),
            total_deaths = format_commas(int(data['actuals.deaths'].iloc[0])),
            vax_dist = format_commas(data['actuals.vaccinesDistributed'].iloc[0]),
            vax_adm = format_commas(data['actuals.vaccinesAdministered'].iloc[0]),
            counties = res,
        )

        return render(request, 'StateData.html', context=context)


def sentence_case(string):
    if string != '':
        result = re.sub('([A-Z])', r' \1', string)
        return result[:1].upper() + result[1:].lower()



def update_data(request):
    # Update the data

    # Read today's state summary data
    df = pd.read_csv("https://api.covidactnow.org/v2/states.csv?apiKey={}".format(ak))

    # Read time series state summary data
    dfts = pd.read_csv("https://api.covidactnow.org/v2/states.timeseries.csv?apiKey={}".format(ak))
    # Get only the data from Jan 1st, 2021 so that the line chart looks clearer
    usa_ts = dfts.groupby(['date'], as_index=False).sum()
    usa_ts = usa_ts[usa_ts['date'] >= '2021-01-01'] 
    
    # Decode state names
    us = {v: k for k, v in US_STATES.items()}
    st_list = [us[state] for state in df['state']]
    df['stateName'] = st_list

    # Update text data on index page
    data = dict()
    data['date_updated'] = df['lastUpdatedDate'][0]
    data['total_cases'] = str(format_commas(int(df['actuals.newCases'].sum())))
    data['total_deaths'] = str(format_commas(int(df['actuals.newDeaths'].sum())))
    data['vaccines_distributed'] = str(format_commas(int(df['actuals.vaccinesDistributed'].sum())))
    data['vaccines_administered'] = str(format_commas(int(df['actuals.vaccinesAdministered'].sum())))
    json.dump(data, open('dashboard/data.json', 'w'))


    # Update the plots

    # Line chart daily new cases since 01/01/2021
    fig_usa_new_cases = px.line(usa_ts, x='date', y="actuals.newCases", labels={'date': 'Date', 'actuals.newCases': 'Number of new cases'})
    fig_usa_new_cases.update_layout(
        font={
            'size':14,
        },
    )
    fig_usa_new_cases.write_html("templates/LineChartDailyCases.html")



    # Top 10 states with most new cases today
    top10_cases = df.sort_values(by='actuals.newCases', axis=0, ascending=False).iloc[:10]

    fig_top10_cases = px.bar(top10_cases, x='stateName', y='actuals.newCases', labels={'stateName': 'State', 'actuals.newCases': 'Number of cases'})
    fig_top10_cases.update_layout(
        font=dict(
            size=14,
        )
    )
    fig_top10_cases.update_traces(marker_color='Medium Purple')
    fig_top10_cases.write_html("templates/top10StatesNewCases.html")



    # Daily new cases in the US
    fig_new_cases = go.Figure(data=go.Choropleth(
        locations=df['state'],
        z = df['actuals.newCases'].astype(float),
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Number of new cases",
    ))

    fig_new_cases.update_layout(
        margin=dict(l=60, r=60, t=50, b=50),
        geo_scope='usa',
            font=dict(
                size=14,
            )
    )
    fig_new_cases.write_html("templates/newCases.html")



    # Line chart daily deaths since 01/01/2021
    fig_usa_new_deaths = px.line(usa_ts, x='date', y="actuals.newDeaths", labels={'date': 'Date', 'actuals.newDeaths': 'Number of deaths'})
    fig_usa_new_deaths.update_layout(
        font={
            'size':14,
        },
    )
    fig_usa_new_deaths.write_html("templates/LineChartDailyDeaths.html")



    # Top 10 states with most deaths today
    top10_deaths = df.sort_values(by='actuals.newDeaths', axis=0, ascending=False).iloc[:10]
    fig_top10_deaths = px.bar(top10_deaths, x='stateName', y='actuals.newDeaths', labels={'stateName': 'State', 'actuals.newDeaths': 'Number of deaths'})
    fig_top10_deaths.update_layout(
        font=dict(
            size=14,
        )
    )
    fig_top10_deaths.update_traces(marker_color='Medium Purple')
    fig_top10_deaths.write_html("templates/top10StatesNewDeaths.html")



    # Daily new deaths in the US
    fig_new_deaths = go.Figure(data=go.Choropleth(
        locations=df['state'],
        z = df['actuals.newDeaths'].astype(float),
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'BuPu',
        colorbar_title = "Number of new deaths",
    ))

    fig_new_deaths.update_layout(
        geo_scope='usa',
        font=dict(
            size=14,
        ),
    )
    fig_new_deaths.write_html("templates/newDeaths.html")



    # Cumulative negative vs positive tests
    fig_nvp = px.scatter(df, x='actuals.positiveTests', y='actuals.negativeTests', color='stateName', labels={
        'actuals.positiveTests': 'Number of positive tests',
        'actuals.negativeTests': 'Number of negative tests',
        'stateName': 'State'
    })
    fig_nvp.update_layout(
        font=dict(
            size=14,
        ),
    )
    fig_nvp.update_traces(marker_size=12)
    fig_nvp.write_html("templates/NegVsPos.html")

    # Risk level chorepleths
    riskLevels_list = [col for col in df.columns if 'riskLevels' in col]

    for rl in riskLevels_list:
        
        fig_risk = go.Figure(data=go.Choropleth(
            locations=df['state'],
            z = df[rl].astype(float),
            locationmode = 'USA-states', # set of locations match entries in `locations`
            colorscale = 'Viridis',
        ))

        fig_risk.update_layout(
            title_text=sentence_case(str(rl).split('.')[1]),
            title_x=0.5,
            geo_scope='usa',
            font=dict(
                size=14,
            ),
        )
        fig_risk.write_html("templates/{}.html".format(str(rl).split('.')[1]))


    return HttpResponseRedirect(reverse('dashboard:index'))