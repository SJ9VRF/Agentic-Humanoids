from utils.logger import Logger

logger = Logger("RobotTestLogger")

logger.info("System initialized successfully.")
logger.warning("Low battery detected.")
logger.error("Task execution failed.")
logger.debug("Debugging motor control values...")
