import pygame

def CreateBoard():
    board = []
    for i in range(10):
        row = []
        for e in range(10):
            row.append(-1)
        board.append(row)
    return board


def PlaceShips(board, ships):
    ships = []


def ComputerPlaceShips(board, ships):
    ships = []


def StartGame():

    #[userboard, enemy board, ship placements]
    user = [CreateBoard(), CreateBoard(), []]
    computer = [CreateBoard(), CreateBoard(), []]
    PlaceShips(user[0], user[2])
    ComputerPlaceShips(computer[0], computer[2])

    return True

def main():

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    background = pygame.Surface(screen.get_size())
    background.fill((50,50,255))
    background = background.convert()
    screen.blit(background, (0, 0))
    gameloop = True

    text = "NeoBattleship"
    pygame.display.set_caption(text)
    pygame.display.flip()

    while gameloop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameloop = False

    pygame.quit()


if __name__ == '__main__':
    main()
