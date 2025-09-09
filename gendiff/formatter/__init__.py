from gendiff.formatter.diff import get_diff
from gendiff.formatter.linear import generate_linear_diff as linear
from gendiff.formatter.plain import plain
from gendiff.formatter.stylish import stylish

__all__ = (
    "get_diff",
    "plain",
    "stylish",
    "linear"
)
