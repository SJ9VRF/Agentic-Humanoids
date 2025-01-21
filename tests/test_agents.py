import unittest
from agents.sensory_agent import SensoryAgent
from agents.manipulation_agent import ManipulationAgent
from agents.energy_management_agent import EnergyManagementAgent
from agents.motor_control_agent import MotorControlAgent


class TestAgents(unittest.TestCase):

    def test_sensory_agent_object_recognition(self):
        sensory_agent = SensoryAgent()
        task_details = {
            "task_type": "object_recognition",
            "object_name": "target_object"
        }
        result = sensory_agent.perform_task(task_details)
        self.assertIsInstance(result, dict)
        self.assertIn("position", result)
        self.assertIn("orientation", result)

    def test_manipulation_agent_task_execution(self):
        manipulation_agent = ManipulationAgent()
        task_details = {
            "task_type": "grasping",
            "object_name": "target_object"
        }
        result = manipulation_agent.perform_task(task_details)
        self.assertTrue(result)

    def test_energy_management_agent_battery_monitoring(self):
        energy_agent = EnergyManagementAgent()
        energy_agent.current_battery_level = 50.0
        battery_status = energy_agent.monitor_battery()
        self.assertEqual(battery_status, 50.0)

    def test_motor_control_agent_movement(self):
        motor_control_agent = MotorControlAgent()
        task_details = {
            "task_type": "movement",
            "destination": [1.0, 1.0, 0.0],
            "orientation": [0, 0, 90]
        }
        result = motor_control_agent.perform_task(task_details)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()

