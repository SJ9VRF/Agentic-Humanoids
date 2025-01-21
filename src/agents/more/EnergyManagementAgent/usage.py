if __name__ == "__main__":
    energy_agent = EnergyManagementAgent()

    # Monitor battery
    energy_agent.monitor_battery()

    # Perform a sample task
    task_details = {
        "task_type": "movement",
        "speed": "normal",
        "destination": [1.0, 2.0, 0.0]
    }
    energy_agent.perform_task(task_details)

    # Optimize energy usage
    optimized_task = energy_agent.optimize_energy_usage(task_details)

    # Predict remaining runtime
    runtime = energy_agent.predict_remaining_runtime()

    # Analyze energy usage
    summary = energy_agent.analyze_energy_usage()

    # Simulate charging
    energy_agent.manage_charging()

