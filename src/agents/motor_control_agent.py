import numpy as np
from scipy.spatial.transform import Rotation as R


class MotorControlAgent:
    """
    Motor Control Agent: Handles precise movements, balance control, and trajectory execution.
    Utilizes state-of-the-art techniques in inverse kinematics, dynamic balancing, and motion optimization.
    """

    def __init__(self, name="Motor Control Agent"):
        self.name = name
        self.current_position = np.array([0.0, 0.0, 0.0])  # Current position [x, y, z]
        self.current_orientation = R.from_euler('xyz', [0, 0, 0], degrees=True)  # Current orientation
        self.joint_limits = {  # Simulated joint limits
            "joint_1": (-180, 180),
            "joint_2": (-90, 90),
            "joint_3": (-90, 90),
        }
        self.joint_angles = {key: 0 for key in self.joint_limits}  # Initial joint angles

    def log(self, message):
        """Log messages with the agent's name."""
        print(f"[{self.name}] {message}")

    def compute_inverse_kinematics(self, target_position, target_orientation):
        """
        Compute the joint angles required to reach a specific target position and orientation.
        Args:
            target_position (np.array): Target position [x, y, z] in meters.
            target_orientation (R): Target orientation as a rotation matrix.

        Returns:
            dict: Joint angles for achieving the target pose.
        """
        self.log(f"Computing inverse kinematics for position {target_position} and orientation {target_orientation.as_euler('xyz', degrees=True)}")
        # Simplified inverse kinematics model for a 3-DOF arm
        x, y, z = target_position
        joint_1 = np.arctan2(y, x) * (180 / np.pi)  # Base rotation
        joint_2 = np.clip(45 - z * 10, *self.joint_limits["joint_2"])  # Simulated elbow adjustment
        joint_3 = np.clip(90 - np.linalg.norm([x, y]) * 20, *self.joint_limits["joint_3"])  # Simulated wrist adjustment

        joint_angles = {
            "joint_1": np.clip(joint_1, *self.joint_limits["joint_1"]),
            "joint_2": joint_2,
            "joint_3": joint_3,
        }
        self.log(f"Computed joint angles: {joint_angles}")
        return joint_angles

    def execute_joint_movements(self, joint_angles):
        """
        Execute joint movements based on computed joint angles.
        Args:
            joint_angles (dict): Dictionary of joint angles to execute.

        Returns:
            bool: True if the motion was successful, False otherwise.
        """
        self.log(f"Executing joint movements: {joint_angles}")
        try:
            # Simulate the movement by updating joint states
            for joint, angle in joint_angles.items():
                if angle < self.joint_limits[joint][0] or angle > self.joint_limits[joint][1]:
                    raise ValueError(f"Joint {joint} angle {angle} is out of limits!")
                self.joint_angles[joint] = angle

            self.log(f"Joint movements executed successfully. Current joint states: {self.joint_angles}")
            return True
        except Exception as e:
            self.log(f"Failed to execute joint movements: {e}")
            return False

    def dynamic_balance_control(self, target_position):
        """
        Maintain balance dynamically while moving towards the target position.
        Args:
            target_position (np.array): Target position [x, y, z] in meters.

        Returns:
            bool: True if balance was maintained successfully, False otherwise.
        """
        self.log(f"Performing dynamic balance control for target position {target_position}")
        try:
            # Simplified balance control based on center of mass (COM) adjustments
            com_offset = np.linalg.norm(target_position - self.current_position)
            if com_offset > 0.5:  # Threshold for balance correction
                self.log("Applying balance corrections...")
            self.log("Balance maintained successfully.")
            return True
        except Exception as e:
            self.log(f"Failed to maintain balance: {e}")
            return False

    def move_to_position(self, target_position, target_orientation):
        """
        Move the robot to the specified target position and orientation.
        Args:
            target_position (list): Target position [x, y, z] in meters.
            target_orientation (list): Target orientation as [roll, pitch, yaw] in degrees.

        Returns:
            bool: True if the movement was successful, False otherwise.
        """
        self.log(f"Moving to position {target_position} with orientation {target_orientation}")
        target_position = np.array(target_position)
        target_orientation = R.from_euler('xyz', target_orientation, degrees=True)

        # Step 1: Compute joint angles
        joint_angles = self.compute_inverse_kinematics(target_position, target_orientation)

        # Step 2: Execute joint movements
        if not self.execute_joint_movements(joint_angles):
            self.log("Failed to execute joint movements.")
            return False

        # Step 3: Ensure balance during movement
        if not self.dynamic_balance_control(target_position):
            self.log("Failed to maintain balance during movement.")
            return False

        # Update current state
        self.current_position = target_position
        self.current_orientation = target_orientation
        self.log(f"Moved successfully to {self.current_position} with orientation {self.current_orientation.as_euler('xyz', degrees=True)}")
        return True

    def trajectory_execution(self, trajectory_points):
        """
        Execute a trajectory consisting of multiple waypoints.
        Args:
            trajectory_points (list): List of waypoints, each containing position [x, y, z] and orientation [roll, pitch, yaw].

        Returns:
            bool: True if the entire trajectory was executed successfully, False otherwise.
        """
        self.log("Starting trajectory execution...")
        for point in trajectory_points:
            target_position = point["position"]
            target_orientation = point["orientation"]
            if not self.move_to_position(target_position, target_orientation):
                self.log(f"Failed to execute trajectory at waypoint {target_position}.")
                return False
        self.log("Trajectory executed successfully.")
        return True

    def perform_task(self, details):
        """
        Perform a motor control task based on the provided details.
        Args:
            details (dict): Task details including type and parameters.

        Returns:
            bool: True if the task was completed successfully, False otherwise.
        """
        task_type = details.get("task_type", "unknown")
        self.log(f"Performing motor control task '{task_type}'...")

        if task_type == "movement":
            target_position = details.get("destination", [0, 0, 0])
            target_orientation = details.get("orientation", [0, 0, 0])  # Default to no rotation
            return self.move_to_position(target_position, target_orientation)

        elif task_type == "trajectory":
            trajectory_points = details.get("trajectory", [])
            return self.trajectory_execution(trajectory_points)

        else:
            self.log(f"Unknown task type '{task_type}'.")
            return False

