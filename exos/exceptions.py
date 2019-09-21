"""
exceptions module
"""

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'


class NonExhaustivePattern(Exception):
    """
    Thrown when pattern matching fails to find a matching predicate.
    """
    pass
