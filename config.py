import json

class Config:
    def __init__(self, config):
        with open(config, "r") as f:
            json_data = json.load(f)
        self.game = json_data['Game']
        parameter =  self.game['parameter']
        self.global_config = parameter['global_parameter']
        self.individuals = parameter['individuals']
        self.predators = parameter['predators']
        self.items = parameter['items']
        self.ability_base = parameter['ability_base']
