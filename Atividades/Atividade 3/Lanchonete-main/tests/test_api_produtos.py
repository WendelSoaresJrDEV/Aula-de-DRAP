def test_produto_alteracao_valor(client):
    
    r = client.post("/produtos", json={"codigo": 1, "valor": 5, "tipo": 1})
    assert r.status_code == 200
    codigo = r.json()["codigo"]

    r2 = client.put(f"/produtos/{codigo}/valor", json={"novo_valor": 6.5})
    assert r2.status_code == 200
    assert r2.json()["alterou"] == True