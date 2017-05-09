from unittest import TestCase
from unittest.mock import patch

from textadventure.directions import Direction
from textadventure.obj import Obj
from textadventure.room import Room
from textadventure.enemy import Enemy


class TestActionRoom(TestCase):
    def setUp(self):
        self.my_room = Room()

    @patch('builtins.input', lambda: 'N')
    def test_action_room_N(self):
        self.assertEqual(self.my_room.action_room(), Direction.NORTH)

    @patch('builtins.input', lambda: 'North')
    def test_action_room_North(self):
        self.assertEqual(self.my_room.action_room(), Direction.NORTH)

    @patch('builtins.input', lambda: 'S')
    def test_action_room_S(self):
        self.assertEqual(self.my_room.action_room(), Direction.SOUTH)

    @patch('builtins.input', lambda: 'South')
    def test_action_room_South(self):
        self.assertEqual(self.my_room.action_room(), Direction.SOUTH)

    @patch('builtins.input', lambda: 'E')
    def test_action_room_E(self):
        self.assertEqual(self.my_room.action_room(), Direction.EAST)

    @patch('builtins.input', lambda: 'East')
    def test_action_room_East(self):
        self.assertEqual(self.my_room.action_room(), Direction.EAST)

    @patch('builtins.input', lambda: 'W')
    def test_action_room_W(self):
        self.assertEqual(self.my_room.action_room(), Direction.WEST)

    @patch('builtins.input', lambda: 'West')
    def test_action_room_West(self):
        self.assertEqual(self.my_room.action_room(), Direction.WEST)


class TestActionRoomTwice(TestCase):
    def setUp(self):
        self.my_room = Room(directions=[Direction.WEST, Direction.NORTH])

    @patch('builtins.input')
    def test_ask_direction_unknown_direction(self, mock_input):
        mock_input.side_effect = ['B', 'N']
        self.assertEqual(self.my_room.action_room(), Direction.NORTH)

    @patch('builtins.input')
    def test_ask_direction_blocked_direction(self, mock_input):
        mock_input.side_effect = ['E', 'N']
        self.assertEqual(self.my_room.action_room(), Direction.NORTH)

    @patch('builtins.input')
    def test_ask_direction_first_direction(self, mock_input):
        mock_input.side_effect = ['W', 'N']
        self.assertEqual(self.my_room.action_room(), Direction.WEST)


class TestRoom(TestCase):
    def test_delete_key(self):
        my_room = Room(obj_in_room=Obj())
        my_room.delete_obj()
        self.assertIsNone(my_room.obj_in_room)

    def test_delete_enemy(self):
        my_room = Room(enemy=Enemy())
        my_room.delete_enemy()
        self.assertIsNone(my_room.enemy)

    def test_delete_condition_to_enter(self):
        my_room = Room(condition_to_enter=Obj())
        my_room.delete_condition_to_enter()
        self.assertIsNone(my_room.condition_to_enter)

    def test_sort_direction(self):
        my_room = Room(directions=[Direction.SOUTH, Direction.NORTH, Direction.WEST, Direction.EAST])
        my_room.sort_direction()
        self.assertEqual(my_room.directions, [Direction.WEST, Direction.NORTH, Direction.EAST, Direction.SOUTH])
