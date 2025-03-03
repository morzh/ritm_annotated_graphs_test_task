from core.annotated_graph import AnnotatedGraph, AnnotatedGraphVertex, AnnotatedGraphEdge, AnnotatedGraphElement
from core.agent_function_rules_factory import agent_rules_factory


class AgentFunction:
    """
    Agent function class.
    """
    def __init__(self, agent_rules: list[tuple], number_vertices: int):
        self.vertices_rules = [None] * number_vertices
        self.edges_rules = [None] * (len(agent_rules) - number_vertices)
        self.__fill_rules(agent_rules, number_vertices)


    def __fill_rules(self, agent_function_rules: list, number_vertices: int) -> None:
        """
        Stores list of rules to two different lists. First for vertices and second for edges.
        Args:
            agent_function_rules:  list of agent function rules;
            number_vertices: number graph vertices
        """
        self.vertices_rules = agent_function_rules[:number_vertices]
        self.edges_rules = agent_function_rules[number_vertices:]


    def process_attribute(self, graph: AnnotatedGraph, graph_element: AnnotatedGraphElement) -> None:
        """
        Process ``graph_element`` according to ``agent_function`` rules.
        Args:
            graph:
            graph_element: graph vertex or edge
        """
        if graph_element.attribute is None:
            if isinstance(graph_element, AnnotatedGraphVertex):
                agent_command = self.vertices_rules[graph_element.id]
            elif isinstance(graph_element, AnnotatedGraphEdge):
                agent_command = self.edges_rules[graph_element.id]
            else:
                return

            agent_atom = agent_rules_factory.get(agent_command[0])
            agent_atom(graph, self, graph_element, **agent_command[1])
            graph_element.is_traversed = True


    def traverse_graph_attributes(self, graph: AnnotatedGraph) -> None:
        """
        Traverse annotated graph attributes.

        Args:
            graph: annotated graph
        """
        graph.reset_traversal()
        for vertex in graph.vertices:
            if vertex.is_traversed: continue
            self.process_attribute(graph, vertex)

        for edge in graph.edges:
            if edge.is_traversed: continue
            self.process_attribute(graph, edge)

