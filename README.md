# EGame

## Description
EGame is a competitive evolutionary game designed by the research group Intelligent Software Systems at Bauhaus University Weimar.
Two populations compete to survive in a changing environment.
Endangered by extinction, hunting predators, and other factors.

## Requirements
- Python3
- Qt5
- PyQt5
- numpy

## Install Requirements
### With Packet Managers
#### Ubuntu
```
sudo apt update
sudo apt install python3 python3-pip
pip3 install PyQt5 numpy
```

#### Arch Linux
```
sudo pacman -S python python-pip # installs python3
pip3 install PyQt5 numpy
```

### With Anaconda
- [Install Anaconda on your system](https://www.anaconda.com/download)
- make sure Anaconda has [numpy](https://anaconda.org/conda-forge/numpy) and [pyqt5](https://anaconda.org/dsdale24/pyqt5) installed

## Game Elements

### Individuals
#### Populations
Populations consist of individuals which have certain traits, abilities and perceptions.
To survive, an individual has to eat something; for example, food, poison, heal potions and corpses.
They can attack individuals of other populations (but no predators) or be attacked by individuals of other populations or predators.
If an individual dies, it creates a corpse at the position where it died which can be eaten by other individuals.

Each individual has its own desires:
- seek food
- dodge poison
- seek opponents
- dodge predators
- seek heal potions
- seek corpses

All desires have a value between 0 and 1 and the sum of all desires has to be 1 in order to have the ability to specialize on certain desires.
That means, if an individual has a desire to dodge poison at 1, it will do anything to dodge the poison even if it gets eaten by opponents or predators since all other desires are at 0.

Additionally, each individual has a perception.
A perception is defined as a radius around the respective individual.
For each desire, there is also a perception:
- food perception
- poison perception
- opponent perception
- predator perception
- heal potion perception
- corpse perception

Again, each perception is a value between 0 and 1 and the sum of all perceptions has to be 1.
This sum represents an amount of pixel which can be adjusted in the configuration file and all perception values are fraction of it.

Furthermore, individuals have certain abilities (values from 0 to 1, sum = 1):
- increased armor
- increased speed
- poison resistance
- reduced breeding time
- toxicity


After a defined amount of frames, new individuals are bred into the populations based on user defined genetic algorithms.
Bad performing individuals die due to natural selection and good performing individuals survive, enabling them to multiply.

#### Predators
Predators are individuals which follow a defined rule set.
All have the same perception radius to seek individuals of the player populations and corpses.
In addition, they desire to seek individuals and corpses equally.

### Items
#### Food
Food only increases health points of individuals who eat it.

#### Poison
Poison increases the internal toxicity of an individual.
The more poison an individual eats, the faster its health decreases.

#### Heal Potions
Health potions reset the poison count and increase the health by a small amount.

#### Corpses
Corpses are like food, only that they contain a fraction of the poison of the dead individual.

## Breeding Time
<!-- TODO: to write -->

## Goal of the Game
<!-- TODO: to write -->