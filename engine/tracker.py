from models.topic import Topic
from models.study_session import StudySession


class StudyTracker:
    def __init__(self):
        self.topics = {}

    def add_topic(self, topic: Topic):
        if topic.name in self.topics:
            raise ValueError(f"Topic '{topic.name}' already exists")

        self.topics[topic.name] = topic

    def log_session(self, session: StudySession):
        if session.topic_name not in self.topics:
            raise ValueError(f"Unknown topic '{session.topic_name}'")

        topic = self.topics[session.topic_name]
        topic.study(session.duration)

    def get_topic(self, name: str) -> Topic:
        return self.topics.get(name)

    def course_progress(self) -> float:
        if not self.topics:
            return 0.0

        total = sum(topic.mastery for topic in self.topics.values())
        return total / len(self.topics)

    def summary(self) -> str:
        lines = ["Study Progress Summary\n"]
        for topic in self.topics.values():
            lines.append(f"- {topic.name}: {topic.mastery:.1f}%")

        lines.append(f"\nOverall Progress: {self.course_progress():.1f}%")
        return "\n".join(lines)
