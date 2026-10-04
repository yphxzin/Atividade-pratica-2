Participantes da atividade 2: Pedro Henrique Marques
# Laboratório de ML Supervisionado — versão corrigida

Este pacote mantém os dois problemas originais (**churn** e **imóveis**) e adiciona o terceiro problema pedido no exercício: **risco de crédito**.

## Correção do botão "Prever"

Nesta versão, o JavaScript:
- mostra "Calculando..." enquanto espera a API;
- captura erros de rede e erros HTTP;
- mostra no cartão **Previsão** a mensagem retornada pelo Flask;
- não fica silencioso quando a API responde com erro;
- usa exatamente o endpoint `/api/prever/<nome>` esperado pelo `app.py`.

O `app.py` também captura exceções e devolve o erro em JSON, além de imprimir o traceback no terminal.

## Como executar no Windows

No terminal, dentro da pasta do projeto:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python gerar_dados.py
python treinar.py
python app.py
```

Depois abra:

```text
http://127.0.0.1:5000
```

**Não abra `templates/index.html` diretamente** e não use Live Server para esta aplicação. O HTML precisa ser servido pelo Flask para conseguir acessar `/api/problemas` e `/api/prever/...`.

## Teste rápido

Com o servidor rodando, abra no navegador:

```text
http://127.0.0.1:5000/api/saude
```

A resposta deve ser parecida com:

```json
{"status":"ok","problemas":["churn","imoveis","credito"]}
```

## Estrutura

```text
laboratorio_ml_corrigido/
├── app.py
├── config.py
├── gerar_dados.py
├── treinar.py
├── requirements.txt
├── data/
├── models/
└── templates/
    └── index.html
```

## Observação

Na primeira execução, se os CSVs ou modelos estiverem ausentes, `app.py` tenta gerar os dados e treinar automaticamente. Mesmo assim, para acompanhar possíveis erros com clareza, recomenda-se rodar primeiro `python gerar_dados.py` e depois `python treinar.py`.
