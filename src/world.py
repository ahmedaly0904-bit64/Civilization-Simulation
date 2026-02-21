from mesa import Model
from .nation import NationAgent

class WorldModel(Model):
    """World model - manages all nations and the simulation."""

    def __init__(self):
        """Initialize the model and create the three initial nations."""
        super().__init__()
        print("\n--- Starting Simulation ---")
        NationAgent(
            self,
            "Nation_A",
            population=1000,
            food=5000,
            food_production=10500,
            growth_rate=0.02,
            carrying_capacity=5000
        )
        agent = self.agents[-1]
        print(f"{agent.country}: Population={agent.population}, Food={agent.food}")
        NationAgent(
            self,
            "Nation_B",
            population=1500,
            food=7000,
            food_production=16000,
            growth_rate=0.025,
            carrying_capacity=7000
        )
        agent = self.agents[-1]
        print(f"{agent.country}: Population={agent.population}, Food={agent.food}")
        NationAgent(
            self,
            "Nation_C",
            population=800,
            food=4000,
            food_production=8200,
            growth_rate=0.015,
            carrying_capacity=4000
        )
        agent = self.agents[-1]
        print(f"{agent.country}: Population={agent.population}, Food={agent.food}")
        print("---------------------------\n")

    def step(self):
        """Execute one simulation step - each nation takes its turn."""
        self.agents.shuffle_do("step")

    def print_summary(self):
        '''
        summary events for each nation

        :param self: nation
        '''
        print("\n" + "=" * 70)
        print(f"{'SIMULATION SUMMARY':^70}")
        print("=" * 70)
        print(f"{'Nation':<15} {'Population':<15} {'Status':<10} {'Famines':<10} {'Food':<10} {'Wars':<10}")
        print("-" * 70)
        for agent in self.agents:
            status = "Alive" if int(agent.population) > 0 else "Extinct"
            print(f"{agent.country:<15} {int(agent.population):<15,} {status:<10} {agent.famine_count:<10} {int(agent.food_history[-1]):<10} {agent.war_count:<10}")
        print("=" * 70 + "\n")
