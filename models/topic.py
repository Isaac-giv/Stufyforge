from datetime import datetime


class Topic:
    def __init__(self, name: str, difficulty: int):
        if not 1 <= difficulty <= 5:
            raise ValueError("Difficulty must be between 1 and 5")

        self.name = name
        self.difficulty = difficulty
        self.total_time_studied = 0  # minutes
        self.mastery = 0.0  # percentage (0–100)
        self.last_studied = None

    def study(self, minutes: int):
        if minutes <= 0:
            raise ValueError("Study time must be positive")

        self.total_time_studied += minutes
        self.last_studied = datetime.now()

        self._update_mastery(minutes)

    def _update_mastery(self, minutes: int):
        """
        Mastery increases more slowly for harder topics.
        This is intentional.
        """
        gain = (minutes / (self.difficulty * 10))
        self.mastery = min(100.0, self.mastery + gain)

    def summary(self) -> str:
        last = (
            self.last_studied.strftime("%Y-%m-%d %H:%M")
            if self.last_studied
            else "Never"
        )

        return (
            f"Topic: {self.name}\n"
            f"Difficulty: {self.difficulty}\n"
            f"Total Time Studied: {self.total_time_studied} mins\n"
            f"Mastery: {self.mastery:.1f}%\n"
            f"Last Studied: {last}"
        )
