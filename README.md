Lyon Vélo'V Real-time data
-----

###### TODO: 
- ###### Add a docker image to do the setup programatically
- ###### Change Flask to debug False

## Instructions
-----
1. Launch a Fuseki server with a dataset called *ds*

Default port should be 3030:
`.\fuseki-server.bat --update --mem /ds`

2. Launch the Python server

`python server.py`

3. Go to `localhost:5000`

Click on Geomap to get to the information on the stations

- Station location on the map
- Station Name
- Station Address
- Number of available bikes
- Number of parking spots
- Time of last update

The information is updated when refreshing the page
