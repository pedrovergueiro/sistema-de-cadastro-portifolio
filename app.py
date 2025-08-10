import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Criar tabela se não existir
def init_db():
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Funções para manipular o banco
def listar_produtos():
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, valor, quantidade FROM produtos")
    dados = cursor.fetchall()
    conn.close()
    return [{"nome": nome, "valor": valor, "quantidade": quantidade} for nome, valor, quantidade in dados]

def adicionar_produto(nome, valor, quantidade):
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, valor, quantidade) VALUES (?, ?, ?)", (nome, valor, quantidade))
    conn.commit()
    conn.close()

def excluir_produto(nome):
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE nome = ?", (nome,))
    conn.commit()
    conn.close()

# HTML do site
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
        h1, h2, h3 {
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
        <input type="number" name="quantidade" placeholder="Quantidade" required min="1">
        <button type="submit">Cadastrar</button>
    </form>

    <h2>Produtos Cadastrados:</h2>
    <ul>
        {% for p in produtos %}
            <li>
                {{ p['nome'] }} - R$ {{ "%.2f"|format(p['valor']) }} - Quantidade: {{ p['quantidade'] }} - Total: R$ {{ "%.2f"|format(p['valor'] * p['quantidade']) }}
                <form method="POST" action="/excluir" style="margin-left: 10px;">
                    <input type="hidden" name="nome" value="{{ p['nome'] }}">
                    <button type="submit">Excluir</button>
                </form>
            </li>
        {% endfor %}
    </ul>

    <h3>Valor total do estoque: R$ {{ "%.2f"|format(total_estoque) }}</h3>
</body>
</html>
"""

@app.route("/")
def index():
    produtos = listar_produtos()
    total_estoque = sum(p["valor"] * p["quantidade"] for p in produtos)
    return render_template_string(HTML_TEMPLATE, produtos=produtos, total_estoque=total_estoque)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"]
    valor = float(request.form["valor"])
    quantidade = int(request.form["quantidade"])
    adicionar_produto(nome, valor, quantidade)
    return redirect("/")

@app.route("/excluir", methods=["POST"])
def excluir():
    nome = request.form["nome"]
    excluir_produto(nome)
    return redirect("/")

if __name__ == "__main__":
    init_db()  # cria o banco/tabela se não existir
    app.run(debug=True)