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
    def setUp(self):
        self.my_world = World()
        self.world_size = self.my_world.init_default_word(lvl=1)

    def test_init_default_word(self):
        len_world = 4
        self.assertEqual(self.world_size, [len_world, len_world])
        self.assertEqual(self.my_world.room_table.shape, (len_world, len_world))

    def test_init_hero_pos(self):
        random.seed(1)
        hero_pos = self.my_world.init_hero_pos(nb_col=self.world_size[0])
        exp_x = 0
        exp_y = 1
        self.assertEqual(self.my_world.hero.current_room, self.my_world.room_table[exp_x, exp_y])
        self.assertEqual(hero_pos, [exp_x, exp_y])

    def test_init_win_pos(self):
        random.seed(1)
        win_pos = self.my_world.init_win_pos(self.world_size)
        exp_x = 3
        exp_y = 1
        self.assertTrue(self.my_world.room_table[exp_x, exp_y].is_win)
        self.assertEqual(win_pos, [exp_x, exp_y])

    def test_build_main_way(self):
        random.seed(4)
        hero_init_pos = [0, 0]
        self.my_world.hero.current_room = self.my_world.room_table[hero_init_pos[0], hero_init_pos[1]]
        win_pos = [3, 3]
        self.my_world.room_table[win_pos[0], win_pos[1]].is_win = True
        list_room_way = self.my_world.build_main_way()
        self.assertTrue(list_room_way[1], [0, 0])
        self.assertTrue((list_room_way[-1], [3, 3]))


class TestIsInsideWorld(TestCase):
    def setUp(self):
        self.my_world = World()

    def test_is_inside_world_true(self):
        pos = [2, 3]
        self.assertTrue(self.my_world.is_inside_world(pos))

    def test_is_inside_world_false_x_inf_0(self):
        pos = [-1, 3]
        self.assertFalse(self.my_world.is_inside_world(pos))

    def test_is_inside_world_false_y_inf_0(self):
        pos = [2, -1]
        self.assertFalse(self.my_world.is_inside_world(pos))

    def test_is_inside_world_false_x_sup_max(self):
        pos = [4, 3]
        self.assertFalse(self.my_world.is_inside_world(pos))

    def test_is_inside_world_false_y_sup_max(self):
        pos = [2, 4]
        self.assertFalse(self.my_world.is_inside_world(pos))
