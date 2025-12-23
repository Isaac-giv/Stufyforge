from models.topic import Topic
from models.study_session import StudySession
from engine.tracker import StudyTracker
from engine.recommender import Recommender
from storage.json_store import JSONStore

# Color support for Windows
from colorama import init, Fore, Style
init(autoreset=True)

GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
RESET = Style.RESET_ALL


def progress_bar(percentage, length=20):
    """
    Returns a string representing a progress bar.
    percentage: 0-100
    length: number of characters in the bar
    """
    filled_length = int(length * percentage // 100)
    bar = f"{GREEN}{'█'*filled_length}{RESET}{'-'*(length-filled_length)} {percentage:.0f}%"
    return bar


def main():
    # Initialize storage and load existing data
    store = JSONStore()
    topics, sessions = store.load()

    # Initialize tracker and add topics
    tracker = StudyTracker()
    for t in topics:
        tracker.add_topic(t)

    # Replay past sessions
    for s in sessions:
        tracker.log_session(s)

    print(f"{GREEN}Welcome to StudyForge CLI!{RESET}")
    print("Commands: add-topic, log-session, recommend, summary, list-topics, delete-topic, help, exit")

    while True:
        command = input("\n> ").strip().lower()

        if command == "exit":
            store.save(list(tracker.topics.values()), sessions)
            print(f"{GREEN}Progress saved. Goodbye!{RESET}")
            break

        elif command.startswith("add-topic"):
            try:
                _, name, difficulty = command.split()
                t = Topic(name, int(difficulty))
                tracker.add_topic(t)
                print(f"{GREEN}Added topic '{name}' with difficulty {difficulty}{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")

        elif command.startswith("log-session"):
            try:
                _, name, duration = command.split()
                s = StudySession(name, int(duration))
                tracker.log_session(s)
                sessions.append(s)
                print(f"{GREEN}Logged {duration} minutes for '{name}'{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")

        elif command == "recommend":
            recommender = Recommender(list(tracker.topics.values()))
            next_topic = recommender.recommend()
            if next_topic:
                print(f"{YELLOW}Next topic to study: {next_topic.name}{RESET}")
            else:
                print(f"{RED}No topics available.{RESET}")

        elif command == "summary":
            if tracker.topics:
                print("Study Progress Summary:")
                for t in tracker.topics.values():
                    bar = progress_bar(t.mastery)
                    print(f"{t.name.ljust(15)} {bar}")
                overall = tracker.course_progress()
                print(f"\nOverall Progress: {overall:.1f}%")
            else:
                print(f"{RED}No topics added yet.{RESET}")

        elif command == "list-topics":
            if tracker.topics:
                print("Topics:")
                for t in tracker.topics.values():
                    print(f"- {t.name} (Difficulty: {t.difficulty}, Mastery: {t.mastery:.1f}%)")
            else:
                print(f"{RED}No topics added yet.{RESET}")

        elif command.startswith("delete-topic"):
            try:
                _, name = command.split()
                if name in tracker.topics:
                    del tracker.topics[name]
                    print(f"{GREEN}Deleted topic '{name}'{RESET}")
                else:
                    print(f"{RED}No topic named '{name}'{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")

        elif command == "help":
            print("Available commands:")
            print("add-topic <name> <difficulty>")
            print("log-session <name> <minutes>")
            print("recommend")
            print("summary")
            print("list-topics")
            print("delete-topic <name>")
            print("help")
            print("exit")

        else:
            print(f"{RED}Unknown command. Type 'help' to see available commands.{RESET}")


if __name__ == "__main__":
    main()
