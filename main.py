import game as game_mod


def main():
    game = game_mod.Game()
    while True:
        game.update()
        game.show()


main()
