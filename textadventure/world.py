import numpy
import random
import math

from .directions import Direction
from .hero import Hero
from .obj import Obj
from .room import Room
from .enemy import Enemy


class World:
    ALL_MOD = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    def __init__(self, name: str=None, init_x_pos: int=0, init_y_pos: int=2, world_lvl: int=None):
        if world_lvl is None:
            room3 = Room('Start', 'You just enter into a manor! You are in a big room with a nice carpet. The door '
                                  'behind you close itself. You now have to choose in three direction.',
                         [Direction.WEST, Direction.NORTH, Direction.EAST])
            room2 = Room('Kitchen',
                         'You enter into a kitchen. Some meal are under preparation but no one is here. You see '
                         'a door in front of you or you can just go back.',
                         [Direction.WEST, Direction.EAST])
            room1 = Room('Closet', 'You found a closet with a lot of cooking stuff. You have to go back',
                         [Direction.EAST], obj_in_room=Obj('Domestic Room\'s Key'))
            room4 = Room('Domestic Chamber',
                         'You enter into a small chamber with a simple bed and a piece of furniture and'
                         ' a small window. There is a book on a chair close to the bed.',
                         [Direction.WEST], obj_in_room=Obj('Gun'), condition_to_enter=Obj('Domestic Room\'s Key'))
            room7 = Room('Living room',
                         'This is the first part of the living room. There is shelf on the wall  with a lot '
                         'of books. You can explore the living room in two directions',
                         [Direction.NORTH, Direction.EAST, Direction.SOUTH])
            room8 = Room('Living room',
                         'This is another part of the living room. There is a big table with some plates and'
                         ' cutlery ready for eating.',
                         [Direction.WEST, Direction.NORTH])
            room12 = Room('Living room',
                          'This is another part of the living room. There is a sofa and a coffee table. You '
                          'can see three half empty glasses. You see a close chest under the windows.',
                          [Direction.WEST, Direction.NORTH, Direction.SOUTH])
            room16 = Room('Chest', 'You open the chest and found bottles of alcohol.',
                          [Direction.SOUTH], obj_in_room=Obj('Bathroom\'s Key'))
            room11 = Room('Living room',
                          'This is another part of the living room. You can see a stair going down in North '
                          'and a long hallway in the West.',
                          [Direction.WEST, Direction.NORTH, Direction.EAST, Direction.SOUTH])
            room15 = Room('Stairs', 'Some dark stairs are going down to a toilet.',
                          [Direction.SOUTH])
            room10 = Room('Hallway', 'A simple hallway with chandelier give access to two rooms.',
                          [Direction.WEST, Direction.NORTH, Direction.EAST],
                          enemy=Enemy('Zombie', Obj('Gun'), 'A Zombie come from the North and jump on you!'))
            room14 = Room('Children Chamber', 'An empty children chamber with a lot of toys on the floor.',
                          [Direction.SOUTH])
            room9 = Room('Adults Chamber', 'A big room with a double bed. You can see a light passing though a door in '
                                           'the south.',
                         [Direction.EAST, Direction.SOUTH])
            room5 = Room('Bathroom',
                         'You open the door and find a bathroom. You discover the girl afraid and crying! You '
                         'saved her!',
                         [Direction.EAST, Direction.SOUTH], condition_to_enter=Obj('Bathroom\'s Key'), is_win=True)
            self.__room_table = None
            self.room_table = numpy.matrix([[room1, room2, room3, room4], [room5, Room(), room7, room8],
                                            [room9, room10, room11, room12], [Room(), room14, room15, room16]],
                                           dtype=Room)
            self.hero = Hero(name, self.room_table[init_x_pos, init_y_pos])
            self.world_size = [4, 4]
        else:
            self.hero = Hero(name)
            self.generate_world(world_lvl)

    @property
    def room_table(self):
        return self.__room_table

    @room_table.setter
    def room_table(self, room_table: numpy.matrix):
        for (x, y), value in numpy.ndenumerate(room_table):
            room_table[x, y].x_pos = x
            room_table[x, y].y_pos = y
        self.__room_table = room_table

    def run_game(self):
        while not self.hero.current_room.is_win:
            direction = self.hero.action()
            if direction is None:
                break
            new_room = self.get_room_after_move(direction)
            self.hero.entry(new_room)
        if self.hero.is_alive:
            self.hero.current_room.display()
            print('You Win!')
        else:
            print('You Loose!')

    def get_room_after_move(self, direction: Direction):
        old_x_pos = self.hero.current_room.x_pos
        old_y_pos = self.hero.current_room.y_pos
        new_room = None
        if direction == Direction.NORTH:
            new_room = self.room_table[old_x_pos+1, old_y_pos]
        elif direction == Direction.EAST:
            new_room = self.room_table[old_x_pos, old_y_pos+1]
        elif direction == Direction.SOUTH:
            new_room = self.room_table[old_x_pos-1, old_y_pos]
        elif direction == Direction.WEST:
            new_room = self.room_table[old_x_pos, old_y_pos-1]
        return new_room

    def generate_world(self, lvl: int):
        self.world_size = self.init_default_word(lvl)
        hero_init_pos = self.init_hero_pos(self.world_size[1])
        win_pos = self.init_win_pos(self.world_size)
        way = self.build_main_way()
        self.apply_way(way)
        all_way = self.add_secondary_ways(way, lvl * 20)
        self.sort_room_direction()
        self.add_lock_door(all_way, lvl)

    def init_default_word(self, lvl: int):
        nb_row = lvl * 4
        nb_column = lvl * 4
        self.room_table = numpy.matrix([[Room(directions=[]) for _ in range(nb_row)] for _ in range(nb_column)])
        return [nb_row, nb_column]

    def init_hero_pos(self, nb_col: int):
        init_y_pos = random.randint(0, nb_col - 1)
        init_x_pos = 0
        self.hero.current_room = self.room_table[init_x_pos, init_y_pos]
        return [init_x_pos, init_y_pos]

    def init_win_pos(self, world_size: [int]):
        win_y = random.randint(0, world_size[1] - 1)
        win_x = random.randint(math.ceil(world_size[0]*0.66), world_size[0]-1)
        self.room_table[win_x, win_y].is_win = True
        return [win_x, win_y]

    def build_main_way(self):
        hero_init_pos = [self.hero.current_room.x_pos, self.hero.current_room.y_pos]
        list_all_tested_room = [hero_init_pos]
        final_way = [hero_init_pos]
        current_room = self.room_table[hero_init_pos[0], hero_init_pos[1]]
        current_pos = hero_init_pos.copy()
        while not current_room.is_win:
            mod_available = self.find_available_mod(current_pos, list_all_tested_room)
            if len(mod_available) == 0:
                final_way.remove(current_pos)
                current_pos = final_way[-1]
            else:
                current_pos = [x + y for x, y in zip(current_pos, random.choice(mod_available))]
                list_all_tested_room.append(current_pos)
                final_way.append(current_pos)
            current_room = self.room_table[current_pos[0], current_pos[1]]
        return final_way

    def find_available_mod(self, current_pos: [int], list_room_not_available: [[int]]):
        mod_available = []
        for mod in World.ALL_MOD:
            new_pos = [x + y for x, y in zip(current_pos, mod)]
            if new_pos not in list_room_not_available and self.is_inside_world(new_pos):
                mod_available.append(mod)
        return mod_available

    def is_inside_world(self, pos: [int]):
        if pos[0] < 0 or pos[0] >= self.world_size[0] or pos[1] < 0 or pos[1] >= self.world_size[1]:
            return False
        return True

    def apply_way(self, way: [[int]]):
        for i in range(1, len(way) - 1):
            self.room_table[way[i][0], way[i][1]].directions.append(find_direction(way[i], way[i-1]))
            self.room_table[way[i][0], way[i][1]].directions.append(find_direction(way[i], way[i+1]))
        self.room_table[way[0][0], way[0][1]].directions.append(find_direction(way[0], way[1]))
        self.room_table[way[-1][0], way[-1][1]].directions.append(find_direction(way[-1], way[-2]))

    def add_secondary_ways(self, way: [[int]], nd_secondary: int):
        way_out = way.copy()
        for _ in range(nd_secondary):
            loc_start_second_way = random.choice(way_out)
            mod_available = self.find_available_mod(loc_start_second_way, way_out)
            if len(mod_available) == 0:
                continue
            loc_end_second_way = [x + y for x, y in zip(loc_start_second_way, random.choice(mod_available))]
            self.apply_way([loc_start_second_way, loc_end_second_way])
            way_out.insert(way_out.index(loc_start_second_way)+1, loc_end_second_way)
        return way_out

    def sort_room_direction(self):
        for (x, y), value in numpy.ndenumerate(self.room_table):
            self.room_table[x, y].sort_direction()

    def add_lock_door(self, all_way: [[int]], nb_lock: int):
        diff_loc = []
        for i in range(len(all_way) - 1):
            diff_loc.append(sum([abs(x - y) for x, y in zip(all_way[i], all_way[i + 1])]))
        for i in range(nb_lock):
            loc_add_lock = random.choice(all_way[1:])
            key = Obj('Key %d' % i)
            index_loc_max_to_add_key = all_way.index(loc_add_lock)-1
            dead_end_available = [x for x in diff_loc[:index_loc_max_to_add_key] if x != 1]
            if dead_end_available:
                index_add_key = random.choice(dead_end_available)
                loc_add_key = all_way[index_add_key]
            else:
                loc_add_key = random.choice(all_way[:index_loc_max_to_add_key])
            self.room_table[loc_add_lock[0], loc_add_lock[1]].condition_to_enter = key
            self.room_table[loc_add_key[0], loc_add_key[1]].obj_in_room = key


def find_direction(loc1: [int], loc2: [int]):
    diff = [y - x for x, y in zip(loc1, loc2)]
    if diff[0] == 1 and diff[1] == 0:
        return Direction.NORTH
    elif diff[0] == -1 and diff[1] == 0:
        return Direction.SOUTH
    elif diff[0] == 0 and diff[1] == 1:
        return Direction.EAST
    elif diff[0] == 0 and diff[1] == -1:
        return Direction.WEST
    else:
        raise ValueError("Location not join")
