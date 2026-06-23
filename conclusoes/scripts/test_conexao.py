import mysql.connector
from mysql.connector import Error

def testar_conexao(porta):
    print(f"--- Testando porta {porta} ---")
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            port=porta,
            user='root',
            password='kwanza2024'
        )
        if conn.is_connected():
            print(f"Sucesso: Conectado à porta {porta}")
            conn.close()
    except Error as e:
        print(f"Erro na porta {porta}: {e}")
    print("-" * 25)

if __name__ == "__main__":
    testar_conexao(3307)
    testar_conexao(3308)
