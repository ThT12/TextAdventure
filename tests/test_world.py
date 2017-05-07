from unittest import TestCase
from unittest.mock import patch
import random

from textadventure.world import World
from textadventure.directions import Direction


class TestWorld(TestCase):
    def setUp(self):
        self.my_world = World(init_x_pos=1, init_y_pos=2)

    def test_get_room_after_move_N(self):
        new_room = self.my_world.get_room_after_move(direction=Direction.NORTH)
        self.assertEqual(new_room, self.my_world.room_table[2, 2])

    def test_get_room_after_move_S(self):
        new_room = self.my_world.get_room_after_move(direction=Direction.SOUTH)
        self.assertEqual(new_room, self.my_world.room_table[0, 2])

    def test_get_room_after_move_E(self):
        new_room = self.my_world.get_room_after_move(direction=Direction.EAST)
        self.assertEqual(new_room, self.my_world.room_table[1, 3])

    def test_get_room_after_move_W(self):
        new_room = self.my_world.get_room_after_move(direction=Direction.WEST)
        self.assertEqual(new_room, self.my_world.room_table[1, 1])


class TestGame(TestCase):
    def setUp(self):
        self.my_world = World()

    @patch('builtins.input')
    def test_win(self, mock_input):
        mock_input.side_effect = ['W', 'W', 'E', 'E', 'E', 1, 'W', 'N', 'N', 'E', 'N', 'S', 'W', 'W', 2, 'W', 'S', 3]
        self.my_world.run_game()

    @patch('builtins.input')
    def test_loose(self, mock_input):
        mock_input.side_effect = ['N', 'N', 'W', 1]
        self.my_world.run_game()


class TestWorldGenerator(TestCase):
    def test_init_default_word(self):
        my_world = World()
        world_size = my_world.init_default_word(lvl=1)
        len_world = 4
        self.assertEqual(world_size, [len_world, len_world])
        self.assertEqual(my_world.room_table.shape, (len_world, len_world))

    def test_init_hero_pos(self):
        random.seed(1)
        my_world = World()
        world_size = my_world.init_default_word(lvl=1)
        hero_pos = my_world.init_hero_pos(nb_col=world_size[0])
        exp_x = 0
        exp_y = 1
        self.assertEqual(my_world.hero.current_room, my_world.room_table[exp_x, exp_y])
        self.assertEqual(hero_pos, [exp_x, exp_y])
