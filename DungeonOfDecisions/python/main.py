from player import Player
from graph import DungeonGraph
from combat import fight
import random



def play_game(player):
    dungeon = DungeonGraph()
    current_room = dungeon.rooms["START"]
    player.current_node = current_room.id  

    while player.is_alive():
        print(f"\n Sala: {current_room.id}({current_room.type})")
        print(f"\n Vida: {player.life}| Posiciones: {player.potions}| Puntaje: {player.score}")
        if current_room.type == "combat":
            enemy_type = random.choice(["Basic","Medium", "Strong"])
            if not fight(player, enemy_type):
                break
        elif current_room.type == "safe":
            player.healt(15)
            print("Has entrado a la sala segura(+15 de vida)")
        elif current_room.type == "treasure":
            event = random.randint(1, 100)
            if event <= 50:
                player.potions += 1
                print("Has encontrado una pocion")
            elif event <= 80:
                player.add_score(10)
                print("Has ganado puntos")
            else:
                player.take_damage(5)
                print("Has caido en una trampa leve")
        elif current_room.type =="trap":
            player.take_damage(10)
            print("Trampa activada")
        elif current_room.type == "puzzle":
            success_chance = max(40,80 - player.floor*10)
            if random.randint(1, 100) <= success_chance:
                player.add_score(10)
                print("Acertijo resuelto")
            else:
                player.take_damage(10)
                print("Fallaste el acertijo")
        elif current_room.type == "mistery":
            effect = random.choice(["blessing", "curse"])
            if effect == "blessing":
                player.add_score(10)
                print("Has sido bendecido")
            else:
                player.take_damage(5)
                print("Has sido maldecido") 
        elif current_room.type == "boss":
            if fight(player, "boss"):
                print("Jefe derrotado")
            break
        next_rooms = dungeon.get_next_rooms(current_room.id)
        if not next_rooms:
            break
        current_room = random.choice(next_rooms)
    print(f"\n Puntaje final del jugador:  {player.id}:{player.score + player.life // 2}")            

if __name__ == "__main__":
    print("Dungeon of Decisions")
    print("Bienvenido al juego")
    p1 = Player(1)
    play_game(p1)
    p2 = Player(2)
    play_game(2)
    print("\n Gana el jugador con mas puntaje")