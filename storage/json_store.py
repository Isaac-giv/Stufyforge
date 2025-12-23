import json
from pathlib import Path
from models.topic import Topic
from models.study_session import StudySession


class JSONStore:
    def __init__(self, filepath="data/study_data.json"):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(exist_ok=True)
        if not self.filepath.exists():
            self._init_file()

    def _init_file(self):
        data = {"topics": [], "sessions": []}
        self._write_file(data)

    def _write_file(self, data: dict):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)

    def save(self, topics: list, sessions: list):
        data = {
            "topics": [
                {
                    "name": t.name,
                    "difficulty": t.difficulty,
                    "total_time_studied": t.total_time_studied,
                    "mastery": t.mastery,
                    "last_studied": t.last_studied.isoformat() if t.last_studied else None,
                }
                for t in topics
            ],
            "sessions": [s.to_dict() for s in sessions],
        }
        self._write_file(data)

    def load(self):
        with open(self.filepath, "r") as f:
            data = json.load(f)

        topics = []
        for t in data["topics"]:
            topic = Topic(t["name"], t["difficulty"])
            topic.total_time_studied = t["total_time_studied"]
            topic.mastery = t["mastery"]
            topic.last_studied = (
                None if t["last_studied"] is None else Topic._parse_date(t["last_studied"])
            )
            topics.append(topic)

        sessions = [StudySession.from_dict(s) for s in data["sessions"]]

        return topics, sessions
