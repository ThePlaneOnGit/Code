from typing import List

class Question:
    def __init__(self, video_link: str, question_text: str, answer_choices: List[str], correct_answer: str):
        if len(answer_choices) < 3 or len(answer_choices) > 4:
            raise ValueError("Answer choices must be 3 or 4.")
        if correct_answer not in answer_choices:
            raise ValueError("Correct answer must be one of the answer choices.")
        self.video_link = video_link
        self.question_text = question_text
        self.answer_choices = answer_choices
        self.correct_answer = correct_answer
