from flask import Flask, render_template, url_for, redirect, request, session


app = Flask(__name__)
app.secret_key = "ajakhflkqhfa"

infos = {"322.167.975-22": "Nome: Ana Luchsinger ---- Analise Pessoal: Fundadora da empresa Digifun, nenhum caso arquivado contra. ",
         "875.133.988-11": "Nome: Leandro Beckman ---- Analise Pessoal: Fundador da empresa NeuroPlay foi indiciado por Ocultação de Cadaver, Ossos foram encontrados em sua Mala.",
         "877.552.132-05": "Nome: Robert Pattinson ---- Analise Pessoal: Fundador da empresa DigiFun, Indiciado por ocultação de patrimonio, mas o caso não foi para frente."
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
    return render_template("casoDigifun.html")

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


if __name__ == "__main__":
    app.run(debug=True)