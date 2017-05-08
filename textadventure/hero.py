from .room import Room
from .obj import Obj


class Hero:
    def __init__(self, name: str='DefaultHero', room: Room=Room(), inventory=None):
        if inventory is None:
            inventory = []
        self.name = name
        self.current_room = room
        self.inventory = inventory
        self.is_alive = True

    def entry(self, room: Room):
        if self.verify_entry(room):
            self.current_room = room
            self.current_room.delete_condition_to_enter()
        else:
            input('Press enter to continue...')

    def verify_entry(self, room: Room):
        if room.condition_to_enter is None:
            return True
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('The door is closed.')
        if not self.inventory:
            print('You have nothing on you to open the door.')
            return False
        print('What do you want to use?')
        obj_used = self.use_obj_inv(is_punch=False)
        if room.condition_to_enter == obj_used:
            print(''.join(['You open the door with the ', obj_used.name, '!']))
            return True
        else:
            print('Nothing happen!')
            return False

    def action(self):
        self.meet_enemy()
        if not self.is_alive:
            return None
        self.current_room.display()
        self.pick_obj()
        return self.current_room.action_room()

    def pick_obj(self):
        if self.current_room.obj_in_room is not None:
            print('Object found:')
            print(''.join(['You found the ', self.current_room.obj_in_room.name, '!']))
            self.inventory.append(self.current_room.obj_in_room)
            self.current_room.delete_obj()

    def meet_enemy(self):
        if self.current_room.enemy is None:
            return
        self.current_room.enemy.display()
        if self.defeat_enemy():
            print(''.join(['You defeat the ', self.current_room.enemy.name, '!']))
            self.current_room.delete_enemy()
        else:
            print(''.join(['You have been defeated by the ', self.current_room.enemy.name, '!']))
            print('You are dead!')
            self.is_alive = False

    def defeat_enemy(self):
        print('What do you want to use to fight him?')
        obj_used = self.use_obj_inv(is_punch=True)
        return self.current_room.enemy.is_win_fight(obj_used)

    def use_obj_inv(self, is_punch: bool = False):
        template_display = '%-2i - %s'
        list_inv = [template_display % (iInv+1, self.inventory[iInv].name) for iInv in range(len(self.inventory))]
        if is_punch:
            list_inv.append(template_display % (len(self.inventory) + 1, 'Punch'))
        print('\n'.join(list_inv))
        while True:
            try:
                choice = int(input()) - 1
                if is_punch and choice == len(self.inventory):
                    choice = Obj(name='Punch')
                else:
                    choice = self.inventory[choice]
                break
            except (ValueError, IndexError):
                print('Invalid object')
        return choice
