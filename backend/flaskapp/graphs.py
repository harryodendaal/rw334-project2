from flask import Blueprint, json, request, jsonify, make_response
from .graphs_utils import GraphVisualization

graphs = Blueprint('graphs', __name__)

@graphs.route('/')
def graphs_home():
    graph = GraphVisualization("bolt://184.73.5.16:7687", "neo4j", "proportions-washers-terminations")
    data = graph.call_d3()
    graph.close()
    #data = {'nodes': 'hello'}
    return jsonify(data)

@graphs.route('/shortest-path')
def graphs_shortest_path():
    graph = GraphVisualization("bolt://184.73.5.16:7687", "neo4j", "proportions-washers-terminations")
    data = graph.call_shortest_path()
    graph.close()
    return jsonify(data)

@graphs.route('/label-propagation')
def graphs_label_propagation():
    graph = GraphVisualization("bolt://184.73.5.16:7687", "neo4j", "proportions-washers-terminations")
    data = graph.call_label_propagation()
    graph.close()
    return jsonify(data)

@graphs.route('/centrality')
def graphs_centrality():
    graph = GraphVisualization("bolt://184.73.5.16:7687", "neo4j", "proportions-washers-terminations")
    data = graph.call_centrality()
    graph.close()
    return jsonify(data)