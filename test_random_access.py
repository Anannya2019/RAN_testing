import pytest
from random_access import RandomAccessSimulator
import os
import pandas as pd

@pytest.fixture
def simulator(tmp_path):
    """Fixture to create a simulator instance with a temporary directory."""
    output_dir = str(tmp_path)
    return RandomAccessSimulator(output_dir)

def test_init(simulator):
    assert os.path.exists(simulator.output_dir)
    assert isinstance(simulator.results, dict)
    assert len(simulator.results["ue_load"]) == 0

def test_run_simulation(simulator):
    result = simulator.run_simulation(ue_load=10)
    assert isinstance(result, dict)
    assert "ue_load" in result
    assert result["ue_load"] == 10
    assert 0 <= result["prach_success_rate"] <= 100  # Updated to match percentage range
    assert 0 <= result["collision_probability"] <= 1

def test_save_results_csv(simulator):
    simulator.run_simulation(ue_load=10)
    simulator.save_results("csv")
    output_file = f"{simulator.output_dir}/results.csv"
    assert os.path.exists(output_file)
    df = pd.read_csv(output_file)
    assert len(df) == 1
    assert df["ue_load"].iloc[0] == 10

def test_save_results_json(simulator):
    simulator.run_simulation(ue_load=10)
    simulator.save_results("json")
    output_file = f"{simulator.output_dir}/results.json"
    assert os.path.exists(output_file)
    df = pd.read_json(output_file)
    assert len(df) == 1
    assert df["ue_load"].iloc[0] == 10

def test_visualize_results(simulator, monkeypatch):
    simulator.run_simulation(ue_load=10)
    simulator.run_simulation(ue_load=20)
    monkeypatch.setattr("matplotlib.pyplot.show", lambda: None)
    simulator.visualize_results()
    assert os.path.exists(f"{simulator.output_dir}/results_plot.png")

if __name__ == "__main__":
    pytest.main(["-v"])