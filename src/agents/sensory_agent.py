import numpy as np
import cv2
import random
from scipy.spatial.transform import Rotation as R


class SensoryAgent:
    """
    Sensory Agent: Handles perception tasks using multimodal sensory inputs like vision, lidar, and audio.
    Utilizes state-of-the-art techniques for object detection, obstacle recognition, and environmental mapping.
    """

    def __init__(self, name="Sensory Agent"):
        self.name = name

    def log(self, message):
        """Log messages with the agent's name."""
        print(f"[{self.name}] {message}")

    def simulate_vision_input(self):
        """
        Simulate vision input using a state-of-the-art object detection model.
        Returns:
            dict: Detected objects with their metadata (bounding boxes, position, etc.).
        """
        self.log("Processing vision input...")
        # Simulated vision data
        objects_detected = {
            "target_object": {
                "bounding_box": [50, 50, 150, 150],  # x_min, y_min, x_max, y_max
                "position": [0.5, 0.3, 0.1],  # x, y, z in meters
                "orientation": [0, 0, 90],  # Euler angles in degrees
                "confidence": 0.95  # Detection confidence
            }
        }
        self.log(f"Vision input processed: {len(objects_detected)} objects detected.")
        return objects_detected

    def simulate_lidar_input(self):
        """
        Simulate lidar input for obstacle detection and depth estimation.
        Returns:
            np.array: 2D array representing lidar point cloud data.
        """
        self.log("Processing lidar input...")
        # Simulated lidar data as a random point cloud
        lidar_data = np.random.uniform(0, 1, (100, 3))  # 100 points with x, y, z
        self.log(f"Lidar input processed: {lidar_data.shape[0]} points detected.")
        return lidar_data

    def simulate_audio_input(self):
        """
        Simulate audio input for sound localization.
        Returns:
            dict: Sound source direction and intensity.
        """
        self.log("Processing audio input...")
        # Simulated audio data
        audio_data = {
            "direction": [30, 15],  # Azimuth and elevation angles in degrees
            "intensity": 0.8  # Normalized intensity
        }
        self.log(f"Audio input processed: Direction {audio_data['direction']} with intensity {audio_data['intensity']}.")
        return audio_data

    def recognize_object(self, object_name, vision_data):
        """
        Recognize an object using vision data.
        Args:
            object_name (str): Name of the object to recognize.
            vision_data (dict): Vision data containing detected objects.

        Returns:
            dict: Metadata of the recognized object.
        """
        self.log(f"Recognizing object '{object_name}'...")
        if object_name in vision_data:
            object_metadata = vision_data[object_name]
            self.log(f"Object '{object_name}' recognized with confidence {object_metadata['confidence']}.")
            return object_metadata
        else:
            self.log(f"Object '{object_name}' not found in vision data.")
            raise ValueError(f"Unable to recognize object: {object_name}")

    def detect_obstacles(self, lidar_data, threshold=0.2):
        """
        Detect obstacles using lidar data.
        Args:
            lidar_data (np.array): 2D array of lidar points.
            threshold (float): Distance threshold for obstacle detection.

        Returns:
            list: List of detected obstacles as (x, y, z) coordinates.
        """
        self.log("Detecting obstacles...")
        obstacles = lidar_data[np.linalg.norm(lidar_data, axis=1) < threshold]
        self.log(f"{len(obstacles)} obstacles detected within threshold {threshold} meters.")
        return obstacles.tolist()

    def localize_sound_source(self, audio_data):
        """
        Localize the direction of a sound source using audio data.
        Args:
            audio_data (dict): Audio input data.

        Returns:
            dict: Direction and intensity of the sound source.
        """
        self.log("Localizing sound source...")
        sound_direction = {
            "azimuth": audio_data["direction"][0],
            "elevation": audio_data["direction"][1],
            "intensity": audio_data["intensity"]
        }
        self.log(f"Sound source localized: Azimuth {sound_direction['azimuth']}°, "
                 f"Elevation {sound_direction['elevation']}°, Intensity {sound_direction['intensity']}.")
        return sound_direction

    def perform_task(self, details):
        """
        Perform a sensory task based on the provided details.
        Args:
            details (dict): Task details including type and parameters.

        Returns:
            dict: Results of the sensory task.
        """
        task_type = details.get("task_type", "unknown")
        self.log(f"Performing sensory task '{task_type}'...")

        if task_type == "object_recognition":
            object_name = details.get("object_name", "unknown object")
            vision_data = self.simulate_vision_input()
            return self.recognize_object(object_name, vision_data)

        elif task_type == "obstacle_detection":
            lidar_data = self.simulate_lidar_input()
            return self.detect_obstacles(lidar_data, threshold=details.get("threshold", 0.2))

        elif task_type == "sound_localization":
            audio_data = self.simulate_audio_input()
            return self.localize_sound_source(audio_data)

        else:
            self.log(f"Task type '{task_type}' is not recognized.")
            raise ValueError(f"Unknown sensory task: {task_type}")

