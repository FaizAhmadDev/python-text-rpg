class Enemy:
    def __init__(self, name, hp, atk, defense, etype):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.type = etype
        self._aggro = False

    def attack_player(self, player):
        damage = max(0, self.atk - player.defense)
        player.hp -= damage
        print(f"{self.name} hits {player.name} for {damage}. Player HP is now {player.hp}")
        if player.hp <= 0:
            print("Player has fallen.")
