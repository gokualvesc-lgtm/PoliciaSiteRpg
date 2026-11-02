from flask import Flask, render_template, url_for, redirect, request, session

app = Flask(__name__)
app.secret_key = "ajakhflkqhfa"

import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(DATABASE_URL)

infos = {"322.167.975-22": "Nome: Ana Luchsinger ---- Analise Pessoal: Fundadora da empresa Digifun, nenhum caso arquivado contra.  Estado Atual: Desaparecida",
         "875.133.988-11": "Nome: Leandro Beckman ---- Analise Pessoal: Fundador da empresa NeuroPlay foi indiciado por Ocultação de Cadaver, Ossos foram encontrados em sua Mala. Estado Atual: Morto",
         "877.552.132-05": "Nome: Robert Pattinson ---- Analise Pessoal: Fundador da empresa DigiFun, Indiciado por ocultação de patrimonio, mas o caso não foi para frente. Estado atual: Desaparecido",
         "066.241.555-67": "Nome: Klever Dawne ---- Analise Pessoal: Antigo Funcionario da Empresa DigiFun, Cursou faculdade em Ciência, Biologia Humana. Nenhum caso Arquivado contra. Data de Nascimento: 09/12/1988 Estado Atual: Vivo."

         }


usuarios = {"255.112.521": "2551",
            "875.661.269": "8756",
            "650.120.508": "6501",
            "878.812.472": "8788",
            "524.122.411": "5241",
            "009.121.555": "0091"
            }

@app.route("/")
def main():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("matricula")
        password = request.form.get("senha")

        try:
            if not usuarios[username]:
                return render_template("login.html")
        except:
            return render_template("login.html")
        if usuarios[username] == password:
            return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/casos")
def casos():
    return render_template("casos.html")

@app.route("/caso-digifun")
def caso_digifun():
    return render_template("casoDigifunAtt.html")

@app.route("/investigacao-pessoal", methods=["POST", "GET"])
def investigacao():

    if request.method == "POST":
        cpf = request.form.get("cpf")

        try:
            if not infos[cpf]:
                return render_template("investigacao.html")
        except:
            return render_template("investigacao.html")

        consulta = infos[cpf]

        return render_template("investigacao.html", consulta=consulta)



    return render_template("investigacao.html", consulta="Nada Consultado!")



@app.route("/anotacoes", methods=["POST", "GET"])
def anotacoes():

    conn = conectar()
    cursor = conn.cursor()

    try:
        if request.method == "POST":

            title = request.form.get("title")
            category = request.form.get("Categoria")
            caso = request.form.get("Caso")
            priority = request.form.get("priority")
            anotacao = request.form.get("anotacao")

            cursor.execute("""
                INSERT INTO "Anotacoes"
                ("Title", "Category", "CasoNumber", "Priority", "Anotacao")
                VALUES (%s, %s, %s, %s, %s)
            """, (title, category, caso, priority, anotacao))

            conn.commit()

        cursor.execute("""
            SELECT "id", "Title", "Category", "CasoNumber",
                   "Priority", "Anotacao"
            FROM "Anotacoes"
            ORDER BY "id" DESC
        """)

        anotacoes = cursor.fetchall()

        return render_template(
            "anotacoes.html",
            anotacoes=anotacoes
        )

    except Exception as e:
        conn.rollback()
        print("ERRO:", repr(e))
        raise

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)
