from player import Player

player1=Player(player_id=1)
player2= Player(player_id=2)
def start_game():
    print('Dungeon Of Decisions')
    print('Loading Game...\n')
    print('Estado inicial de los jugadores: ')
    print(f'jugador1: -> Vida:{player1.life},Puntaje:{player1.score}')
    print(f'jugador2: -> Vida:{player2.life},Puntaje:{player2.score}')

