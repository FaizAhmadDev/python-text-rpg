class Player:
    def __init__(self, name, hp, atk, defense, coins):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defense = defense
        self.coins = coins
        self.level = 1
        self.exp = 0
        self._temp_last_action = None

    def attack_enemy(self, enemy):
        damage = max(0, self.atk - enemy.defense)
        enemy.hp -= damage
        self._temp_last_action = ("attack", damage)
        print(f"{self.name} hits {enemy.name} for {damage}. Enemy HP is now {enemy.hp}")
        if enemy.hp <= 0:
            self.gain_exp(10)
            print(f"{enemy.name} defeated!")

    def gain_exp(self, amount):
        self.exp += amount
        print(f"Gained {amount} EXP.")  
        if self.exp >= 20:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.atk += 2
        self.defense += 1
        self.exp = 0
        print("Leveled up! Now level", self.level)

    def use_item(self, item):
        # interacts with item's internals 
        if 'heal' in item.props:
            heal = item.props['heal']
            self.hp = min(self.max_hp, self.hp + heal)
            print(f"{self.name} healed for {heal}. HP: {self.hp}/{self.max_hp}")
        if 'atk' in item.props:
            self.atk += item.props['atk']
            print(f"{self.name} attack increased by {item.props['atk']}")
        if 'def' in item.props:
            self.defense += item.props['def']
            print(f"{self.name} defense increased by {item.props['def']}")

    def print_status(self):
        print(f"{self.name} - HP: {self.hp}/{self.max_hp} Atk: {self.atk} Def: {self.defense} Coins: {self.coins} Lvl: {self.level}")
