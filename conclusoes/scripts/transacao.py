import mysql.connector

def conectar(porta):
    return mysql.connector.connect(
        host='127.0.0.1',
        port=porta,
        user='root',
        password='kwanza2024',
        database='mercadokwanza',
        autocommit=False,
        use_pure=True
    )

# ==========================
# CONFIGURAÇÃO
# ==========================
PRODUTO_ID = 5
LOJA_BENGUELA = 6
LOJA_LUANDA = 1
CLIENT_ID = 42
QUANTIDADE = 10

# ⚠️ ajusta conforme o teu docker-compose
no_luanda = conectar(3307)
no_benguela = conectar(3308)

cur_l = no_luanda.cursor()
cur_b = no_benguela.cursor()

try:
    # ==========================
    # STOCK INICIAL
    # ==========================
    cur_b.execute(
        """
        SELECT quantidade
        FROM STOCK
        WHERE produto_id=%s AND loja_id=%s
        FOR UPDATE
        """,
        (PRODUTO_ID, LOJA_BENGUELA)
    )

    resultado = cur_b.fetchone()

    if resultado is None:
        raise Exception("Produto não existe no stock de Benguela")

    stock_inicial = resultado[0]
    print(f"Stock inicial em Benguela: {stock_inicial}")

    # ==========================
    # VALIDAR STOCK
    # ==========================
    if stock_inicial < QUANTIDADE:
        raise Exception(f"Stock insuficiente: {stock_inicial}")

    # ==========================
    # VER VENDAS INICIAIS EM LUANDA
    # ==========================
    cur_l.execute(
        "SELECT COUNT(*) FROM VENDA WHERE loja_id=%s",
        (LOJA_LUANDA,)
    )

    vendas_iniciais = cur_l.fetchone()[0]
    print(f"Vendas iniciais em Luanda: {vendas_iniciais}")

    # ==========================
    # UPDATE STOCK BENGUELA
    # ==========================
    cur_b.execute(
        """
        UPDATE STOCK
        SET quantidade = quantidade - %s
        WHERE produto_id=%s AND loja_id=%s
        """,
        (QUANTIDADE, PRODUTO_ID, LOJA_BENGUELA)
    )

    print(f"[Benguela] Stock decrementado: -{QUANTIDADE}")

    # ==========================
    # INSERT VENDA LUANDA
    # ==========================
    cur_l.execute(
        """
        INSERT INTO VENDA
        (loja_id, cliente_id, data_venda, total)
        VALUES (%s, %s, NOW(), %s)
        """,
        (LOJA_LUANDA, CLIENT_ID, QUANTIDADE * 1500)
    )

    venda_id = cur_l.lastrowid

    cur_l.execute(
        #'INSERT INTO ITEM_VENDA',
        (venda_id, produto_id, qtd, preco_unit, desconto),
        'VALUES (%s, %s, %s, %s, %s)',
        (venda_id, PRODUTO_ID, QUANTIDADE, 1500, 0.0)
    )

    print(f"[Luanda] Venda registada: {venda_id}")

    # ==========================
    # COMMIT
    # ==========================
    no_benguela.commit()
    no_luanda.commit()

    print("Transação concluída com sucesso")

    # ==========================
    # ESTADO FINAL
    # ==========================
    cur_b.execute(
        """
        SELECT quantidade
        FROM STOCK
        WHERE produto_id=%s AND loja_id=%s
        """,
        (PRODUTO_ID, LOJA_BENGUELA)
    )

    stock_final = cur_b.fetchone()[0]

    cur_l.execute(
        "SELECT COUNT(*) FROM VENDA WHERE loja_id=%s",
        (LOJA_LUANDA,)
    )

    vendas_finais = cur_l.fetchone()[0]

    print(f"Stock final em Benguela: {stock_final}")
    print(f"Vendas finais em Luanda: {vendas_finais}")

except Exception as e:
    # ==========================
    # ROLLBACK
    # ==========================
    no_benguela.rollback()
    no_luanda.rollback()

    print("ROLLBACK efectuado em ambos os nós")
    print(f"Motivo: {e}")

    # ==========================
    # VERIFICAÇÃO APÓS ROLLBACK
    # ==========================
    cur_b.execute(
        """
        SELECT quantidade
        FROM STOCK
        WHERE produto_id=%s AND loja_id=%s
        """,
        (PRODUTO_ID, LOJA_BENGUELA)
    )

    stock_rollback = cur_b.fetchone()[0]

    cur_l.execute(
        "SELECT COUNT(*) FROM VENDA WHERE loja_id=%s",
        (LOJA_LUANDA,)
    )

    vendas_rollback = cur_l.fetchone()[0]
        
    print(f"Stock após ROLLBACK: {stock_rollback}")
    print(f"Vendas após ROLLBACK: {vendas_rollback}")

finally:
    cur_l.close()
    cur_b.close()
    no_luanda.close()
    no_benguela.close()