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
        root          = Node(Board(False))
        root.children = [Node(Board(False)) for _ in range(3)]

        for child in root.children:
            child.children = [Node(Board(False)) for _ in range(2)]
        
        #    child       gchild
        root.children[0].children[0].value = 5
        root.children[0].children[1].value = 7

        root.children[1].children[0].value = 1
        root.children[1].children[1].value = 3

        root.children[2].children[0].value = 9
        root.children[2].children[1].value = 4

        root.value = PlayerMinimax._minimax(root, 2, float('-inf'), float('inf'), True)
        self.assertEqual(root.value, 5, "test_minimax_tree1: Root value is not 5")

    def test_minimax_tree2(self):
        root          = Node(Board(False))
        root.children = [Node(Board(False)) for _ in range(3)]

        for child in root.children:
            child.children = [Node(Board(False)) for _ in range(2)]

            for gchild in child.children:
                gchild.children = [Node(Board(False)) for _ in range(2)]

        #    child       gchild      ggchild
        root.children[0].children[0].children[0].value = 5
        root.children[0].children[0].children[1].value = -1

        root.children[0].children[1].children[0].value = 4
        root.children[0].children[1].children[1].value = 3

        root.children[1].children[0].children[0].value = -10
        root.children[1].children[0].children[1].value = -3

        root.children[1].children[1].children[0].value = 12
        root.children[1].children[1].children[1].value = 7

        root.children[2].children[0].children[0].value = -7
        root.children[2].children[0].children[1].value = -6

        root.children[2].children[1].children[0].value = -8
        root.children[2].children[1].children[1].value = -3

        root.value = PlayerMinimax._minimax(root, 3, float('-inf'), float('inf'), True)
        self.assertEqual(root.value, 4, "test_minimax_tree2: Root value is not 4")

    def test_minimax_tree3(self):
        root          = Node(Board(False))
        root.children = [Node(Board(False)) for _ in range(2)]

        for child in root.children:
            child.children = [Node(Board(False)) for _ in range(2)]

            for gchild in child.children:
                gchild.children = [Node(Board(False)) for _ in range(2)]

                for ggchild in gchild.children:
                    ggchild.children = [Node(Board(False)) for _ in range(3)]

        #    child       gchild      ggchild     gggchild
        root.children[0].children[0].children[0].children[0].value = -4
        root.children[0].children[0].children[0].children[1].value = 5
        root.children[0].children[0].children[0].children[2].value = -5

        root.children[0].children[0].children[1].children[0].value = 10
        root.children[0].children[0].children[1].children[1].value = -7
        root.children[0].children[0].children[1].children[2].value = 13

        root.children[0].children[1].children[0].children[0].value = 13
        root.children[0].children[1].children[0].children[1].value = 12
        root.children[0].children[1].children[0].children[2].value = 2

        root.children[0].children[1].children[1].children[0].value = -7
        root.children[0].children[1].children[1].children[1].value = -6
        root.children[0].children[1].children[1].children[2].value = -12

        root.children[1].children[0].children[0].children[0].value = 10
        root.children[1].children[0].children[0].children[1].value = 3
        root.children[1].children[0].children[0].children[2].value = 5

        root.children[1].children[0].children[1].children[0].value = 7
        root.children[1].children[0].children[1].children[1].value = -9
        root.children[1].children[0].children[1].children[2].value = -1

        root.children[1].children[1].children[0].children[0].value = 1
        root.children[1].children[1].children[0].children[1].value = 3
        root.children[1].children[1].children[0].children[2].value = 4

        root.children[1].children[1].children[1].children[0].value = 4
        root.children[1].children[1].children[1].children[1].value = 7
        root.children[1].children[1].children[1].children[2].value = 9

        root.value = PlayerMinimax._minimax(root, 4, float('-inf'), float('inf'), True)
        self.assertEqual(root.value, 3, "test_minimax_tree3: Root value is not 3")

    def test_build_tree1(self):
        test_root = Node(Board(False))
        test_root = PlayerMinimax._build_tree(test_root, 1)

        expected_root          = Node(Board(False))
        expected_root.children = [Node(Board(False)) for _ in range(8)]

        expected_root.children[0].board.update(1, 1, "player")
        expected_root.children[1].board.update(1, 2, "player")
        expected_root.children[2].board.update(1, 3, "player")
        expected_root.children[3].board.update(2, 1, "player")
        expected_root.children[4].board.update(2, 3, "player")
        expected_root.children[5].board.update(3, 1, "player")
        expected_root.children[6].board.update(3, 2, "player")
        
        self.assertNotEqual(test_root, expected_root, "test_build_tree1: Trees are equal")

        expected_root.children[7].board.update(3, 3, "player")

        self.assertEqual(test_root, expected_root, "test_build_tree1: Trees are not equal")

if __name__ == "__main__":
    main()
