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

2. Launch the Python server in ./server_flask/

`python server.py`

3. Go to `localhost:5000`

You can see the list of bike stations on the map and their information, as well as the current weather
Clicking on a station on the map will show:

- Station location on the map
- Station Name
- Station Address
- Number of available bikes
- Number of parking spots
- Time of last update

The information is updated when refreshing the page
