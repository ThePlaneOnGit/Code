import os
import datetime

class QuizLogger:
    def __init__(self, username):
        self.username = username
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_path = os.path.join(self.log_dir, f"{self.username}_log.txt")

    def log_wrong_answer(self, question_text, selected, correct):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(
                f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Wrong: {question_text} (Answered: {selected} | Correct: {correct})\n"
            )

    def log_summary(self, total, correct_count):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(
                f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Quiz Finished - {correct_count}/{total} correct.\n\n"
            )
