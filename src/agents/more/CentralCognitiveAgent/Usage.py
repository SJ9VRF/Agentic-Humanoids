from agents.sensory_agent import SensoryAgent
from agents.planning_agent import PlanningAgent
from agents.manipulation_agent import ManipulationAgent
from agents.motor_control_agent import MotorControlAgent

if __name__ == "__main__":
    # Create central cognitive agent
    central_agent = CentralCognitiveAgent()

    # Create and register agents
    sensory_agent = SensoryAgent()
    planning_agent = PlanningAgent()
    manipulation_agent = ManipulationAgent()
    motor_control_agent = MotorControlAgent()

    central_agent.register_agent("sensory", sensory_agent)
    central_agent.register_agent("planning", planning_agent)
    central_agent.register_agent("manipulation", manipulation_agent)
    central_agent.register_agent("motor_control", motor_control_agent)

    # Example command
    command = "Fetch the target object and deliver it to the location [1, 2, 0]."
    central_agent.perform_task(command)

