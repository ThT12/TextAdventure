from unittest import TestCase
from unittest.mock import patch
import random

from textadventure.world import World, find_direction
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
        self.my_world.init_default_word(lvl=1)

    def test_init_default_word(self):
        len_world = 4
        self.assertEqual(self.my_world.world_size, [len_world, len_world])
        self.assertEqual(self.my_world.room_table.shape, (len_world, len_world))

    def test_init_hero_pos(self):
        random.seed(1)
        hero_pos = self.my_world.init_hero_pos(nb_col=self.my_world.world_size[0])
        exp_x = 0
        exp_y = 1
        self.assertEqual(self.my_world.hero.current_room, self.my_world.room_table[exp_x, exp_y])
        self.assertEqual(hero_pos, [exp_x, exp_y])

    def test_init_win_pos(self):
        random.seed(1)
        win_pos = self.my_world.init_win_pos(self.my_world.world_size)
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
        diff = []
        for i in range(len(list_room_way)-1):
            diff.append(sum([abs(x - y) for x, y in zip(list_room_way[i], list_room_way[i+1])]))
        self.assertEqual(diff, [1] * len(diff))
        self.assertTrue(list_room_way[1], [0, 0])
        self.assertTrue((list_room_way[-1], [3, 3]))

    @patch.object(World, "is_inside_world")
    def test_find_available_mod(self, mock_is_inside_world):
        mock_is_inside_world.side_effect = [True, True, False]
        mod_available = self.my_world.find_available_mod([0, 1], [[1, 1]])
        self.assertEqual(mod_available, [[-1, 0], [0, 1]])

    @patch("textadventure.world.find_direction")
    def test_apply_way(self, mock_find_direction):
        mock_find_direction.side_effect = [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST,
                                           Direction.NORTH, Direction.SOUTH]
        way = [[0, 0], [1, 0], [2, 0], [2, 1]]
        self.my_world.room_table[0, 0].directions = [Direction.SOUTH]
        self.my_world.room_table[1, 0].directions = [Direction.WEST]
        self.my_world.room_table[2, 0].directions = [Direction.SOUTH]
        self.my_world.room_table[2, 1].directions = [Direction.NORTH]
        self.my_world.apply_way(way)
        self.assertEqual(self.my_world.room_table[0, 0].directions, [Direction.SOUTH, Direction.NORTH])
        self.assertEqual(self.my_world.room_table[1, 0].directions, [Direction.WEST, Direction.NORTH, Direction.SOUTH])
        self.assertEqual(self.my_world.room_table[2, 0].directions, [Direction.SOUTH, Direction.WEST, Direction.EAST])
        self.assertEqual(self.my_world.room_table[2, 1].directions, [Direction.NORTH, Direction.SOUTH])

    def test_add_secondary_ways(self):
        random.seed(1)
        init_way = [[0, 0], [1, 0], [2, 0]]
        end_way = self.my_world.add_secondary_ways(init_way, 2)
        self.assertEqual(len(end_way) - 2, len(init_way))
        self.assertTrue(Direction.WEST in self.my_world.room_table[0, 1].directions)
        self.assertTrue(Direction.EAST in self.my_world.room_table[0, 0].directions)
        self.assertTrue(Direction.WEST in self.my_world.room_table[1, 1].directions)
        self.assertTrue(Direction.EAST in self.my_world.room_table[1, 0].directions)
        self.assertEqual(end_way, [[0, 0], [0, 1], [1, 0], [1, 1], [2, 0]])

    def test_sort_room_direction(self):
        self.my_world.room_table[0, 0].directions = [Direction.EAST, Direction.NORTH]
        self.my_world.room_table[3, 3].directions = [Direction.WEST, Direction.SOUTH, Direction.NORTH]
        self.my_world.sort_room_direction()
        self.assertTrue(self.my_world.room_table[0, 0].directions, sorted(self.my_world.room_table[0, 0].directions))
        self.assertTrue(self.my_world.room_table[3, 3].directions, sorted(self.my_world.room_table[3, 3].directions))


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


class TestFindDirection(TestCase):
    def test_find_direction_N(self):
        self.assertEqual(find_direction([1, 0], [2, 0]), Direction.NORTH)

    def test_find_direction_S(self):
        self.assertEqual(find_direction([1, 0], [0, 0]), Direction.SOUTH)

    def test_find_direction_E(self):
        self.assertEqual(find_direction([1, 1], [1, 2]), Direction.EAST)

    def test_find_direction_W(self):
        self.assertEqual(find_direction([1, 1], [1, 0]), Direction.WEST)

    def test_find_direction_error(self):
        self.assertRaises(ValueError)
