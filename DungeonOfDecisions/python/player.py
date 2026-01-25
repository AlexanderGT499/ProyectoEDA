class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.max_life = 100
        self.life = 100
        self.score = 0
        self.current_node = None
        self.potions = 2
        self.floor = 1
 
    def take_damage(self, amount):
        self.life -= amount
        if self.life < 0:
            self.life = 0
 
    def healt(self, amount):
        self.life += amount
        if self.life > self.max_life:
            self.life = self.max_life
 
    def add_score(self, points):
        self.score += points
 
    def set_position(self, node):
        self.current_node = node
 
    def get_status(self):
        return {
            "id": self.id,
            "life": self.life,
            "score": self.score,
            "current_node": self.current_node
        }
 
    def use_potion(self):
        if self.potions > 0 and self.life < self.max_life:
            heal_amount = 20 if self.life <= 80 else 10
            self.healt(heal_amount)
            self.potions -= 1
            self.score -= 2
        else:
            pass
 
    def advance_floor(self):
        self.floor += 1
        self.add_score(5)
 
    def is_alive(self):
        return self.life > 0


        
