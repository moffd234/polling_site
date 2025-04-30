from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poll.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap5(app)
db = SQLAlchemy(app)


class PollOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    votes = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    poll_data = PollOption.query.all()
    total_votes = sum(option.votes for option in poll_data) or 1  # Avoid divide by zero
    # Calculate percentages
    for option in poll_data:
        option.percent = round((option.votes / total_votes) * 100)
    return render_template("poll.html", poll_data=poll_data)

@app.route('/vote', methods=['POST'])
def vote():
    option_id = request.form.get('option')
    option = PollOption.query.get(option_id)
    if option:
        option.votes += 1
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not PollOption.query.first():
            options = ["Option A", "Option B", "Option C", "Option D", "Option E"]
            for opt in options:
                db.session.add(PollOption(name=opt))
            db.session.commit()

    app.run(debug=True)

