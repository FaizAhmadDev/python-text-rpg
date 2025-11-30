import random
from player import Player
from enemy import Enemy
from inventory import Inventory, Item
from map import WorldMap
from combat import Combat

class Game:
    def __init__(self):
        self.player = Player("Hero", 100, 10, 5, 20)
        self.inventory = Inventory()
        self.world = WorldMap()
        self.combat = Combat()
        self.current_room = self.world.start_room
        self.running = True
        self._temp_last_loot = None

    def welcome(self):
        print("Welcome to the Mini Adventure RPG!")
        print("Explore rooms, fight monsters, buy items, and level up.")
        print("Commands: explore, status, inventory, shop, quit")

    def game_loop(self):
        # Big loop with a lot of branching
        while self.running and self.player.hp > 0:
            print(f"\nYou are in: {self.current_room['name']}")
            print(self.current_room['desc'])
            cmd = input(">>> ").strip().lower()
            if cmd == "quit":
                self.running = False
            elif cmd == "explore":
                self.explore()
            elif cmd == "status":
                self.player.print_status()
            elif cmd == "inventory":
                self.inventory.show()
            elif cmd == "shop":
                self.shop()
            elif cmd == "move":
                self.move()
            else:
                print("Unknown command. Try: explore, status, inventory, shop, move, quit")

    def explore(self):
        # method with multiple responsibilities: encounter + loot + random event
        room = self.current_room
        print("You look around...")
        # Random encounter chance
        if random.random() < 0.7:
            e = self._random_enemy_for_room(room['type'])
            print(f"A {e.name} appears!")
            # Feature-envy-ish: combat uses player and enemy internals
            result = self.combat.fight(self.player, e, self.inventory)
            if result == "won":
                loot = self._generate_loot(e)
                self._temp_last_loot = loot
                print(f"You found: {', '.join([i.name for i in loot])}")
                for it in loot:
                    self.inventory.add(it)
            elif result == "ran":
                print("You escaped but dropped some coins.")
                self.player.coins = max(0, self.player.coins - 2)
            else:
                print("You died in battle...")
                self.running = False
        else:
            print("No enemies here. You found some coins.")
            self.player.coins += 5
            # duplicate-like logic: item chance
            if random.random() < 0.3:
                potion = Item("small_potion", "Restores a small amount of HP", {"heal":20})
                self.inventory.add(potion)
                print("You picked up a small potion.")

    def _generate_loot(self, enemy):
        # loot logic 
        items = []
        if enemy.type == "goblin":
            items.append(Item("coin", "A shiny coin", {"value": 5}))
            if random.random() < 0.3:
                items.append(Item("rusty_sword", "Old sword (+2 attack)", {"atk":2}))
        elif enemy.type == "skeleton":
            items.append(Item("bone", "Just a bone", {}))
            if random.random() < 0.4:
                items.append(Item("small_potion", "Restores HP", {"heal":15}))
        else:
            # boss loot
            items.append(Item("gold_bar", "Valuable gold", {"value": 50}))
            items.append(Item("large_potion", "Big heal", {"heal":50}))
        return items

    def _random_enemy_for_room(self, rtype):
        if rtype == "forest":
            if random.random() < 0.6:
                return Enemy("Goblin", 30, 6, 2, "goblin")
            else:
                return Enemy("Wolf", 25, 5, 3, "wolf")
        elif rtype == "cave":
            if random.random() < 0.5:
                return Enemy("Skeleton", 35, 8, 1, "skeleton")
            else:
                return Enemy("Bat", 15, 4, 0, "bat")
        else:
            return Enemy("Bandit Leader", 80, 12, 4, "boss")

    def shop(self):
        # method with responsibilities: listing, buying and special offers
        print("Welcome to the shop. You have", self.player.coins, "coins.")
        print("Items: 1) small_potion (5c) 2) rusty_sword (10c) 3) shield (15c)")
        choice = input("Buy (1/2/3) or leave: ").strip()
        if choice == "1":
            if self.player.coins >= 5:
                self.player.coins -= 5
                p = Item("small_potion", "Restores HP", {"heal":20})
                self.inventory.add(p)
                print("Bought small potion.")
            else:
                print("Not enough coins.")
        elif choice == "2":
            if self.player.coins >= 10:
                self.player.coins -= 10
                s = Item("rusty_sword", "Plus 2 attack", {"atk":2})
                self.inventory.add(s)
                print("Bought rusty sword.")
            else:
                print("Not enough coins.")
        elif choice == "3":
            if self.player.coins >= 15:
                self.player.coins -= 15
                sh = Item("shield", "Plus 2 defense", {"def":2})
                self.inventory.add(sh)
                print("Bought shield.")
            else:
                print("Not enough coins.")
        else:
            print("Leaving shop.")

    def move(self):
        # Simple movement but with message chains and repeated validation
        print("Where do you want to go?")
        for i, r in enumerate(self.world.rooms):
            print(i+1, r['name'])
        try:
            idx = int(input("Enter number: ").strip()) - 1
            if 0 <= idx < len(self.world.rooms):
                self.current_room = self.world.rooms[idx]
                print("Moved to", self.current_room['name'])
            else:
                print("Invalid choice.")
        except Exception as e:
            print("That didn't work:", e)
