from pathlib import Path
from core.data_provider import DataProvider


if __name__ == '__main__':
    filename_problem_description = Path('input_data/graph_agent_problem.txt')
    annotated_graph, agent_function = DataProvider.get(filename_problem_description.absolute())
    agent_function.traverse_graph_attributes(annotated_graph)
    print(annotated_graph)
