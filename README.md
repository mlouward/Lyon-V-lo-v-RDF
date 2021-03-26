Lyon Vélo'V Real-time data
-----

###### TODO: 
- ###### ~~Add a docker image to do the setup programatically~~
  - Not possible with stains/jena-fuseki docker image (needs authentication with random password else can't update dataset)
- ###### ~~Change Flask to debug False~~

## Instructions
-----
1. Launch a Fuseki server with a dataset called *ds*

Default port should be 3030:
`.\fuseki-server.bat --update --mem /ds`

2. Install python libraries

`pip install -r requirements.txt`

3. Load static data into the triplestore

Run `python jsontordf.py` in folder ./load_graph

4. Launch the Python server in folder ./server_flask

`python server.py`

5. Go to [localhost:5000](http://localhost:5000)

You can see the list of bike stations and their information, as well as the current weather
Clicking on a station on the map will show:

- Station location on the map
- Station Name
- Station Address
- Number of available bikes
- Number of parking spots
- Time of last update

The information is updated when refreshing the page
