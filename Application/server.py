import os

from flask import Flask, render_template, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv
from os import getenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = Flask(__name__, instance_relative_config=True)
db_path = os.path.join(app.instance_path, 'poll.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = getenv('FLASK_SECRET_KEY')

db = SQLAlchemy(app)

member_names = ["Janaija Norton", "Jessica Witt", "Joshua Morris", "Mr. Cofield", "Mrs. B", "Shakerria Dorsey",
                "Shayne Carey", "Tatyana Adei Flowers", "Stewart Carey", "Austin Green", "Alex Aviles",
                "Benson", "Ciara Gonzalez", "Dominique", "Dr. Washington", "Toya Miller", "Yusuf Aminah",
                "Katlyn Witt", "Maury Moody"
                ]


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    options = db.relationship('PollOption', backref='poll', lazy=True)


class PollOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    votes = db.Column(db.Integer, default=0)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)


@app.route('/')
def index():
    voted_polls = session.get('voted_polls', [])
    all_polls = Poll.query.all()

    for poll in all_polls:
        total_votes = sum(option.votes for option in poll.options) or 1
        for option in poll.options:
            option.percent = round((option.votes / total_votes) * 100)

    return render_template("poll.html", polls=all_polls, voted_polls=voted_polls)


@app.route('/vote/<int:poll_id>', methods=['POST'])
def vote(poll_id):
    option_id = request.form.get('option')
    option = db.session.get(PollOption, option_id)

    if option and option.poll_id == poll_id:
        option.votes += 1
        db.session.commit()

        voted_polls = session.get('voted_polls', [])
        voted_polls.append(poll_id)
        session['voted_polls'] = voted_polls

        return jsonify({'message': 'Vote recorded successfully.'})

    return jsonify({'error': 'Invalid vote'}), 400

@app.route("/debug/polls")
def debug_polls():
    polls = Poll.query.all()
    data = []
    for poll in polls:
        data.append({
            "question": poll.question,
            "options": [
                {"name": o.name, "votes": o.votes}
                for o in poll.options
            ]
        })
    return jsonify(data)

def create_poll(question: str, options: list[str]):
    poll = Poll(question=question)
    db.session.add(poll)
    db.session.flush()
    poll_options = [PollOption(name=option, poll_id=poll.id) for option in options]
    db.session.add_all(poll_options)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Poll.query.first():
            questions = [
                "Most Inspirational?", "Best Mentor?", "Most Supportive", "Most Creative Lesson Plans", "Most Patient",
                "Most Innovative", "Most Dedicated", "Most Organized", "Most Positive Attitude",
                "Most Student Centered", "The Early Bird", "Coffee's Best Friend", "The Office Clown",
                "The Chit Chat Award", "The Busy Bee", "The Food Order Master", "The Super Snacker",
                "The Walking Toolbox", "Thinks In Emoji", "Peace Maker", "Five More Minutes", "Always In A Meeting",
                "The Fire Extinguisher"
            ]

            for q in questions:
                create_poll(q, member_names)

            db.session.commit()

    app.run(debug=True)
