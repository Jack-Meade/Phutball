from unittest                        import TestCase, main
from lib.PlayerClasses.PlayerMinimax import PlayerMinimax
from lib                             import Node, Board

class TestMinimax(TestCase):
    @staticmethod
    def main():
        main()

    def setUp(self):
        pass
    
    def test_minimax_tree1(self):
        root                = PlayerMinimax(Board(5,5))
        root._root.children = [Node(Board(5,5)) for _ in range(3)]

        for child in root._root.children:
            child.children = [Node(Board(5,5)) for _ in range(2)]
        
        #    child       gchild
        root._root.children[0].children[0].value = 5
        root._root.children[0].children[1].value = 7

        root._root.children[1].children[0].value = 1
        root._root.children[1].children[1].value = 3

        root._root.children[2].children[0].value = 9
        root._root.children[2].children[1].value = 4

        root.take_turn(Board(5,5), True, 2, 'heuristic1', True)
        self.assertEqual(root._root.value, 5, "test_minimax_tree1: Root value is not 5")

    def test_minimax_tree2(self):
        root                = PlayerMinimax(Board(5,5))
        root._root.children = [Node(Board(5,5)) for _ in range(3)]

        for child in root._root.children:
            child.children = [Node(Board(5,5)) for _ in range(2)]

            for gchild in child.children:
                gchild.children = [Node(Board(5,5)) for _ in range(2)]

        #    child       gchild      ggchild
        root._root.children[0].children[0].children[0].value = 5
        root._root.children[0].children[0].children[1].value = -1

        root._root.children[0].children[1].children[0].value = 4
        root._root.children[0].children[1].children[1].value = 3

        root._root.children[1].children[0].children[0].value = -10
        root._root.children[1].children[0].children[1].value = -3

        root._root.children[1].children[1].children[0].value = 12
        root._root.children[1].children[1].children[1].value = 7

        root._root.children[2].children[0].children[0].value = -7
        root._root.children[2].children[0].children[1].value = -6

        root._root.children[2].children[1].children[0].value = -8
        root._root.children[2].children[1].children[1].value = -3

        root.take_turn(Board(5,5), True, 3, 'heuristic1', True)
        self.assertEqual(root._root.value, 4, "test_minimax_tree2: Root value is not 4")

    def test_minimax_tree3(self):
        root          = PlayerMinimax(Board(5,5))
        root._root.children = [Node(Board(5,5)) for _ in range(2)]

        for child in root._root.children:
            child.children = [Node(Board(5,5)) for _ in range(2)]

            for gchild in child.children:
                gchild.children = [Node(Board(5,5)) for _ in range(2)]

                for ggchild in gchild.children:
                    ggchild.children = [Node(Board(5,5)) for _ in range(3)]

        #    child       gchild      ggchild     gggchild
        root._root.children[0].children[0].children[0].children[0].value = -4
        root._root.children[0].children[0].children[0].children[1].value = 5
        root._root.children[0].children[0].children[0].children[2].value = -5

        root._root.children[0].children[0].children[1].children[0].value = 10
        root._root.children[0].children[0].children[1].children[1].value = -7
        root._root.children[0].children[0].children[1].children[2].value = 13

        root._root.children[0].children[1].children[0].children[0].value = 13
        root._root.children[0].children[1].children[0].children[1].value = 12
        root._root.children[0].children[1].children[0].children[2].value = 2

        root._root.children[0].children[1].children[1].children[0].value = -7
        root._root.children[0].children[1].children[1].children[1].value = -6
        root._root.children[0].children[1].children[1].children[2].value = -12

        root._root.children[1].children[0].children[0].children[0].value = 10
        root._root.children[1].children[0].children[0].children[1].value = 3
        root._root.children[1].children[0].children[0].children[2].value = 5

        root._root.children[1].children[0].children[1].children[0].value = 7
        root._root.children[1].children[0].children[1].children[1].value = -9
        root._root.children[1].children[0].children[1].children[2].value = -1

        root._root.children[1].children[1].children[0].children[0].value = 1
        root._root.children[1].children[1].children[0].children[1].value = 3
        root._root.children[1].children[1].children[0].children[2].value = 4

        root._root.children[1].children[1].children[1].children[0].value = 4
        root._root.children[1].children[1].children[1].children[1].value = 7
        root._root.children[1].children[1].children[1].children[2].value = 9

        root.take_turn(Board(5,5), True, 4, 'heuristic1', True)
        self.assertEqual(root._root.value, 3, "test_minimax_tree3: Root value is not 3")

if __name__ == "__main__":
    main()
