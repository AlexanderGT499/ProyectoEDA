import json
import random
from player import Player
from graph import DungeonGraph
from combat import fight

GAME_STATE_PATH = "../data/game_state.json"
PLAYER_ACTION_PATH = "../data/player_action.json"

# Inicializamos el  juego
player = Player(1)
dungeon = DungeonGraph()
current_room = dungeon.rooms["START"]

def write_game_state(message="", enemy=None, game_over=False):
    next_rooms = dungeon.get_next_rooms(current_room.id)

    state = {
        "player": {
            "id": player.id,
            "life": player.life,
            "max_life": player.max_life,
            "score": player.score,
            "potions": player.potions,
            "floor": player.floor,
            "current_room": current_room.id
        },
        "room": {
            "id": current_room.id,
            "type": current_room.type
        },
        "next_rooms": [room.id for room in next_rooms],
        "enemy": enemy,
        "message": message,
        "game_over": game_over
    }

    with open(GAME_STATE_PATH, "w") as f:
        json.dump(state, f, indent=4)


def read_player_action():
    with open(PLAYER_ACTION_PATH, "r") as f:
        return json.load(f)


# Escribimos estado inicial
write_game_state("Bienvenido a Dungeon of Decisions")


while True:
    action_data = read_player_action()

    action = action_data["action"]

    if action == "none":
        continue

    # USAR POCIÓN
    if action == "use_potion":
        player.use_potion()
        write_game_state("Has usado una poción")

    # MOVERSE DE SALA
    elif action == "move":
        target = action_data["target_room"]
        current_room = dungeon.rooms[target]

        msg = f"Te moviste a la sala {current_room.id}"

        # Resolvemos evento según tipo de sala
        if current_room.type == "combat":
            enemy_type = random.choice(["weak", "medium", "strong"])
            result = fight(player, enemy_type)
            if not result:
                write_game_state("Has muerto", game_over=True)
                break
            msg = f"Combate ganado contra {enemy_type}"

        elif current_room.type == "safe":
            player.heal(15)
            msg = "Sala segura (+15 vida)"

        elif current_room.type == "treasure":
            event = random.randint(1, 100)
            if event <= 50:
                player.potions += 1
                msg = "Encontraste una poción"
            elif event <= 80:
                player.add_score(10)
                msg = "Encontraste puntos"
            else:
                player.take_damage(5)
                msg = "Trampa leve"

        elif current_room.type == "trap":
            player.take_damage(10)
            msg = "Trampa activada"

        elif current_room.type == "puzzle":
            chance = max(40, 80 - player.floor * 10)
            if random.randint(1, 100) <= chance:
                player.add_score(10)
                msg = "Acertijo resuelto"
            else:
                player.take_damage(10)
                msg = "Fallaste el acertijo"

        elif current_room.type == "mistery":
            effect = random.choice(["blessing", "curse"])
            if effect == "blessing":
                player.add_score(10)
                msg = "Bendición recibida"
            else:
                player.take_damage(5)
                msg = "Maldición recibida"

        elif current_room.type == "boss":
            result = fight(player, "boss")
            if result:
                write_game_state("Jefe derrotado", game_over=True)
                break
            else:
                write_game_state("Has muerto", game_over=True)
                break

        write_game_state(msg)

    # Aqui osea le reseteamos el archivo  del player action cada que el jugador hace algo nuevo
    with open(PLAYER_ACTION_PATH, "w") as f:
        json.dump({
            "action": "none",
            "target_room": None,
            "combat_action": None,
            "use_potion": False
        }, f, indent=4)
