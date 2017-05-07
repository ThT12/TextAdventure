import numpy
import random

from .directions import Direction
from .hero import Hero
from .obj import Obj
from .room import Room
from .enemy import Enemy


class World:
    def __init__(self, name: str=None, init_x_pos: int=0, init_y_pos: int=2, world_lvl: int=None):
        if world_lvl is None:
            room3 = Room('Start', 'You just enter into a manor! You are in a big room with a nice carpet. The door '
                                  'behind you close itself. You now have to choose in three direction.',
                         [Direction.WEST, Direction.NORTH, Direction.EAST])
            room2 = Room('Kitchen', 'You enter into a kitchen. Some meal are under preparation but no one is here. You see '
                                    'a door in front of you or you can just go back.',
                         [Direction.WEST, Direction.EAST])
            room1 = Room('Closet', 'You found a closet with a lot of cooking stuff. You have to go back',
                         [Direction.EAST], obj_in_room=Obj.DOM_ROOM_KEY)
            room4 = Room('Domestic Chamber', 'You enter into a small chamber with a simple bed and a piece of furniture and'
                                             ' a small window. There is a book on a chair close to the bed.',
                         [Direction.WEST], obj_in_room=Obj.GUN, condition_to_enter=Obj.DOM_ROOM_KEY)
            room7 = Room('Living room', 'This is the first part of the living room. There is shelf on the wall  with a lot '
                                        'of books. You can explore the living room in two directions',
                         [Direction.NORTH, Direction.EAST, Direction.SOUTH])
            room8 = Room('Living room', 'This is another part of the living room. There is a big table with some plates and'
                                        ' cutlery ready for eating.',
                         [Direction.WEST, Direction.NORTH])
            room12 = Room('Living room', 'This is another part of the living room. There is a sofa and a coffee table. You '
                                         'can see three half empty glasses. You see a close chest under the windows.',
                          [Direction.WEST, Direction.NORTH, Direction.SOUTH])
            room16 = Room('Chest', 'You open the chest and found bottles of alcohol.',
                          [Direction.SOUTH], obj_in_room=Obj.BATHROOM_KEY)
            room11 = Room('Living room', 'This is another part of the living room. You can see a stair going down in North '
                                         'and a long hallway in the West.',
                          [Direction.WEST, Direction.NORTH, Direction.EAST, Direction.SOUTH])
            room15 = Room('Stairs', 'Some dark stairs are going down to a toilet.',
                          [Direction.SOUTH])
            room10 = Room('Hallway', 'A simple hallway with chandelier give access to two rooms.',
                          [Direction.WEST, Direction.NORTH, Direction.EAST],
                          enemy=Enemy('Zombie', Obj.GUN, 'A Zombie come from the North and jump on you!'))
            room14 = Room('Children Chamber', 'An empty children chamber with a lot of toys on the floor.',
                          [Direction.SOUTH])
            room9 = Room('Adults Chamber', 'A big room with a double bed. You can see a light passing though a door in '
                                           'the south.',
                         [Direction.EAST, Direction.SOUTH])
            room5 = Room('Bathroom', 'You open the door and find a bathroom. You discover the girl afraid and crying! You '
                                     'saved her!',
                         [Direction.EAST, Direction.SOUTH], condition_to_enter=Obj.BATHROOM_KEY, is_win=True)
            self.__room_table = None
            self.room_table = numpy.matrix([[room1, room2, room3, room4], [room5, Room(), room7, room8],
                                            [room9, room10, room11, room12], [Room(), room14, room15, room16]], dtype=Room)
            self.hero = Hero(name, self.room_table[init_x_pos, init_y_pos])
        else:
            self.generate_world(world_lvl)
            self.hero = Hero(name)

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
        world_size = self.init_default_word(lvl)
        hero_init_pos = self.init_hero_pos(world_size[1])

    def init_default_word(self, lvl: int):
        nb_row = lvl * 4
        nb_column = lvl * 4
        self.room_table = numpy.matrix([[Room() for _ in range(nb_row)] for _ in range(nb_column)])
        return [nb_row, nb_column]

    def init_hero_pos(self, nb_col: int):
        init_y_pos = random.randint(0, nb_col - 1)
        init_x_pos = 0
        self.hero.current_room = self.room_table[init_x_pos, init_y_pos]
        return  [init_x_pos, init_y_pos]