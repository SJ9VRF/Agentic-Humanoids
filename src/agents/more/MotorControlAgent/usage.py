if __name__ == "__main__":
    motor_control_agent = MotorControlAgent()

    # Move to a specific position and orientation
    task_details = {
        "task_type": "movement",
        "destination": [1.0, 1.0, 0.0],
        "orientation": [0, 0, 90]  # Roll, pitch, yaw in degrees
    }
    success = motor_control_agent.perform_task(task_details)
    print(f"Task success: {success}")

    # Execute a trajectory
    trajectory_task = {
        "task_type": "trajectory",
        "trajectory": [
            {"position": [0.5, 0.5, 0.0], "orientation": [0, 0, 45]},
            {"position": [1.0, 1.0, 0.0], "orientation": [0, 0, 90]},
            {"position": [1.5, 1.5, 0.0], "orientation": [0, 0, 135]},
        ]
    }
    success = motor_control_agent.perform_task(trajectory_task)
    print(f"Trajectory success: {success}")
