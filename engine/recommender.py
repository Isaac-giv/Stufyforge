from datetime import datetime, timedelta


class Recommender:
    def __init__(self, topics: list):
        self.topics = topics

    def recommend(self):
        """
        Returns the topic that should be studied next.
        Uses mastery, difficulty, and last studied date.
        """
        best_score = -1
        best_topic = None
        now = datetime.now()

        for topic in self.topics:
            # Recency factor: days since last studied
            if topic.last_studied:
                days = (now - topic.last_studied).days
            else:
                days = 999  # never studied topics are top priority

            # Lower mastery and higher difficulty increase priority
            score = (100 - topic.mastery) * topic.difficulty + days

            if score > best_score:
                best_score = score
                best_topic = topic

        return best_topic
