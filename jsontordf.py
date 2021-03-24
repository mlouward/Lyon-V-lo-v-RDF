import json
import sys
import urllib.request

from rdflib import RDF, RDFS, Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import FOAF, XSD
from rdflib.plugins.stores import sparqlstore

# Bicycles namespace
n = Namespace(
    'http://www.semanticweb.org/maxime/ontologies/2021/2/untitled-ontology-16#BicycleStand/')
# Root namespace
r = Namespace(
    'http://www.semanticweb.org/maxime/ontologies/2021/2/untitled-ontology-16#')


def get_json_data():
    # Gets the JSON data of bikes in Lyon
    with urllib.request.urlopen("https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=1.1.0&outputformat=GEOJSON&request=GetFeature&typename=jcd_jcdecaux.jcdvelov&SRSNAME=urn:ogc:def:crs:EPSG::4171") as url:
        data = json.loads(url.read().decode())
    return data


def json_to_graph(json_data, ontology):
    # Converts JSON data into a RDFLib graph

    # Create an empty graph, and add our initial ontology
    # for geolocated resources
    g = Graph(
        identifier='http://www.semanticweb.org/maxime/ontologies/2021/2/untitled-ontology-16#BicycleStand/')
    g2 = g.parse(location=ontology)
    # Bind the root namespace to prefix ex
    g2.bind('ex', r)

    print("Nb de stations:", len(json_data['features']))
    for station in json_data['features']:
        station_props = station['properties']
        g2.add((
            URIRef(r[station_props['number']]),
            URIRef(RDF.type),
            URIRef(r.BicycleStand)
        ))
        g2.add((
            r[station_props['number']],
            n.name,
            Literal(station_props['name'], datatype=XSD.string)
        ))
        g2.add((
            r[station_props['number']],
            n.id,
            Literal(station_props['number'], datatype=XSD.int)
        ))
        g2.add((
            r[station_props['number']],
            n.lat,
            Literal(station_props['lat'], datatype=XSD.double)
        ))
        g2.add((
            r[station_props['number']],
            n.lng,
            Literal(station_props['lng'], datatype=XSD.double)
        ))

    return g2


def my_bnode_ext(node):
    # Create a named node from a blank node
    if isinstance(node, BNode):
        return '<bnode:b%s>' % node
    return sparqlstore._node_to_sparql(node)


if __name__ == '__main__':
    json_data = get_json_data()

    # Populate the graph from JSON
    graph = json_to_graph(json_data, ontology='BicycleStands.owl')
    print("Nb de triples:", len(graph))

    graph.serialize(destination='output.ttl', format='turtle')

    query_endpoint = 'http://localhost:3030/ds/query'
    update_endpoint = 'http://localhost:3030/ds/update'
    store = sparqlstore.SPARQLUpdateStore(node_to_sparql=my_bnode_ext)
    store.open((query_endpoint, update_endpoint))

    for (s, p, o) in graph:
        store.add((s, p, o))
