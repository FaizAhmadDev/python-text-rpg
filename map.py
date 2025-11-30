class WorldMap:
    def __init__(self):
        self.rooms = [
            {"name": "Forest Edge", "type": "forest", "desc": "Trees and rustling sounds."},
            {"name": "Cave Entrance", "type": "cave", "desc": "Darkness lies within."},
            {"name": "Bandit Camp", "type": "camp", "desc": "You see tents and guards."}
        ]
        self.start_room = self.rooms[0]
