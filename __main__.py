#!/usr/bin/env python3

import tkinter # pip install tk
from tkinter import messagebox
import webbrowser
import random
from question import Question
from playsound import playsound  # pip install playsound
import os

class QuizGUI:
    def __init__(self, root, questions: list):
        self.root = root
        self.questions = questions.copy()
        random.shuffle(self.questions)
        self.index = 0
        self.selected_choice = tk.StringVar()
        self.setup_gui()

    def play_sound(self, sound_type):
        sound_folder = os.path.join(os.path.dirname(__file__), "sounds")
        if sound_type == "correct":
            sound_path = os.path.join(sound_folder, "correct.mp3")
        elif sound_type == "incorrect":
            sound_path = os.path.join(sound_folder, "incorrect.mp3")
        else:
            return
        if os.path.isfile(sound_path):
            try:
                playsound(sound_path, block=False)
            except Exception as e:
                print(f"Could not play sound: {e}")

    def open_video(self):
        webbrowser.open(self.questions[self.index].video_link)

    def check_answer(self):
        selected = self.selected_choice.get()
        if not selected:
            messagebox.showinfo("Oops!", "Please choose an answer!")
            return
        correct = self.questions[self.index].correct_answer
        if selected == correct:
            self.play_sound("correct")
            messagebox.showinfo("🎉 Hooray!", "Correct! 🏆")
        else:
            self.play_sound("incorrect")
            messagebox.showinfo("😮 Your Answer Isn't Correct, Try Again!")
        self.next_question()

    def next_question(self):
        self.index += 1
        if self.index < len(self.questions):
            self.show_question()
        else:
            messagebox.showinfo("🎊 Finished!", "You have completed all the questions! 🌟")
            self.root.quit()

    def show_question(self):
        q = self.questions[self.index]
        self.selected_choice.set("")
        self.question_lbl.config(text=q.question_text)
        for i, choice in enumerate(q.answer_choices):
            self.radio_buttons[i].config(text=choice, value=choice, state=tk.NORMAL)
            self.radio_buttons[i].pack(anchor="w", padx=40, pady=15)
        for i in range(len(q.answer_choices), 4):
            self.radio_buttons[i].pack_forget()

    def setup_gui(self):
        self.root.title("RIGHT OR WRONG Time!")
        self.root.geometry("820x500")
        self.root.configure(bg="#ffd6fc")  # Soft pink background

        # Title Banner
        title = tk.Label(self.root, text="Welcome to Right or Wrong!", font=("Comic Sans MS", 28, "bold"),
                         bg="#ffd6fc", fg="#1e90ff")
        title.pack(pady=20)

        # Left panel for video
        left_frame = tk.Frame(self.root, width=410, height=400, bg="#a7e9f7")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        left_frame.pack_propagate(False)

        video_label = tk.Label(left_frame, text="Watch the Video!", font=("Comic Sans MS", 18, "bold"), bg="#a7e9f7", fg="#ff69b4")
        video_label.pack(pady=10)

        open_video_btn = tk.Button(
            left_frame,
            text="CLICK TO WATCH!",
            command=self.open_video,
            font=("Comic Sans MS", 20, "bold"),
            bg="#ffe066",
            fg="#ff1493",
            activebackground="#fffacd",
            activeforeground="#1e90ff",
            relief="raised",
            bd=8,
            padx=15,
            pady=15
        )
        open_video_btn.pack(pady=30)

        # Right panel for question
        right_frame = tk.Frame(self.root, width=410, height=400, bg="#afffc7")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)

        self.question_lbl = tk.Label(right_frame, text="", wraplength=350, font=("Comic Sans MS", 20, "bold"),
                                    bg="#afffc7", fg="#ff4500")
        self.question_lbl.pack(pady=30)

        self.radio_buttons = []
        for _ in range(4):
            rb = tk.Radiobutton(
                right_frame,
                text="",
                variable=self.selected_choice,
                value="",
                font=("Comic Sans MS", 18, "bold"),
                bg="#afffc7",
                fg="#1e90ff",
                selectcolor="#ffe066",
                indicatoron=False,
                width=20,
                height=2,
                pady=10,
                bd=5,
                relief="groove"
            )
            self.radio_buttons.append(rb)
            rb.pack(anchor="w", padx=40, pady=15)

        submit_btn = tk.Button(
            right_frame,
            text="Submit Answer!",
            command=self.check_answer,
            font=("Comic Sans MS", 20, "bold"),
            bg="#ffe066",
            fg="#ff1493",
            activebackground="#fffacd",
            activeforeground="#1e90ff",
            relief="raised",
            bd=8,
            padx=15,
            pady=15
        )
        submit_btn.pack(pady=30)

        self.show_question()

if __name__ == "__main__":
    questions = []
    root.mainloop()
