from collections import Counter

class Node(object):
    def __init__(self, board):
        self._children = []
        self._value    = None
        self._board    = board

    def __hash__(self):
        return hash((str(self._board.state), str(self._value), str(self._children)))

    def __eq__(self, other):
        b = self._board == other.board
        v = self._value == other.value
        c = set(self._children) - set(other.children)
        return b and v and not c

    def __gt__(self, other):
        return self._value > other.value

    def _get_children(self):
        return self._children
    def _set_children(self, children):
        self._children = children

    def _get_value(self):
        return self._value
    def _set_value(self, value):
        self._value = value

    def _get_board(self):
        return self._board
    def _set_board(self, board):
        self._board = board

    children = property(_get_children, _set_children)
    value    = property(_get_value, _set_value)
    board    = property(_get_board)

    def is_terminal(self):
        return self.board.ball["y"] <= 1 or self.board.ball["y"] >= len(self._board)-2