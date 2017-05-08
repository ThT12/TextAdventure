class Obj:
    def __init__(self, name: str='Name'):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    # BATHROOM_KEY = 'Bathroom\'s Key'
    # DOM_ROOM_KEY = 'Domestic Room\'s Key'
    # GUN = 'Gun'
    # PUNCH = 'Punch'
    # RANDOM_KEY = 'Random Key'
