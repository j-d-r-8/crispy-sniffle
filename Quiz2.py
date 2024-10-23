import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import random

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Game")
        self.questions = self.load_questions('questions.json')
        self.leaderboard = self.load_leaderboard('leaderboard.json')
        self.score = 0
        self.question_index = 0
        self.create_main_menu()

    def load_questions(self, filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    def load_leaderboard(self, filepath):
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_leaderboard(self, filepath):
        with open(filepath, 'w') as file:
            json.dump(self.leaderboard, file, indent=4)

    def create_main_menu(self):
        self.main_menu_frame = tk.Frame(self.master)
        self.main_menu_frame.pack(pady=50)
        tk.Label(self.main_menu_frame, text="Quiz Game", font=("Arial", 24)).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Start Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self.main_menu_frame, text="View Leaderboard", command=self.view_leaderboard).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Exit", command=self.master.quit).pack(pady=10)

    def start_quiz(self):
        self.main_menu_frame.pack_forget()
        random.shuffle(self.questions)
        self.create_quiz_widgets()
        self.display_question()

    def create_quiz_widgets(self):
        self.question_label = tk.Label(self.master, text="", wraplength=400, justify="left")
        self.question_label.pack(pady=20)
        self.difficulty_label = tk.Label(self.master, text="")
        self.difficulty_label.pack()
        self.options_frame = tk.Frame(self.master)
        self.options_frame.pack()
        self.score_label = tk.Label(self.master, text=f"Score: {self.score}")
        self.score_label.pack()
        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_answer)
        self.submit_button.pack(pady=20)

    def display_question(self):
        if self.question_index < len(self.questions):
            question_data = self.questions[self.question_index]
            self.question_label.config(text=f"Q{self.question_index + 1}: {question_data['question']}")
            self.difficulty_label.config(text=f"Difficulty: {question_data['difficulty']}")
            for widget in self.options_frame.winfo_children():
                widget.destroy()
            self.selected_option = tk.StringVar()
            self.selected_option.set(None)  # Explicitly set to None
            for option in question_data['options']:
                rb = tk.Radiobutton(self.options_frame, text=option, variable=self.selected_option, value=option)
                rb.pack(anchor='w')
        else:
            messagebox.showinfo("Quiz Complete", "You have completed the quiz!")
            self.view_leaderboard()

    def check_answer(self):
        selected = self.selected_option.get()
        correct_answer = self.questions[self.question_index]['answer']
        if selected == correct_answer:
            self.score += self.get_points(self.questions[self.question_index]['difficulty'])
            response = "Correct"
        else:
            response = "Incorrect"
        messagebox.showinfo(response, f"That's the {response.lower()} answer!")
        self.score_label.config(text=f"Score: {self.score}")
        if self.question_index == len(self.questions) - 1:
            self.handle_quiz_completion()
        else:
            self.question_index += 1
            self.master.after(1000, self.display_question)

    def handle_quiz_completion(self):
        user_name = simpledialog.askstring("Quiz Complete", "Enter your name for the leaderboard:")
        if user_name:
            self.leaderboard.append({'name': user_name, 'score': self.score})
            self.save_leaderboard('leaderboard.json')
        messagebox.showinfo("Quiz Complete", f"Congratulations, {user_name}! You have completed the quiz with a score of {self.score}.")
        self.view_leaderboard()

    def get_points(self, difficulty):
        return {'easy': 1, 'medium': 2, 'hard': 3}.get(difficulty, 0)

    def view_leaderboard(self):
        self.main_menu_frame.pack_forget()
        leaderboard_frame = tk.Frame(self.master)
        leaderboard_frame.pack(pady=50)
        tk.Label(leaderboard_frame, text="Leaderboard", font=("Arial", 24)).pack(pady=10)
        for entry in sorted(self.leaderboard, key=lambda x: x['score'], reverse=True):
            tk.Label(leaderboard_frame, text=f"{entry['name']} - {entry['score']}").pack()
        tk.Button(leaderboard_frame, text="Back to Menu", command=lambda: self.switch_frame(leaderboard_frame)).pack(pady=10)

    def switch_frame(self, old_frame):
        old_frame.pack_forget()
        self.create_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
