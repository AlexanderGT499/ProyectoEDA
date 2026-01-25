import random
import json

ENEMIES = {
    "weak": {"Life": 20, "Damage": 10, "Score": 10},
    "medium": {"Life": 35, "Damage": 15, "Score": 20},
    "strong": {"Life": 50, "Damage": 20, "Score": 30},
    "boss": {"Life": 100, "Damage": 25, "Score": 50},
}

PLAYER_ACTION_PATH = "../data/player_action.json"

def read_combat_action():
    with open(PLAYER_ACTION_PATH, "r") as f:
        data = json.load(f)
        return data["combat_action"]

def fight(player, enemy_type):
    enemy = ENEMIES[enemy_type].copy()

    floor_modifier = 1 + (player.floor * 0.15)
    enemy["Life"] = int(enemy["Life"] * floor_modifier)
    enemy["Damage"] = int(enemy["Damage"] * floor_modifier)

    defend_next = False

    while enemy["Life"] > 0 and player.is_alive():
        action = read_combat_action()

        if action is None:
            continue

        # ATAQUE
        if action == "attack":
            enemy["Life"] -= 20

        # DEFENSA
        elif action == "defend":
            defend_next = True
            player.add_score(2)

        # RESET acción de combate
        with open(PLAYER_ACTION_PATH, "w") as f:
            json.dump({
                "action": "none",
                "target_room": None,
                "combat_action": None,
                "use_potion": False
            }, f, indent=4)

        # TURNO DEL ENEMIGO
        if enemy["Life"] > 0:
            damage = enemy["Damage"]
            if defend_next:
                damage //= 2
                defend_next = False

            player.take_damage(damage)

    if player.is_alive():
        player.add_score(enemy["Score"])
        player.advance_floor()
        return True
    else:
        return False
