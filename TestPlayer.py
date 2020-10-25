from unittest             import TestCase, main
from PlayerClasses.Player import Player
from Board                import Board

class TestPlayer(TestCase):
    def setUp(self):
        pass       

    def test_place_players(self):
        test_board = Board(False)

        expected_result = [
            {
                'board': [
                    [3,3,3,3,3],
                    [0,2,3,3,0],
                    [0,5,1,5,0],
                    [0,4,4,4,0],
                    [4,4,4,4,4]
                ],
                'ball': {'x' : 2, 'y' : 2}
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,3,2,3,0],
                    [0,5,1,5,0],
                    [0,4,4,4,0],
                    [4,4,4,4,4]
                ],
                'ball': {'x' : 2, 'y' : 2}
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,3,3,2,0],
                    [0,5,1,5,0],
                    [0,4,4,4,0],
                    [4,4,4,4,4]
                ],
                'ball': {'x' : 2, 'y' : 2}
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,3,3,3,0],
                    [0,2,1,5,0],
                    [0,4,4,4,0],
                    [4,4,4,4,4]
                ],
                'ball': {'x' : 2, 'y' : 2}
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,3,3,3,0],
                    [0,5,1,2,0],
                    [0,4,4,4,0],
                    [4,4,4,4,4]
                ],
                'ball': {'x' : 2, 'y' : 2}
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,3,3,3,0],
                    [0,5,1,5,0],
                    [0,2,4,4,0],
                    [4,4,4,4,4]
                ],
                'ball': {'x' : 2, 'y' : 2}
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,3,3,3,0],
                    [0,5,1,5,0],
                    [0,4,2,4,0],
                    [4,4,4,4,4]
                ],
                'ball': {'x' : 2, 'y' : 2}
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,3,3,3,0],
                    [0,5,1,5,0],
                    [0,4,4,2,0],
                    [4,4,4,4,4]
                ],
                'ball': {'x' : 2, 'y' : 2}
            },
        ]
            
        self.assertEqual(Player.place_players(test_board), expected_result, "Player.place_players() invalid")

    def test_kick_ball(self):
        test_board = Board(False)
        test_board.update(1, 1, "player")
        test_board.update(3, 1, "player")
        test_board.update(1, 3, "player")
        test_board.update(2, 3, "player")

        expected_result = [
            {
                'board': [
                    [1,3,3,3,3],
                    [0,3,3,2,0],
                    [0,5,5,5,0],
                    [0,2,2,4,0],
                    [4,4,4,4,4]  
                ],
                'ball': {'x' : 0, 'y' : 0 }
            },
            {
                'board': [
                    [3,3,3,3,1],
                    [0,2,3,3,0],
                    [0,5,5,5,0],
                    [0,2,2,4,0],
                    [4,4,4,4,4]
                ],
                'ball': {'x' : 4, 'y' : 0 }
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,2,3,2,0],
                    [0,5,5,5,0],
                    [0,4,2,4,0],
                    [1,4,4,4,4]
                ],
                'ball': {'x' : 0, 'y' : 4 }
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,2,3,2,0],
                    [0,5,5,5,0],
                    [0,2,4,4,0],
                    [4,4,1,4,4]
                ],
                'ball': {'x' : 2, 'y' : 4 }
            }
        ]
        
        self.assertEqual(Player.kick_ball(test_board), expected_result, "Player.kick_ball() Invalid")

    def test_get_successors(self):
        test_board = Board(False)
        test_board.update(1, 1, "player")

        expected_result = [
            {
                'board': [
                    [3,3,3,3,3],
                    [0,2,2,3,0],
                    [0,5,1,5,0],
                    [0,4,4,4,0],
                    [4,4,4,4,4]  
                ],
                'ball': {'x' : 2, 'y' : 2 }
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,2,3,2,0],
                    [0,5,1,5,0],
                    [0,4,4,4,0],
                    [4,4,4,4,4]  
                ],
                'ball': {'x' : 2, 'y' : 2 }
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,2,3,3,0],
                    [0,2,1,5,0],
                    [0,4,4,4,0],
                    [4,4,4,4,4]  
                ],
                'ball': {'x' : 2, 'y' : 2 }
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,2,3,3,0],
                    [0,5,1,2,0],
                    [0,4,4,4,0],
                    [4,4,4,4,4]  
                ],
                'ball': {'x' : 2, 'y' : 2 }
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,2,3,3,0],
                    [0,5,1,5,0],
                    [0,2,4,4,0],
                    [4,4,4,4,4]  
                ],
                'ball': {'x' : 2, 'y' : 2 }
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,2,3,3,0],
                    [0,5,1,5,0],
                    [0,4,2,4,0],
                    [4,4,4,4,4]  
                ],
                'ball': {'x' : 2, 'y' : 2 }
            },
            {
                'board': [
                    [3,3,3,3,3],
                    [0,2,3,3,0],
                    [0,5,1,5,0],
                    [0,4,4,2,0],
                    [4,4,4,4,4]  
                ],
                'ball': {'x' : 2, 'y' : 2 }
            },
            {
                'board': [
                    [1,3,3,3,3],
                    [0,3,3,3,0],
                    [0,5,5,5,0],
                    [0,4,4,4,0],
                    [4,4,4,4,4]  
                ],
                'ball': {'x' : 0, 'y' : 0 }
            }
        ]

        self.assertEqual(Player.get_successes(test_board), expected_result, "Player.get_successes() Invalid")

if __name__ == '__main__':
    main()
