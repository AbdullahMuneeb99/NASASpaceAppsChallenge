# backend/space_vitals/services/communications_service.py

from datetime import datetime
from typing import List, Dict

class CommunicationService:
    """
    Handles communication between astronauts, Earth, and the space station.
    Supports sending and retrieving text/voice messages.
    """

    def __init__(self):
        # Simulated message storage
        # In production, this would connect to a database
        self.messages: List[Dict] = []

    def send_message(self, sender: str, recipient: str, channel: str, content: str, msg_type: str = "text") -> Dict:
        """
        Send a message through a communication channel.
        :param sender: The astronaut or system sending the message
        :param recipient: The target recipient
        :param channel: One of ['crew', 'earth', 'station']
        :param content: Message content
        :param msg_type: 'text' or 'voice'
        :return: The stored message
        """
        if channel not in ["crew", "earth", "station"]:
            raise ValueError(f"Invalid channel: {channel}. Must be 'crew', 'earth', or 'station'.")
        
        message = {
            "timestamp": datetime.utcnow().isoformat(),
            "sender": sender,
            "recipient": recipient,
            "channel": channel,
            "content": content,
            "type": msg_type
        }
        self.messages.append(message)
        return message

    def get_messages(self, channel: str = None) -> List[Dict]:
        """
        Retrieve all messages, optionally filtered by channel.
        :param channel: Optional filter for 'crew', 'earth', or 'station'
        :return: List of messages
        """
        if channel:
            return [m for m in self.messages if m["channel"] == channel]
        return self.messages

    def get_latest_message(self, channel: str = None) -> Dict:
        """
        Get the most recent message (optionally by channel)
        """
        messages = self.get_messages(channel)
        if not messages:
            return {}
        return messages[-1]

    def clear_messages(self):
        """
        Clear all stored messages (useful for resets or testing)
        """
        self.messages.clear()
