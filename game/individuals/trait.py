from game.individuals.invalid_dna_exception import InvalidDNAException

class Trait:
    def check_dna(self, dna):
        """
        check if the dna is valid
        """
        eps = 1e-5
        if abs(1 - sum(dna)) > eps:
            raise InvalidDNAException(dna, "DNA does not sum up to 1.0 !")
        for value in dna:
            if value < 0:
                raise InvalidDNAException(dna, "DNA is negative!")