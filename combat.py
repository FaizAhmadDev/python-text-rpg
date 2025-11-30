import random

class Combat:
    def fight(self, player, enemy, inventory):
        # method handling full fight choreography
        print("=== Combat Start ===")
        while player.hp > 0 and enemy.hp > 0:
            print("Your move: attack / defend / item / run")
            choice = input(">> ").strip().lower()
            if choice == "attack":
                player.attack_enemy(enemy)
                if enemy.hp <= 0:
                    print("Enemy dropped loot.")
                    return "won"
                # enemy turn
                enemy.attack_player(player)
                if player.hp <= 0:
                    return "lost"
            elif choice == "defend":
                # temporary field 
                saved = player.defense
                player.defense += 2
                print("You brace yourself.")
                enemy.attack_player(player)
                player.defense = saved
                if player.hp <= 0:
                    return "lost"
            elif choice == "item":
                inventory.show()
                idx = input("Use which item number? ").strip()
                try:
                    idxn = int(idx) - 1
                    if 0 <= idxn < len(inventory.items):
                        item = inventory.items.pop(idxn)
                        player.use_item(item)
                    else:
                        print("Invalid item.")
                except:
                    print("Bad input.")
            elif choice == "run":
                # simple chance
                if random.random() < 0.5:
                    print("You ran away!")
                    return "ran"
                else:
                    print("Couldn't escape.")
                    enemy.attack_player(player)
            else:
                print("Invalid action.")
        print("=== Combat End ===")
        if player.hp <= 0:
            return "lost"
        return "won"
