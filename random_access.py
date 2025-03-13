import os
import random
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RandomAccessSimulator:
    def __init__(self, output_dir: str = "results", preambles: int = 64):
        """Initialize the simulator with output directory and number of PRACH preambles."""
        self.output_dir = output_dir
        self.preambles = preambles
        self.results: Dict[str, List] = {
            "ue_load": [],
            "prach_success_rate": [],
            "collision_probability": [],
            "access_delay": [],
            "retransmissions": []
        }
        os.makedirs(self.output_dir, exist_ok=True)

    def run_simulation(self, ue_load: int, max_attempts: int = 5, base_delay: float = 0.01) -> Dict:
        """Simulate RA process for given UE load."""
        logger.info(f"Running simulation with UE load: {ue_load}")
        
        successful_ues = set()  # Track UEs that have succeeded
        collisions = 0
        total_attempts = 0
        delays = []
        retransmissions = 0
        
        # Simulate RA attempts
        for attempt in range(max_attempts):
            # Only simulate UEs that haven't succeeded yet
            remaining_ues = [i for i in range(ue_load) if i not in successful_ues]
            if not remaining_ues:
                break  # All UEs have succeeded
            
            # Each remaining UE picks a preamble
            preamble_choices = {ue: random.randint(0, self.preambles - 1) for ue in remaining_ues}
            preamble_counts = {}
            
            # Count how many UEs picked each preamble
            for ue, preamble in preamble_choices.items():
                preamble_counts[preamble] = preamble_counts.get(preamble, 0) + 1
            
            # Check for successes and collisions
            for ue, preamble in preamble_choices.items():
                if preamble_counts[preamble] == 1:  # No collision
                    if ue not in successful_ues:  # First success for this UE
                        successful_ues.add(ue)
                        delay = base_delay * (attempt + 1)
                        delays.append(delay)
                else:
                    collisions += 1
                    if attempt > 0:
                        retransmissions += 1
            
            total_attempts += len(remaining_ues)

        # Calculate metrics
        success_rate = (len(successful_ues) / ue_load * 100) if ue_load > 0 else 0  # Percentage
        collision_prob = collisions / total_attempts if total_attempts > 0 else 0
        collision_prob *= 100  # Percentage
        avg_delay = sum(delays) / len(delays) if delays else 0

        results = {
            "ue_load": ue_load,
            "prach_success_rate": success_rate,
            "collision_probability": collision_prob,
            "access_delay": avg_delay,
            "retransmissions": retransmissions
        }
        
        self.results["ue_load"].append(ue_load)
        self.results["prach_success_rate"].append(success_rate)
        self.results["collision_probability"].append(collision_prob)
        self.results["access_delay"].append(avg_delay)
        self.results["retransmissions"].append(retransmissions)
        
        logger.info(f"Simulation results for UE load {ue_load}: {results}")
        return results

    def save_results(self, format: str = "csv"):
        """Save results to a file."""
        df = pd.DataFrame(self.results)
        if format == "csv":
            output_file = f"{self.output_dir}/results.csv"
            df.to_csv(output_file, index=False)
            logger.info(f"Results saved to {output_file}")
        elif format == "json":
            output_file = f"{self.output_dir}/results.json"
            df.to_json(output_file, orient="records")
            logger.info(f"Results saved to {output_file}")

    def visualize_results(self):
        """Visualize results using Matplotlib."""
        df = pd.DataFrame(self.results)
        
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 2, 1)
        plt.plot(df["ue_load"].to_numpy(), df["prach_success_rate"].to_numpy(), marker='o')
        plt.title("PRACH Success Rate vs UE Load")
        plt.xlabel("UE Load")
        plt.ylabel("Success Rate (%)")  # Updated label
        
        plt.subplot(2, 2, 2)
        plt.plot(df["ue_load"].to_numpy(), df["collision_probability"].to_numpy(), marker='o', color='r')
        plt.title("Collision Probability vs UE Load")
        plt.xlabel("UE Load")
        plt.ylabel("Collision Probability")
        
        plt.subplot(2, 2, 3)
        plt.plot(df["ue_load"].to_numpy(), df["access_delay"].to_numpy(), marker='o', color='g')
        plt.title("Average Access Delay vs UE Load")
        plt.xlabel("UE Load")
        plt.ylabel("Delay (s)")
        
        plt.subplot(2, 2, 4)
        plt.plot(df["ue_load"].to_numpy(), df["retransmissions"].to_numpy(), marker='o', color='b')
        plt.title("Retransmissions vs UE Load")
        plt.xlabel("UE Load")
        plt.ylabel("Retransmissions")
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/results_plot.png")
        plt.show()
        logger.info("Visualization completed.")

if __name__ == "__main__":
    simulator = RandomAccessSimulator()
    ue_loads = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    for load in ue_loads:
        simulator.run_simulation(load)
    
    simulator.save_results("csv")
    simulator.visualize_results()