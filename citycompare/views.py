from __future__ import absolute_import
from flask import render_template
from citycompare import flask_app
from sodapy import Socrata
import pandas as pd
import plotly
from plotly.graph_objs import Scatter, Layout

from .forms import CityForm

@flask_app.route('/')
def index():
    return render_template(
        'index.html',
        city_form=CityForm(),
    )

@flask_app.route('/plot')
def plot():
    # for client with token:
    # client = Socrata("sandbox.demo.socrata.com", "FakeAppToken", username="fakeuser@somedomain.com", password="ndKS92mS01msjJKs")
    client = Socrata("data.calgary.ca", None)
    results = client.get("qzer-3is5", order='date DESC', limit=2000)

    # put into dataframe
    results_df = pd.DataFrame.from_records(results)

    # Data prep
    results_df['date'] = pd.to_datetime(results_df['date'])
    # df.loc[df['major_incident_type'] == 'False Alarm']

    # results_df['incident_count'].iloc(['major_incident_type'='False Alarm'])

    # subset false alarm dataframe
    fa_df = results_df.loc[results_df['major_incident_type'] == 'False Alarm']
    f_df = results_df.loc[results_df['major_incident_type'] == 'Fire']

    data1 = Scatter(x=fa_df['date'], y=fa_df['incident_count'], name='False Alarm')
    data2 = Scatter(x=f_df['date'], y=f_df['incident_count'], name='Fire')

    plot_html = plotly.offline.plot(
        {
            "data": [data1, data2],
            "layout": Layout(title="Calgary Fire Incidents",
                             legend=dict(orientation="h"))
        },
        output_type='div'
    )

    return plot_html