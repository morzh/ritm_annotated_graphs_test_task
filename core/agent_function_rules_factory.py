from core.agent_function_rules import  *
import typing

class AgentFunctionFactory:
    """
    This class serves as a factory in a factory pattern.
    Attributes:
        _builders: dictionary with registered functions.
    """
    def __init__(self):
        """
        Initialize empty _builders dictionary.
        """
        self._builders = {}

    def register(self, key: str, builder: typing.Callable) -> None:
        """
        Register factory subject builder. Builder creates class, initialized with parameters.

        Args:
            key: class alias key
            builder: subject class builder
        """
        self._builders[key] = builder

    def get(self, key: str, **kwargs) -> typing.Callable:
        """
        Create initialized subject with the given key word parameters

        Args:
            key: subject class key in builders dictionary or class string alias

        :return: function reference
        """
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(f'Model type {key} is not supported.')
        return builder


agent_rules_factory = AgentFunctionFactory()
agent_rules_factory.register('set', set_value)
agent_rules_factory.register('copy_vertex', copy_vertex)
agent_rules_factory.register('copy_edge', copy_edge)
agent_rules_factory.register('mult', multiply)
agent_rules_factory.register('min', minimum)
