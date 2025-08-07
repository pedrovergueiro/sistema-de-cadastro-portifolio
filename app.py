from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Lista para armazenar os produtos
produtos = []

# HTML com CSS embutido
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sistema de Cadastro de Produtos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f7fa;
            margin: 40px;
            color: #333;
        }
        h1, h2 {
            color: #2c3e50;
        }
        form {
            margin-bottom: 20px;
        }
        input[type="text"], input[type="number"] {
            padding: 8px;
            margin-right: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            width: 200px;
            box-sizing: border-box;
        }
        button {
            padding: 8px 16px;
            background-color: #3498db;
            border: none;
            color: white;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #2980b9;
        }
        ul {
            list-style-type: none;
            padding-left: 0;
        }
        li {
            background: white;
            margin-bottom: 10px;
            padding: 12px 15px;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgb(0 0 0 / 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        li form {
            margin: 0;
        }
        li button {
            background-color: #e74c3c;
            padding: 6px 12px;
        }
        li button:hover {
            background-color: #c0392b;
        }
    </style>
</head>
<body>
    <h1>Cadastro de Produtos</h1>
    
    <form method="POST" action="/cadastrar">
        <input type="text" name="nome" placeholder="Nome do produto" required>
        <input type="number" step="0.01" name="valor" placeholder="Valor do produto (R$)" required>
        <button type="submit">Cadastrar</button>
    </form>

    <h2>Produtos Cadastrados:</h2>
    <ul>
        {% for p in produtos %}
            <li>
                {{ p['nome'] }} - R$ {{ "%.2f"|format(p['valor']) }}
                <form method="POST" action="/excluir" style="margin-left: 10px;">
                    <input type="hidden" name="nome" value="{{ p['nome'] }}">
                    <button type="submit">Excluir</button>
                </form>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, produtos=produtos)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"]
    valor = float(request.form["valor"])
    produtos.append({"nome": nome, "valor": valor})
    return redirect("/")

@app.route("/excluir", methods=["POST"])
def excluir():
    nome = request.form["nome"]
    global produtos
    produtos = [p for p in produtos if p["nome"] != nome]
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
