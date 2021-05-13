from flaskapp.auth import token_required
from flask import Blueprint, json, request, jsonify, make_response
from .graphs_utils import GraphVisualization
from . import config

graphs = Blueprint('graphs', __name__)


@token_required
@graphs.route('/')
def graphs_home():
    graph = GraphVisualization(config.NEO4J_URL, config.NEO4J_USERNAME, config.NEO4J_PASSWORD)
    data = graph.call_d3()
    graph.close()
    #data = {'nodes': 'hello'}
    return jsonify(data)


@token_required
@graphs.route('/shortest-path')
def graphs_shortest_path():
    graph = GraphVisualization(config.NEO4J_URL, config.NEO4J_USERNAME, config.NEO4J_PASSWORD)
    data = graph.call_shortest_path()
    graph.close()
    return jsonify(data)


@token_required
@graphs.route('/label-propagation')
def graphs_label_propagation():
    graph = GraphVisualization(config.NEO4J_URL, config.NEO4J_USERNAME, config.NEO4J_PASSWORD)
    data = graph.call_label_propagation()
    graph.close()
    return jsonify(data)


@token_required
@graphs.route('/centrality')
def graphs_centrality():
    graph = GraphVisualization(config.NEO4J_URL, config.NEO4J_USERNAME, config.NEO4J_PASSWORD)
    data = graph.call_centrality()
    graph.close()
    return jsonify(data)

# "MATCH (e1:Employee {emailaddress: \"ermis-f@enron.com\"}), (e2:Employee {emailaddress: \"lokey-t@enron.com\"}) "
#                         "CALL gds.beta.shortestPath.dijkstra.stream({ "
#                         "nodeQuery: 'MATCH (e:Employee) RETURN id(e) as id', "
#                         "relationshipQuery: 'MATCH (e3:Employee)-[r:EMAILS]-(e4:Employee) RETURN id(e3) as source, id(e4) as target, r.amount as weight', "
#                         "sourceNode: id(e1), "
#                         "targetNode: id(e2)}) "
#                         "YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs "
#                         "RETURN gds.util.asNode(sourceNode).emailaddress AS sourceNodeName, gds.util.asNode(targetNode).emailaddress AS targetNodeName, [nodeId IN nodeIds | nodeId] AS node_Ids, costs "
#                         "ORDER BY index"

# MATCH (e1:Employee {emailaddress: "ybarbo-p@enron.com"}), (e2:Employee {emailaddress: "pimenov-v@enron.com"}) 
# CALL example.Djikstra(e1, e2) 
# YIELD nodes,distances 
# RETURN nodes,distances