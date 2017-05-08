from unittest import TestCase
from unittest.mock import patch

from textadventure.directions import Direction
from textadventure.hero import Hero
from textadventure.obj import Obj
from textadventure.room import Room
from textadventure.enemy import Enemy


class TestHero(TestCase):

    @patch.object(Hero, "verify_entry")
    def test_entry_allowed(self, mock_verify_entry):
        mock_verify_entry.return_value = True
        my_hero = Hero(room=Room('Init Room'))
        move_room = Room('Move room', condition_to_enter=Obj.RANDOM_KEY)
        my_hero.entry(move_room)
        self.assertEqual(my_hero.current_room, move_room)
        self.assertIsNone(move_room.condition_to_enter)

    @patch.object(Hero, "verify_entry")
    @patch('builtins.input')
    def test_entry_not_allowed(self, mock_verify_entry, mock_input):
        mock_verify_entry.return_value = False
        mock_input.return_value = None
        init_room = Room('Init Room')
        my_hero = Hero(room=init_room)
        move_room = Room(name='Move room', condition_to_enter=Obj.RANDOM_KEY)
        my_hero.entry(move_room)
        self.assertEqual(my_hero.current_room, init_room)
        self.assertIsNotNone(move_room.condition_to_enter)

    def test_verify_entry_no_key_needed(self):
        my_hero = Hero(inventory=[])
        my_room = Room(obj_in_room=None)
        self.assertTrue(my_hero.verify_entry(my_room))

    def test_verify_entry_key_needed_no_inventory(self):
        my_hero = Hero(inventory=[])
        my_room = Room(condition_to_enter=Obj())
        self.assertFalse(my_hero.verify_entry(my_room))

    @patch.object(Hero, "use_obj_inv")
    def test_verify_entry_key_needed_good_key_selected(self, mock_use_obj_inv):
        mock_use_obj_inv.return_value = Obj()
        my_hero = Hero(inventory=[Obj()])
        my_room = Room(condition_to_enter=Obj())
        self.assertTrue(my_hero.verify_entry(my_room))

    @patch.object(Hero, "use_obj_inv")
    def test_verify_entry_key_needed_bad_key_selected(self, mock_use_obj_inv):
        mock_use_obj_inv.return_value = Obj(name='Obj1')
        my_hero = Hero(inventory=[Obj(name='Obj1')])
        my_room = Room(condition_to_enter=Obj(name='Obj2'))
        self.assertFalse(my_hero.verify_entry(my_room))

    @patch('builtins.input')
    def test_action_not_dead(self, mock_input):
        mock_input.return_value = 'N'
        my_hero = Hero(room=Room(obj_in_room=Obj()))
        self.assertEqual(Direction.NORTH, my_hero.action())
        self.assertIn(Obj(), my_hero.inventory)

    def test_action_dead(self):
        my_hero = Hero()
        my_hero.is_alive = False
        self.assertIsNone(my_hero.action())

    def test_pick_key_with_key(self):
        my_hero = Hero(room=Room(obj_in_room=Obj()))
        self.assertNotIn(Obj(), my_hero.inventory)
        my_hero.pick_obj()
        self.assertIn(Obj(), my_hero.inventory)
        self.assertIsNone(my_hero.current_room.obj_in_room)

    def test_pick_key_without_key(self):
        my_hero = Hero(room=Room(obj_in_room=None))
        self.assertNotIn(Obj(), my_hero.inventory)
        my_hero.pick_obj()
        self.assertNotIn(Obj(), my_hero.inventory)

    @patch.object(Hero, 'use_obj_inv')
    def test_defeat_enemy(self, mock_use_obj_inv):
        mock_use_obj_inv.return_value = Obj()
        my_hero = Hero(room=Room(enemy=Enemy(kill_by=Obj())), inventory=[Obj()])
        self.assertTrue(my_hero.defeat_enemy())

    @patch('builtins.input')
    def test_use_obj_inv_no_punch(self, mock_input):
        mock_input.side_effect = [2, 1]
        my_hero = Hero(room=Room(), inventory=[Obj()])
        self.assertEqual(my_hero.use_obj_inv(is_punch=False), Obj())

    @patch('builtins.input')
    def test_use_obj_inv_punch(self, mock_input):
        mock_input.return_value = 1
        my_hero = Hero(room=Room(), inventory=[])
        self.assertEqual(my_hero.use_obj_inv(is_punch=True), Obj(name='Punch'))

    def test_meet_enemy_when_no_enemy(self):
        my_hero = Hero(room=Room(enemy=None))
        self.assertIsNone(my_hero.meet_enemy())

    @patch.object(Hero, "defeat_enemy")
    def test_meet_enemy_when_win_fight(self, mock_defeat_enemy):
        mock_defeat_enemy.return_value = True
        my_hero = Hero(room=Room(enemy=Enemy(kill_by=Obj())))
        my_hero.meet_enemy()
        self.assertTrue(my_hero.is_alive)
        self.assertIsNone(my_hero.current_room.enemy)

    @patch.object(Hero, "defeat_enemy")
    def test_meet_enemy_when_loose_fight(self, mock_defeat_enemy):
        mock_defeat_enemy.return_value = False
        my_hero = Hero(room=Room(enemy=Enemy(kill_by=Obj())))
        my_hero.meet_enemy()
        self.assertFalse(my_hero.is_alive)
        self.assertIsNotNone(my_hero.current_room.enemy)
