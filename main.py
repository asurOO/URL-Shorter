import os, string, random
from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(8), unique=True)
    original = db.Column(db.String(500))

def gen_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.before_first_request
def init():
    db.create_all()

@app.route('/shorten', methods=['POST'])
def shorten():
    original = request.json.get('url')
    code = gen_code()
    while URL.query.filter_by(short=code).first():
        code = gen_code()
    rec = URL(short=code, original=original)
    db.session.add(rec)
    db.session.commit()
    return {"short_url": f"{os.getenv('BASE_URL')}/{code}"}, 200

@app.route('/<code>')
def redirecter(code):
    rec = URL.query.filter_by(short=code).first_or_404()
    return redirect(rec.original)
