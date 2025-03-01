
class AnnotatedGraphElement:
    """
    Base class for AnnotatedGraphVertex and AnnotatedGraphEdge.
    Attributes:
        id: graph element id;
        attribute:  graph element attribute (float or None);
        is_traversed: this flag equals True if graph element is traversed, False otherwise.
    """
    def __init__(self, element_id=-1, attribute: float | None = None):
        """
        Args:
            element_id: graph element id;
            attribute: graph element attribute value.
        """
        self.id = element_id
        self.attribute = attribute
        self.is_traversed = False


class AnnotatedGraphVertex(AnnotatedGraphElement):
    """
    AnnotatedGraph vertex data storage class.
    Attributes:
        id: graph element id;
        attribute:  graph element attribute value (float or None);
        is_traversed: this flag equals True if graph element is traversed, False otherwise.
    """
    def __init__(self, vertex_id=-1, attribute: float | None = None):
        """
        Args:
            vertex_id: vertex id;
            attribute: vertex attribute.
        """
        super().__init__(vertex_id, attribute)

    def __repr__(self):
        return f'AnnotatedGraphVertex(id={self.id}, attribute={self.attribute})'


class AnnotatedGraphEdge(AnnotatedGraphElement):
    """
    AnnotatedGraph edge data storage class.
    Attributes:
        id: graph element id;
        attribute:  graph element attribute value (float or None);
        is_traversed: this flag is True if graph element had been traversed, False otherwise;
        vertices: edge from -> to vertices ids.
    """
    def __init__(self, edge_id, from_id=-1, to_id=-1, attribute: float | None = None):
        """
        Args:
            edge_id: edge id
            from_id: from vertex id
            to_id: to vertex id
            attribute: edge attribute.
        """
        super().__init__(edge_id, attribute)
        self.vertices = (from_id, to_id)

    def __repr__(self):
        return f'AnnotatedGraphEdge(vertices={self.vertices}, attribute={self.attribute})'


class AnnotatedGraph:
    """
    AnnotatedGraph class.
    Attributes:
        vertices: list of graph vertices (nodes)
        edges: list of graph edges
    """
    def __init__(self, number_vertices: int, edges_list: list):
        """
        Args:
            number_vertices: graph vertices number
            edges_list: graph edges list
        """
        self.vertices = self.__build_vertices(number_vertices)
        self.edges = self.__build_edges(edges_list)

    def __repr__(self):
        return f'AnnotatedGraph(number_vertices={len(self.vertices)}, number_edges={len(self.edges)})'

    def __str__(self):
        vertices_description = [None] * (len(self.vertices) + 1)
        vertices_description[0] = 'Graph vertices:\n'
        for vertex_id, vertex in enumerate(self.vertices):
            vertices_description[vertex_id + 1] = f'\t id={vertex_id}, attribute={vertex.attribute}\n'

        edges_description = [None] * (len(self.edges) + 1)
        edges_description[0] = 'Graph edges:\n'
        for edge_id, edge in enumerate(self.edges):
            edges_description[edge_id + 1] = f'\t id={edge_id}, attribute={edge.attribute}\n'

        return ''.join(vertices_description + edges_description)


    @staticmethod
    def __build_vertices(number_vertices: int) -> list[AnnotatedGraphVertex]:
        """
        Build graph's vertices using ``number_vertices`` value.

        Args:
            number_vertices: graph vertices number.

        Returns: list of vertices
        """
        vertices = [AnnotatedGraphVertex] * number_vertices
        for vertex_index in range(number_vertices):
            vertices[vertex_index] = AnnotatedGraphVertex(vertex_index)
        return vertices


    @staticmethod
    def __build_edges(edges_list: list) -> list[AnnotatedGraphEdge]:
        """
        Build graph's edges using input information list.

        Args:
            edges_list: edges (from, to) data list.

        Returns: list of edges.
        """
        edges_number = len(edges_list)
        edges = [AnnotatedGraphEdge] * edges_number
        for edge_index in range(edges_number):
            edges[edge_index] = AnnotatedGraphEdge(edge_index, edges_list[edge_index][0] - 1, edges_list[edge_index][1] - 1)
        return edges


    def reset_traversal(self) -> None:
        """
        Set all graph's elements attributes to None and is_traversed flag to False.
        """
        for vertex in self.vertices:
            vertex.attribute = None
            vertex.is_traversed = False
        for edge in self.edges:
            edge.attribute = None
            edge.is_traversed = False


    def input_edges(self, vertex: AnnotatedGraphVertex) -> list[AnnotatedGraphEdge]:
        """
        Get all input edges of the given ``vertex``.

        Args:
            vertex: graph vertex

        Returns: list of ``vertex`` input edges.
        """
        input_edges_list = []
        for edge_index in range(len(self.edges)):
            if self.edges[edge_index].vertices[1] == vertex.id:
                input_edges_list.append(self.edges[edge_index])

        return input_edges_list


    def left_node(self, edge: AnnotatedGraphEdge) -> AnnotatedGraphVertex:
        """
        Get left vertex to the given ``edge``.

        Args:
            edge: graph edge

        Returns: graph vertex
        """
        return self.vertices[edge.vertices[0]]