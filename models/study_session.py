from datetime import datetime


class StudySession:
    def __init__(self, topic_name: str, duration: int, timestamp=None):
        if duration <= 0:
            raise ValueError("Study duration must be positive")

        self.topic_name = topic_name
        self.duration = duration  # minutes
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> dict:
        return {
            "topic_name": self.topic_name,
            "duration": self.duration,
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict):
        return StudySession(
            topic_name=data["topic_name"],
            duration=data["duration"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )
