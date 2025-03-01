import re
from pathlib import Path
from core.annotated_graph import AnnotatedGraph
from core.agent_function import AgentFunction


class DataProvider:
    """
    Data provider class for agent function rules and annotated graph definition.
    """
    @staticmethod
    def get(description_filename: Path) -> tuple[AnnotatedGraph, AgentFunction]:
        """
        Get annotated graph and agent function  classes according to  data, provided in ``description_filename``.
        Args:
            description_filename: filename with problem text description

        Returns: annotated graph and agent function.
        """
        with open(description_filename) as file:
            content = file.read()

        sections =  DataProvider.__split_on_empty_lines(content)

        if not len(sections) == 3:
            raise IOError('Wrong input file data structure')

        number_vertices, number_edges = DataProvider.__parse_number_elements(sections[0])
        edges_list = DataProvider.__parse_edges_section(sections[1])

        if not number_edges == len(edges_list):
            raise IOError('Error processing edges.')
        agent_instructions = DataProvider.__parse_agent_instructions(sections[2])

        if not len(agent_instructions) == number_vertices + number_edges:
            raise IOError(f'Number of agent function instructions should be {number_vertices + number_edges}')
        agent_commands = DataProvider.__convert_instructions_to_commands(agent_instructions)

        return AnnotatedGraph(number_vertices, edges_list), AgentFunction(agent_commands, number_vertices)


    @staticmethod
    def __split_on_empty_lines(string: str) -> list[str]:
        """
        Split string by empty line(s).
        Args:
            string: input string

        Returns: list of strings
        """
        # greedily match 2 or more new-lines
        blank_line_regex = r"(?:\r?\n){2,}"
        return re.split(blank_line_regex, string.strip())


    @staticmethod
    def __parse_number_elements(string: str) -> tuple[int, int]:
        """
        Parse string with vertices and edges number.

        Args:
            string: string to parse.

        Returns: tuple with vertices and edges number.
        """
        elements = string.split('#')[0].strip().split(' ')
        if not len(elements) == 2:
            raise ImportError('Wrong vertices or edges number data.')
        return int(elements[0]), int(elements[1])


    @staticmethod
    def __parse_edges_section(string: str) -> list[tuple[int, int]]:
        """
        Parse text edges description.

        Args:
            string: input string to parse

        Returns: edges (from, to) data list
        """
        lines = string.split('\n')
        edges = [line.split('#')[0].strip().split(' ') for line in lines]
        edges = [tuple(map(int, edge)) for edge in edges]
        edges_checks = [len(array) == 2 for array in edges]
        if not all(edges_checks) == True:
            raise IOError('Error reading edges data.')
        return edges


    @staticmethod
    def __parse_agent_instructions(string: str) -> list[str]:
        """
        Parse agent function rules.

        Args:
            string: input string to parse.

        Returns: list of text commands.
        """
        lines = string.split('\n')
        agent_text_rules = [line.split('#')[0].strip() for line in lines]
        return agent_text_rules


    @staticmethod
    def __convert_instructions_to_commands(agent_rules: list[str]) -> list[tuple[str, dict]]:
        """
        Convert list of agent function text rules to a representation, suitable for factory method.

        Args:
            agent_rules: list of agent function text rules

        Returns: list of agent function rules.
        """
        convertion_result = []
        for instruction in agent_rules:
            if DataProvider.__is_number(instruction):
                command = ('set', {'value': float(instruction)})
            elif instruction.startswith('e'):
                command = ('copy_edge', {'edge_index': int(instruction.split(' ')[1]) - 1})
            elif  instruction.startswith('v'):
                command = ('copy_vertex', {'vertex_index': int(instruction.split(' ')[1]) - 1})
            elif instruction.startswith('*'):
                command = ('mult', {})
            elif instruction.startswith('min'):
                command = ('min', {})
            else:
                command = ('', {})

            convertion_result.append(command)
        return convertion_result


    @staticmethod
    def __is_number(string: str) -> bool:
        """
        Checks if string is a number.

        Args:
            string: input string/

        Returns: True is ``string`` is a number, False otherwise/
        """
        try:
            float(string)
            return True
        except ValueError:
            return False
