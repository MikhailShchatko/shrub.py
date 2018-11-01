import abc
import collections


RECURSE_KEY = "recurse"
NAME_KEY = "name"


class EvergreenBuilder:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _yaml_map(self):
        """A map of values to yaml decorators."""

    @abc.abstractmethod
    def to_map(self):
        """Convert this object to a pythonic map."""

    def _add_if_defined(self, obj, prop):
        """Add the specified property to the given object if it exists."""
        value = getattr(self, prop)
        if value:
            if self._yaml_map()[prop][RECURSE_KEY]:
                if isinstance(value, collections.Sequence):
                    value = [v.to_map() for v in value]
                else:
                    value = value.to_map()
            obj[self._yaml_map()[prop][NAME_KEY]] = value

    def _add_defined_attribs(self, obj, attrib_list):
        """Add any defined attributes in the given list to the given map."""
        for attrib in attrib_list:
            self._add_if_defined(obj, attrib)
