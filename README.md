# Atividade Prática 2 — Aprendizado de Máquina Supervisionado

## Participante

- Pedro Henrique Marques

## Objetivo

Este projeto foi desenvolvido para a disciplina de Aprendizado de Máquina Supervisionado.

O objetivo é construir um modelo capaz de estimar a **probabilidade de inadimplência de pedidos de empréstimo**, apoiando a tomada de decisão de uma equipe de crédito.

O projeto também mantém os exemplos de:

- Churn de clientes
- Preço de imóveis
- Risco de crédito

A aplicação utiliza **Python, pandas, scikit-learn, Flask, HTML, CSS e JavaScript**.

---

## Problema de crédito

A base utilizada possui **6.000 contratos de empréstimo**, com aproximadamente **21% de inadimplentes**.

A variável alvo é:

- `inadimplente = 1`: cliente não pagou o empréstimo
- `inadimplente = 0`: cliente pagou o empréstimo

### Variáveis utilizadas

| Variável | Descrição |
|---|---|
| `idade` | Idade do cliente |
| `renda_mensal` | Renda mensal |
| `tempo_emprego_anos` | Tempo de emprego em anos |
| `score_credito` | Score de crédito entre 300 e 1000 |
| `dividas_ativas` | Número de dívidas em aberto |
| `possui_imovel` | Indica se o cliente possui imóvel |
| `finalidade` | Finalidade do empréstimo |
| `valor_emprestimo` | Valor solicitado |
| `prazo_meses` | Prazo do empréstimo |
| `inadimplente` | Variável alvo |

A coluna `id_contrato` foi removida das features porque é somente um identificador e não representa uma característica útil do cliente.

---

# 1. Análise Exploratória

A análise exploratória foi realizada com `pandas`, `matplotlib` e `seaborn`.

A proporção de inadimplentes encontrada foi de aproximadamente:

```text
21%