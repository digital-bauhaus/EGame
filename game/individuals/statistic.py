
class Statistic:
    def __init__(self):
        # general
        self.time_survived = 0

        # items
        self.food_eaten = 0
        self.poison_eaten = 0
        self.consumed_potions = 0
        self.consumed_corpses = 0
        
        # competitions
        self.enemies_attacked = 0
        self.attacked_by_opponents = 0
        self.attacked_by_predators = 0

        # perception
        self.food_seen = 0
        self.poison_seen = 0
        self.potions_seen = 0
        self.opponents_seen = 0
        self.predators_seen = 0
        self.corpses_seen = 0

    def increment(self, type):
        if type == "food":
            self.food_seen += 1
        elif type == "poison":
            self.poison_seen += 1
        elif type == "health_potion":
            self.potions_seen += 1
        elif type == "predators":
            self.predators_seen += 1
        elif type == "corpse":
            self.corpses_seen += 1
        elif "pop" in type:
            self.opponents_seen += 1
        else:
            raise Exception("statistic increment error! " + type + " not found")

    def print(self):
        print("frames survived", self.time_survived)
        print("food eaten", self.food_eaten)
        print("poison eaten", self.poison_eaten)
        print("consumed health potions", self.consumed_potions)
        print("consumed corpses", self.consumed_corpses)
        print("enemies attacked", self.enemies_attacked)
        print("attacked by opponents", self.attacked_by_opponents)
        print("attacked by predators", self.attacked_by_predators)
        print("food seen", self.food_seen)
        print("poison seen", self.poison_seen)
        print("health potions seen", self.potions_seen)
        print("opponents seen", self.opponents_seen)
        print("predators seen", self.predators_seen)
        print("corpses seen", self.corpses_seen)