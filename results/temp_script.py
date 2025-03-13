from random_access import RandomAccessSimulator
sim = RandomAccessSimulator('results')
result = sim.run_simulation(0)
import sys
sys.stdout.write(str(result))