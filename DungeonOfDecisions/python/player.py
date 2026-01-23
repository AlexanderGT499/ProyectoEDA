class Player:
    
    def __init__(self, player_id):
        self.id = player_id
        self.life=100
        self.score =0
        self.current_node=None
    
    def take_damage(self, amount):
        self.life-=amount
        if self.life<0:
            self.life=0

    def healt(self, amount):
        self.life+=amount
        if self.life>100:
            self.life=100
    
    def add_score(self,point):
        self.score+=point

    def set_position(self,node):
        self.current_node=node
    
    def get_status(self):
        return{
            "id":self.id,
            "life":self.life,
            "score":self.score,
            "current_node": self.current_node
        }



    
    
        





        
