from flask import Flask, render_template, request, redirect, url_for, session, flash
from account import AccountManager
from logger import QuizLogger
from question import Question
import random, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Example questions
QUESTIONS = [
        Question("/static/images/1.png", "What Did the Child Do Wrong?", ["Throw the Trash in the Bin", "Put the Trash in His Pocket", "Put the Trash on the Ground"], "Put the Trash on the Ground"),
    Question("/static/images/2.png", "What did the child do wrong", ["Leave the faucet on while entering", "Leave the faucet on while leaving", "Use the faucet"], "Blue"),
]

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('quiz'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    am = AccountManager()
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        ok, msg = am.login(username, password)
        if ok:
            session['username'] = username
            flash(msg, 'success')
            return redirect(url_for('quiz'))
        flash(msg, 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    am = AccountManager()
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        ok, msg = am.register(username, password)
        if ok:
            session['username'] = username
            flash(msg, 'success')
            return redirect(url_for('quiz'))
        flash(msg, 'danger')
    return render_template('register.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    if 'index' not in session:
        session['index'] = 0
        session['correct_count'] = 0
        random.shuffle(QUESTIONS)

    index = session['index']

    if request.method == 'POST':
        selected = request.form.get('choice')
        q = QUESTIONS[index]
        logger = QuizLogger(username)
        if selected == q.correct_answer:
            session['correct_count'] += 1
        else:
            logger.log_wrong_answer(q.question_text, selected, q.correct_answer)

        session['index'] += 1
        if session['index'] >= len(QUESTIONS):
            logger.log_summary(len(QUESTIONS), session['correct_count'])
            return redirect(url_for('result'))

        return redirect(url_for('quiz'))

    q = QUESTIONS[index]
    return render_template('quiz.html', q=q, index=index + 1, total=len(QUESTIONS))

@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('login'))
    score = session.get('correct_count', 0)
    total = len(QUESTIONS)
    username = session['username']
    session.clear()
    return render_template('result.html', score=score, total=total, username=username)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
