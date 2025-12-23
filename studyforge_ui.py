import tkinter as tk
from tkinter import ttk, messagebox
from models.topic import Topic
from models.study_session import StudySession
from engine.tracker import StudyTracker
from engine.recommender import Recommender
from storage.json_store import JSONStore

# Initialize storage and tracker
store = JSONStore()
topics_data, sessions_data = store.load()

tracker = StudyTracker()
for t in topics_data:
    tracker.add_topic(t)
for s in sessions_data:
    tracker.log_session(s)


class StudyForgeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("StudyForge")
        self.geometry("600x500")
        self.resizable(False, False)

        # Topic List Frame
        self.topic_frame = tk.Frame(self)
        self.topic_frame.pack(pady=10)

        tk.Label(self.topic_frame, text="Topics", font=("Arial", 14, "bold")).pack()

        self.topic_list_frame = tk.Frame(self.topic_frame)
        self.topic_list_frame.pack()

        # Buttons Frame
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        tk.Button(self.button_frame, text="Add Topic", command=self.add_topic_popup).grid(row=0, column=0, padx=5)
        tk.Button(self.button_frame, text="Log Session", command=self.log_session_popup).grid(row=0, column=1, padx=5)
        tk.Button(self.button_frame, text="Recommend", command=self.recommend_topic).grid(row=0, column=2, padx=5)
        tk.Button(self.button_frame, text="Save & Exit", command=self.save_and_exit).grid(row=0, column=3, padx=5)

        self.refresh_topics()

    def refresh_topics(self):
        # Clear old widgets
        for widget in self.topic_list_frame.winfo_children():
            widget.destroy()

        # Display topics with progress bars
        for topic in tracker.topics.values():
            frame = tk.Frame(self.topic_list_frame)
            frame.pack(fill="x", pady=2)

            tk.Label(frame, text=f"{topic.name} (Difficulty {topic.difficulty})", width=20, anchor="w").pack(side="left", padx=5)
            progress = ttk.Progressbar(frame, length=300, maximum=100)
            progress['value'] = topic.mastery
            progress.pack(side="left", padx=5)
            tk.Label(frame, text=f"{topic.mastery:.0f}%", width=5).pack(side="left", padx=5)

    def add_topic_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add Topic")
        popup.geometry("250x120")
        tk.Label(popup, text="Topic Name:").pack(pady=5)
        name_entry = tk.Entry(popup)
        name_entry.pack()

        tk.Label(popup, text="Difficulty (1-5):").pack(pady=5)
        diff_entry = tk.Entry(popup)
        diff_entry.pack()

        def add_topic():
            try:
                name = name_entry.get().strip()
                difficulty = int(diff_entry.get())
                if name == "" or not 1 <= difficulty <= 5:
                    raise ValueError
                topic = Topic(name, difficulty)
                tracker.add_topic(topic)
                self.refresh_topics()
                popup.destroy()
            except:
                messagebox.showerror("Error", "Invalid input. Difficulty must be 1-5.")

        tk.Button(popup, text="Add", command=add_topic).pack(pady=10)

    def log_session_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Log Session")
        popup.geometry("250x120")

        tk.Label(popup, text="Select Topic:").pack(pady=5)
        topic_var = tk.StringVar()
        topic_menu = ttk.Combobox(popup, textvariable=topic_var, values=list(tracker.topics.keys()))
        topic_menu.pack()

        tk.Label(popup, text="Minutes Studied:").pack(pady=5)
        duration_entry = tk.Entry(popup)
        duration_entry.pack()

        def log_session():
            try:
                topic_name = topic_var.get()
                minutes = int(duration_entry.get())
                if topic_name not in tracker.topics or minutes <= 0:
                    raise ValueError
                session = StudySession(topic_name, minutes)
                tracker.log_session(session)
                sessions_data.append(session)
                self.refresh_topics()
                popup.destroy()
            except:
                messagebox.showerror("Error", "Invalid input.")

        tk.Button(popup, text="Log", command=log_session).pack(pady=10)

    def recommend_topic(self):
        recommender = Recommender(list(tracker.topics.values()))
        topic = recommender.recommend()
        if topic:
            messagebox.showinfo("Recommendation", f"Next topic to study: {topic.name}")
        else:
            messagebox.showinfo("Recommendation", "No topics available.")

    def save_and_exit(self):
        store.save(list(tracker.topics.values()), sessions_data)
        self.destroy()


if __name__ == "__main__":
    app = StudyForgeGUI()
    app.mainloop()
