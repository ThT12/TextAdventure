from .obj import Obj


class Enemy:
    def __init__(self, name: str='Enemy', kill_by: Obj=Obj(), context: str='I\'m the monster!'):
        self.name = name
        self.kill_by = kill_by
        self.context = context

    def is_win_fight(self, obj: Obj):
        return self.kill_by == obj

    def display(self):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(''.join(['You meet the ', self.name, '!']))
        print(self.context)
