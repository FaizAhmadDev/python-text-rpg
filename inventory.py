class Item:
    def __init__(self, name, desc, props):
        self.name = name
        self.desc = desc
        # props is a dict like {"heal":20} or {"atk":2}
        self.props = props

class Inventory:
    def __init__(self):
        # Data clump: items stored as tuples sometimes, dict other times in student's code
        self.items = []
        self.gold = 0

    def add(self, item):
        # sometimes we add item objects, sometimes simple tuples
        if isinstance(item, Item):
            self.items.append(item)
        else:
            self.items.append(Item(item[0], item[1], item[2]))
        print(f"Added {item.name if isinstance(item, Item) else item[0]} to inventory.")

    def show(self):
        print("Inventory:")
        if not self.items:
            print(" (empty)")
            return
        for i, it in enumerate(self.items):
            print(i+1, it.name, "-", it.desc)
