from textadventure.world import World


def main():
    print('Welcome to Text Adventure Game - v1.0')
    name = input('What is your name?')
    print(''.join(['Hi ', name, '! A little girl have disappear! Can you find her in the manor?']))
    input('Press enter to start your quest!')
    my_world = World(name=name, world_lvl=1)
    my_world.run_game()


if __name__ == "__main__":
    main()
