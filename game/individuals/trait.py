from game.individuals.invalid_dna_exception import InvalidDNAException

class Trait:
    def check_dna(self, dna):
        """
        check if the dna is valid
        """
        eps = 1e-10
        if abs(1 - sum(dna)) > eps:
            raise InvalidDNAException("Desire DNA does not sum up to 1.0 !")
