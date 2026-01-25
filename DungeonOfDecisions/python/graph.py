class Room:
    def __init__(self, id_room, room_type):
        self.id = id_room
        self.type = room_type
        self.connections = []

    def connect(self, other_room):
        self.connections.append(other_room)


class DungeonGraph:
    def __init__(self):
        self.rooms = {}
        self.create_map()

    def create_room(self, id_room, room_type):
        self.rooms[id_room] = Room(id_room, room_type)

    def connect_rooms(self, from_id, to_id):
        self.rooms[from_id].connect(self.rooms[to_id])

    def create_map(self):
        self.create_room("START", "start")
        self.create_room("A", "combat")
        self.create_room("B", "safe")
        self.create_room("C", "treasure")
        self.create_room("D", "trap")
        self.create_room("E", "puzzle")
        self.create_room("F", "combat")
        self.create_room("G", "mistery")
        self.create_room("BOSS", "boss")

        self.connect_rooms("START", "A")
        self.connect_rooms("START", "B")
        self.connect_rooms("A", "C")
        self.connect_rooms("A", "D")
        self.connect_rooms("B", "E")
        self.connect_rooms("C", "F")
        self.connect_rooms("D", "F")
        self.connect_rooms("F", "G")
        self.connect_rooms("G", "BOSS")

    def get_next_rooms(self, id_room):
        return self.rooms[id_room].connections
