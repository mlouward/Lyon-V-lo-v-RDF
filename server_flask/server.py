import json
import os

import folium
from flask import (Flask, Markup, flash, redirect, render_template, request,
                   session, url_for)
import pandas as pd
import requests

app = Flask(__name__)
app.secret_key = os.urandom(16)  # Random key


# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    """index, page de départ"""
    if request.method == 'POST':
        return redirect(url_for('geomap'))

    return render_template('index.html')  # page d'accueil


# geomap of Lyon and its bike stations
@app.route('/map')
def geomap():
    lyon = folium.Map(
        location=[45.7661517, 4.85813048], zoom_start=14, tiles="CartoDB Positron")
    stations = get_stations_infos()
    live_count = get_bikes_by_station()
    coordinates = stations[['lat', 'lng']].values.tolist()

    for point in range(len(coordinates)):
        folium.Marker(coordinates[point],
                      popup=map_popup(stations, live_count, point),
                      icon=folium.Icon(color='red',
                                       icon_color='white')).add_to(lyon)
    lyon._repr_html_()
    map_div = Markup(lyon.get_root().html.render())
    hdr_txt = Markup(lyon.get_root().header.render())
    script_txt = Markup(lyon.get_root().script.render())

    return render_template(
        'geomap.html', map_div=map_div, hdr_txt=hdr_txt, script_txt=script_txt,
        data=live_count.to_dict('records')
    )


def get_stations_infos():
    response = requests.post('http://localhost:3030/ds/sparql',
                             data={'query': '''
    prefix ex: <http://www.semanticweb.org/maxime/ontologies/2021/2/untitled-ontology-16#>
    prefix ns1: <http://www.semanticweb.org/maxime/ontologies/2021/2/untitled-ontology-16#BicycleStand/>
    prefix owl: <http://www.w3.org/2002/07/owl#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?id ?name ?lat ?lng WHERE { ?station a ex:BicycleStand ;ns1:name ?name ; ns1:lat ?lat ;ns1:lng ?lng ; ns1:id ?id . }
    '''})

    all_results = []
    result_json = response.json()['results']['bindings']
    for row in result_json:
        tmp = [row['id']['value'], row['name']['value'],
               row['lat']['value'], row['lng']['value']]
        all_results.append(tmp)

    return pd.DataFrame(all_results, columns=['id', 'name', 'lat', 'lng'])


def get_bikes_by_station():
    data = requests.get(
        "https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=1.1.0&outputformat=GEOJSON&request=GetFeature&typename=jcd_jcdecaux.jcdvelov&SRSNAME=urn:ogc:def:crs:EPSG::4171").json()
    props = [x['properties'] for x in data['features']]
    for key in ["titre", "startdate", "enddate", "description", "nature",
                "etat", "langue", "code_insee", "address2", "commune", "nmarrond", "bonus", "pole", "availability", "availabilitycode", "banking", "gid", "last_update_fme"]:
        for dic in props:
            del dic[key]

    df = pd.DataFrame(props)
    return df


def map_popup(stations, live_count, point):
    s = live_count
    res = ("{} <br>"
           "{} places disponibles <br>"
           "{} vélos disponibles <br>"
           "Status: {} <br>"
           "Addresse: {} <br>"
           "Last update: {}").format(
               str(stations['name'][point].encode(
                   'raw_unicode_escape'))[2:-1],
        live_count.loc[live_count["name"] == stations["name"]
                       [point]]["available_bike_stands"].values[0],
        live_count.loc[live_count["name"] == stations["name"]
                       [point]]["available_bikes"].values[0],
        live_count.loc[live_count["name"] ==
                       stations["name"][point]]["status"].values[0],
        str(live_count.loc[live_count["name"] ==
                           stations["name"][point]]["address"].values[0].encode('raw_unicode_escape'))[2:-1],
        live_count.loc[live_count["name"] == stations["name"][point]]["last_update"].values[0])

    return folium.Popup(res, max_width=500)


if __name__ == "__main__":
    app.run(debug=True)
