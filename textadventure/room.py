from .directions import Direction
from .obj import Obj
from .enemy import Enemy


class Room:
    def __init__(self, name: str='Default Room', description: str='Default Description',
                 directions: [Direction]=None, obj_in_room: Obj=None, condition_to_enter: Obj=None,
                 is_win: bool=False, enemy: Enemy=None):
        if directions is None:
            directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        self.name = name
        self.description = description
        self.directions = directions
        self.obj_in_room = obj_in_room
        self.condition_to_enter = condition_to_enter
        self.enemy = enemy
        self.is_win = is_win
        self.x_pos = None
        self.y_pos = None

    def display(self):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(self.name)
        print('Description:')
        print(self.description)

    def action_room(self):
        print('Where do you want to go ?')
        print('\n'.join(self.directions))
        valid_input = False
        direction_choose = None
        while not valid_input:
            user_choice = input()
            if user_choice in ['N', 'North']:
                direction_choose = Direction.NORTH
            elif user_choice in ['E', 'East']:
                direction_choose = Direction.EAST
            elif user_choice in ['S', 'South']:
                direction_choose = Direction.SOUTH
            elif user_choice in ['W', 'West']:
                direction_choose = Direction.WEST
            else:
                valid_input = False
                print('Unknown direction input. Please, try again!')
                continue
            if direction_choose not in self.directions:
                valid_input = False
                print('You cannot go in this direction. Please, choose another direction!')
            else:
                valid_input = True
        return direction_choose

    def delete_obj(self):
        self.obj_in_room = None

    def delete_enemy(self):
        self.enemy = None

    def delete_condition_to_enter(self):
        self.condition_to_enter = None
