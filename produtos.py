from multiprocessing.connection import Connection
from database import conectar

def cadastrar_produtos():
    nome = str(input('nome do produto: '))
    preco = float(input(' preço do produto em R$: '))
    quantidade = int(input('quantidade: '))
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)', (nome, preco, quantidade))
    conn.commit()
    conn.close()
    print("✅ Produto cadastrado!")
  

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    for p in produtos:
        print(f"{p[0]} - {p[1]} - R${p[2]:.2f} - {p[3]} unidades")

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    for p in produtos:
        print(f"{p[0]} - {p[1]} - R${p[2]:.2f} - {p[3]} unidades")

def excluir_produto():  
    listar_produtos()
    id_prod = int(input("ID do produto a excluir: "))
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = ?', (id_prod,))
    conn.commit()
    conn.close()
    print("✅ Produto removido!")




