from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db = SQLAlchemy(app)

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(200), nullable=False)
    aluno = db.relationship('Aluno', backref='curso')

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(200), nullable=False)
    data_nasc = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    escolaridade = db.Column(db.String(200), nullable=False)
    login = db.Column(db.String(200), nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    alunos = Aluno.query.all()
    return render_template("index.html", alunos=alunos)

@app.route("/adicionar", methods = ["GET", "POST"])
def adicionar():
    if request.method == "POST":
        curso = Curso(nome = request.form["curso"])
        db.session.add(curso)
        db.session.commit()

        aluno = Aluno(
            nome = request.form["nome"],
            data_nasc = request.form["data_nasc"],
            endereco = request.form["endereco"],
            escolaridade = request.form["escolaridade"],
            login = request.form["login"],
            senha = request.form["senha"],
            curso_id = curso.id
        )
        db.session.add(aluno)
        db.session.commit()
        
        return redirect("/")
    return render_template("adicionar.html")

if __name__ == "__main__":
    app.run(debug=True)