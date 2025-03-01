from __future__ import annotations
from functools import reduce
from operator import mul
import warnings

from core.annotated_graph import AnnotatedGraph, AnnotatedGraphVertex, AnnotatedGraphEdge


def set_value(graph: AnnotatedGraph, agent_function, element, **kwargs) -> None:
    """
    Set given value to ``element`` attribute.

    Args:
        graph: annotated graph
        agent_function: agent function
        element: graph element to process
        **kwargs: dictionary which has `value` key
    """
    attribute = kwargs.get('value', None)
    element.attribute = attribute


def copy_vertex(graph: AnnotatedGraph, agent_function, element, **kwargs) -> None:
    """
    Copy vertex attribute value to ``element`` attribute.

    Args:
        graph: annotated graph
        agent_function: agent function
        element: graph element
        **kwargs: dictionary which has `vertex_index` key
    """
    vertex_index = kwargs.get('vertex_index', -1)
    if vertex_index < 0 or vertex_index >= len(graph.vertices):
        warnings.warn("Vertex index is incorrect")
        return
    agent_function.process_attribute(graph, graph.vertices[vertex_index])
    element.attribute = graph.vertices[vertex_index].attribute


def copy_edge(graph: AnnotatedGraph, agent_function, element, **kwargs) -> None:
    """
    Copy edge attribute value to ``element`` attribute.

    Args:
        graph: annotated graph
        agent_function: agent function
        element: graph element
        **kwargs: dictionary which has `edge_index` key
    """
    edge_index = kwargs.get('edge_index', -1)
    if edge_index < 0 or edge_index >= len(graph.edges):
        warnings.warn("Edge index is incorrect")
        return
    agent_function.process_attribute(graph, graph.edges[edge_index])
    element.attribute = graph.edges[edge_index].attribute


def multiply(graph: AnnotatedGraph, agent_function, edge, **kwargs) -> None:
    """
    Defined only for edges; вычисляет произведение значений атрибутов левого узла и входящих в него рёбер.

    Args:
        graph: annotated graph
        agent_function: agent function
        edge: graph edge to process
        **kwargs:
    """
    if not isinstance(edge, AnnotatedGraphEdge):
        return
    vertex = graph.left_node(edge)
    agent_function.process_attribute(graph, vertex)
    input_edges = graph.input_edges(vertex)
    [agent_function.process_attribute(graph, edge) for edge in input_edges]
    operands_attributes = [edge.attribute for edge in input_edges]
    operands_attributes.append(vertex.attribute)
    if all(operands_attributes):
        # Check that operands_attributes list has no None values.
        edge.attribute = reduce(mul, operands_attributes)


def minimum(graph: AnnotatedGraph, agent_function, vertex, **kwargs) -> None:
    """
    Defined only for nodes. Вычисляет минимальное значение атрибутов рёбер, входящих в узел;

    Args:
        graph: annotated graph
        agent_function: agent function
        vertex: graph vertex to process
        **kwargs:
    """
    if not isinstance(vertex, AnnotatedGraphVertex): return
    input_edges = graph.input_edges(vertex)
    if not len(input_edges): return
    [agent_function.process_attribute(graph, edge) for edge in input_edges]
    edges_attributes = [edge.attribute for edge in input_edges]
    if all(edges_attributes):
        # Check that edges_attributes list has no None values.
        vertex.attribute = min(edges_attributes)
