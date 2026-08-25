import random
from functions import stochastic_growth
from traits import Traits
WARFARE_PROBABILITY        = 0.1
FAMINE_INTENSITY_COEFFICIENT = 0.3
ENEMY_DAMAGE               = 0.1
ATTACKER_DAMAGE            = 0.04
TIME_STEP                  = 1
CONSUMPTION_PER_PERSON     = 2

class Nation:
    """
    Class representing a nation
    in the simulation with population
    and food resource management.
    """


    def __init__(
        self,
        name,
        population,
        food,
        food_production,
        growth_rate,
        carrying_capacity,
    ):
        """
        Args:
            name             : Name of the civilization
            population       : Initial population count
            food             : Initial food stock
            food_production  : Annual food production capacity
            growth_rate      : Population growth rate (r)
            carrying_capacity: Maximum sustainable population (K)
        """
        self.name              = name
        self.population        = population
        self.food              = food
        self.food_production   = food_production
        self.growth_rate       = growth_rate
        self.carrying_capacity = carrying_capacity

        self.pop_history        = [population]
        self.food_history       = [food]

        self.war_count    = 0
        self.famine_count = 0
        self.idea               = Traits()
    @property
    def is_alive(self) -> bool:
        """True if the civilization still exists."""
        return self.population > 0


    def step(self, neighbors: list = None):
        if not self.is_alive:
            return

        self._update_food()
        self._update_population()
        if neighbors:
            self._attempt_warfare(neighbors)

        self.food_history.append(self.food)

    def _update_food(self):
        consumption      = self.population * CONSUMPTION_PER_PERSON
        weather_factor   = random.uniform(0.8, 1.2)
        actual_production = self.food_production * weather_factor
        self.food        = self.food + actual_production - consumption

    def _update_population(self):
        if self.food >= 0:
            new_population = stochastic_growth(
                self.population,
                self.growth_rate,
                self.carrying_capacity,
                TIME_STEP,
            )
            delta = new_population - self.population
            self.change_populations(delta)
        else:
            deficit_per_person = abs(self.food) / max(1, self.population)
            death_rate = min(1.0, deficit_per_person * FAMINE_INTENSITY_COEFFICIENT)
            deaths = int(self.population * death_rate)
            self.change_populations(-deaths)
            self.food = 0
            self.famine_count += 1

    def _attempt_warfare(self, neighbors: list):
        enemies = [n for n in neighbors if n.is_alive]
        if enemies and random.random() < WARFARE_PROBABILITY:
            enemy = random.choice(enemies)
            if self.population > enemy.population:
                self.attack(enemy)

    def receive_damage(self, amount: float):
        deaths = int(self.population * amount)
        if self.population - deaths < 1:
            deaths = self.population
        self.change_populations(-deaths)

    def border_attrition(self, border_length: int):
        damage = min(0.5,0.2 * border_length / self.population)
        self.receive_damage(damage)
    def attack(self, enemy: "Nation"):
        enemy.receive_damage(ENEMY_DAMAGE)
        enemy.war_count += 1    
        self.receive_damage(ATTACKER_DAMAGE)
        self.war_count += 1
    def change_populations(self, delta:float):
        self.population = max(0, self.population + delta)
    def __repr__(self) -> str:
        return (
            f"Nation({self.name} | "
            f"pop={int(self.population):,} | "
            f"{'Alive' if self.is_alive else 'Extinct'})"
        )