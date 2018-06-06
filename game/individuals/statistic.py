
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