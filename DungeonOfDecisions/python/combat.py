import random

ENEMIES = {
    "Weak" : {"Life" : 20, "Damage" : 10, "Score" : 10},
    "Medium" : {"Life": 35, "Damage" : 15, "Score" : 20},
    "Strong" : {"Life": 50, "Damage" : 20, "Score" : 30},
    "Boss" : {"Life": 100, "Damage" : 25, "Score" : 50},
}

def fight(player, enemy_type):
    enemy = ENEMIES[enemy_type].copy()
    floor_modifier = 1 + (player.floor * 0.15)
    enemy["Life"] = int(enemy["Life"] * floor_modifier)
    enemy["Damage"] = int(enemy["Damage"] * floor_modifier)
    print(f"Combate contra {enemy_type.upper()}")
    defend_next = False
    while enemy["Life"] > 0 and player.is_alive():
        action = input("Atacar(A) / Defender(D): ").lower()
        if action == "a":
            enemy["life"] -= 20
            print("Has atacado al enemigo") 
        elif action == "d":
            defend_next = True
            player.add_score(2)
            print("Has bloqueado el ataque")
        if enemy["Life"] > 0:
            damage = enemy["Damage"]
            if defend_next:
                damage //= 2
                defend_next = False
            player.take_damage(damage)
            print(f"Recibes {damage} de daño")
        if player.is_alive():
            player.add_score(enemy["Score"])
            player.advance_floor()
            print("Enemigo derrotado")
            return True 
        else:
            print("Has muerto")
            return False
