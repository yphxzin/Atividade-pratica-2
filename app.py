"""API e interface web. Uso: python app.py -> http://127.0.0.1:5000"""
import json
import os
import traceback

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

from config import DADOS, MODELOS, PROBLEMAS

def preparar_modelos():
    # Gera dados caso ainda não existam.
    if not all((DADOS / p["arquivo"]).exists() for p in PROBLEMAS.values()):
        import gerar_dados
        gerar_dados.main()

    # Re-treina se algum modelo ou metricas estiver faltando.
    faltando = (
        not (MODELOS / "metricas.json").exists()
        or any(not (MODELOS / f"{nome}.joblib").exists() for nome in PROBLEMAS)
    )
    if faltando:
        import treinar
        treinar.main()

preparar_modelos()

METRICAS = json.loads(
    (MODELOS / "metricas.json").read_text(encoding="utf-8")
)
MODELOS_CARREGADOS = {
    nome: joblib.load(MODELOS / f"{nome}.joblib")
    for nome in PROBLEMAS
}

app = Flask(__name__)
app.json.ensure_ascii = False
app.json.sort_keys = False

def validar(problema, dados):
    linha, erros = {}, []

    for campo, regra in problema["features"].items():
        valor = dados.get(campo)

        if valor in (None, ""):
            linha[campo] = None
            continue

        if regra["tipo"] == "categoria":
            if valor not in regra["opcoes"]:
                erros.append(
                    f"{campo} deve ser um de: {', '.join(regra['opcoes'])}"
                )
            linha[campo] = valor
            continue

        try:
            numero = float(valor)
            if not regra["min"] <= numero <= regra["max"]:
                erros.append(
                    f"{campo} deve estar entre {regra['min']} e {regra['max']}"
                )
            linha[campo] = numero
        except (TypeError, ValueError):
            erros.append(f"{campo} deve ser numérico")

    return linha, erros

@app.get("/")
def pagina():
    return render_template("index.html")

@app.get("/api/problemas")
def problemas():
    return jsonify({
        nome: {**problema, "metricas": METRICAS[nome]}
        for nome, problema in PROBLEMAS.items()
    })

@app.post("/api/prever/<nome>")
def prever(nome):
    try:
        if nome not in PROBLEMAS:
            return jsonify(erro="Problema não encontrado"), 404

        problema = PROBLEMAS[nome]
        linha, erros = validar(
            problema, request.get_json(silent=True) or {}
        )

        if erros:
            return jsonify(erro="; ".join(erros)), 400

        X = pd.DataFrame(
            [linha], columns=list(problema["features"])
        )

        # Converte apenas as colunas numéricas.
        for campo, regra in problema["features"].items():
            if regra["tipo"] == "numero":
                X[campo] = pd.to_numeric(X[campo], errors="coerce")

        modelo = MODELOS_CARREGADOS[nome]

        if problema["tipo"] == "classificacao":
            prob = float(modelo.predict_proba(X)[0, 1])
            return jsonify(probabilidade=prob)

        valor = float(modelo.predict(X)[0])
        return jsonify(valor=valor)

    except Exception as exc:
        traceback.print_exc()
        return jsonify(
            erro=f"Erro interno ao gerar previsão: {type(exc).__name__}: {exc}"
        ), 500

@app.get("/api/saude")
def saude():
    return jsonify(status="ok", problemas=list(PROBLEMAS))

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
