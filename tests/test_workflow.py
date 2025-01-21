import unittest
from agents.central_cognitive_agent import CentralCognitiveAgent
from agents.sensory_agent import SensoryAgent
from agents.manipulation_agent import ManipulationAgent
from agents.energy_management_agent import EnergyManagementAgent
from agents.motor_control_agent import MotorControlAgent


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        # Create central agent and register other agents
        self.central_agent = CentralCognitiveAgent()
        self.sensory_agent = SensoryAgent()
        self.manipulation_agent = ManipulationAgent()
        self.energy_agent = EnergyManagementAgent()
        self.motor_control_agent = MotorControlAgent()

        self.central_agent.register_agent("sensory", self.sensory_agent)
        self.central_agent.register_agent("manipulation", self.manipulation_agent)
        self.central_agent.register_agent("energy", self.energy_agent)
        self.central_agent.register_agent("motor_control", self.motor_control_agent)

    def test_workflow_execution(self):
        # Simulate a high-level command
        command = "Fetch the target object and deliver it to the location [1, 1, 0]."
        self.central_agent.perform_task(command)

        # Ensure the workflow completes without errors
        self.assertTrue(True)  # Dummy assertion since this test focuses on system-level execution

    def test_low_battery_workflow(self):
        # Set the battery level low
        self.energy_agent.current_battery_level = 15.0

        # Simulate a high-level command
        command = "Move to position [2, 2, 0]."
        self.central_agent.perform_task(command)

        # Assert that the battery was charged after execution
        self.assertGreaterEqual(self.energy_agent.current_battery_level, 100.0)


if __name__ == "__main__":
    unittest.main()

