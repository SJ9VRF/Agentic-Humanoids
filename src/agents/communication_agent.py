import random
from transformers import pipeline
from gtts import gTTS
import os
import tempfile


class CommunicationAgent:
    """
    Communication Agent: Handles verbal and non-verbal communication with users.
    Utilizes state-of-the-art NLP and text-to-speech (TTS) technologies for effective interaction.
    """

    def __init__(self, name="Communication Agent"):
        self.name = name
        self.text_generator = pipeline("text-generation", model="gpt2")  # For generating text-based responses
        self.sentiment_analyzer = pipeline("sentiment-analysis")  # For understanding user sentiment

    def log(self, message):
        """Log messages with the agent's name."""
        print(f"[{self.name}] {message}")

    def analyze_user_input(self, user_input):
        """
        Analyze user input for intent and sentiment.
        Args:
            user_input (str): User's input message.

        Returns:
            dict: Detected intent and sentiment.
        """
        self.log(f"Analyzing user input: '{user_input}'")
        # Simulate intent detection
        intent = self.detect_intent(user_input)
        # Analyze sentiment
        sentiment = self.sentiment_analyzer(user_input)[0]
        self.log(f"Detected intent: {intent}, Sentiment: {sentiment}")
        return {"intent": intent, "sentiment": sentiment}

    def detect_intent(self, user_input):
        """
        Detect the user's intent based on input.
        Args:
            user_input (str): User's input message.

        Returns:
            str: Detected intent (e.g., "query", "command", "feedback").
        """
        # Simple intent detection based on keywords
        if any(keyword in user_input.lower() for keyword in ["what", "how", "why"]):
            return "query"
        elif any(keyword in user_input.lower() for keyword in ["do", "perform", "execute"]):
            return "command"
        elif any(keyword in user_input.lower() for keyword in ["good", "bad", "suggest"]):
            return "feedback"
        else:
            return "unknown"

    def generate_response(self, intent, sentiment):
        """
        Generate an appropriate response based on detected intent and sentiment.
        Args:
            intent (str): User's detected intent.
            sentiment (dict): User's sentiment analysis result.

        Returns:
            str: Generated response.
        """
        self.log(f"Generating response for intent: {intent}, sentiment: {sentiment}")
        if intent == "query":
            response = self.text_generator("This is a response to your query.", max_length=50)[0]["generated_text"]
        elif intent == "command":
            response = "Executing your command now. Please wait..."
        elif intent == "feedback":
            if sentiment["label"] == "POSITIVE":
                response = "Thank you for your positive feedback! I'll keep improving."
            else:
                response = "I appreciate your feedback and will work on improvements."
        else:
            response = "I'm sorry, I didn't understand your request. Could you please rephrase?"
        self.log(f"Generated response: '{response}'")
        return response

    def text_to_speech(self, response):
        """
        Convert the generated response to speech using a TTS engine.
        Args:
            response (str): The text response to convert to speech.

        Returns:
            None
        """
        self.log("Converting response to speech...")
        tts = gTTS(text=response, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            os.system(f"start {temp_audio.name}")
        self.log("Response played as speech.")

    def multimodal_feedback(self, response):
        """
        Simulate non-verbal feedback such as gestures or LED patterns.
        Args:
            response (str): The response text to guide feedback.

        Returns:
            str: Simulated non-verbal feedback description.
        """
        self.log("Providing multimodal feedback...")
        # Simulate gestures or visual cues
        feedback_options = ["nods head", "blinks LED light", "waves hand"]
        feedback = random.choice(feedback_options)
        self.log(f"Non-verbal feedback: {feedback}")
        return feedback

    def report_status(self, status):
        """
        Report the robot's status to the user.
        Args:
            status (str): Status message to report.

        Returns:
            None
        """
        self.log(f"Reporting status: {status}")
        print(f"[Status Report] {status}")

    def perform_task(self, user_input):
        """
        Perform the complete communication workflow for a user input.
        Args:
            user_input (str): User's input message.

        Returns:
            None
        """
        # Analyze input
        analysis = self.analyze_user_input(user_input)

        # Generate response
        response = self.generate_response(analysis["intent"], analysis["sentiment"])

        # Provide verbal and non-verbal feedback
        self.text_to_speech(response)
        self.multimodal_feedback(response)

        # Report final status
        self.report_status(f"Task based on input '{user_input}' completed.")

