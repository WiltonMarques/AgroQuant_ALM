# 🌾 AgroQuant ALM: Institutional Asset Liability Management for Agribusiness

**Status:** 🚧 MVP Functional | #BuildInPublic

O **AgroQuant ALM** é um motor quantitativo desenvolvido em Python projetado para solucionar a maior vulnerabilidade do agronegócio corporativo: a exposição ao risco de juros (Passivo) e à volatilidade de preços (Ativo). 

Diferente de ferramentas de trading direcional, o AgroQuant foca no **Dual-Hedge**, garantindo que a margem operacional da fazenda ou cooperativa seja blindada no "instante zero" através de derivativos na B3, com total aderência regulatória.

## 📌 Contexto Estratégico: A Dor do "Price Taker"
O empresário do agronegócio é, por natureza, um tomador de preços. Ele não dita o custo do capital (CDI) nem o preço da carne (BGI). O AgroQuant ALM devolve o controle da operação ao gestor da Tesouraria, transformando variáveis estocásticas macroeconômicas em constantes matemáticas.

## ⚙️ Arquitetura do Projeto (MVP)
O projeto opera através de uma esteira ETL (Extract, Transform, Load) baseada em microsserviços e Separation of Concerns:
* `captura_curva_di.py`: Ingestão resiliente da curva de juros futuros (B3 com fallback para InfoMoney/Sintético).
* `captura_bgi_b3.py`: Coleta de preços Spot (CEPEA) e Futuros (BGI).
* `gerador_insumos.py`: Parametrização zootécnica (conversão alimentar, reposição e sanidade).
* `agroquant_engine.py`: O "cérebro" que consolida os dados, aplica tributação (Funrural) e orquestra o Hedge.
* `modulo_compliance.py`: Geração de relatórios de auditoria criptografados.

## 🚀 Prova de Conceito (Estudo de Caso & ROI)
Validamos o motor simulando um Confinamento Modelo de 10.000 cabeças com Custeio de R$ 30 Milhões, submetido a um estresse na taxa Selic (de 10.5% para 13.5% a.a.).
- **Capital Salvo do Banco:** R$ 300.000,00 (Diferença entre a dívida exposta e a dívida travada no DI1).
- **Lucro Líquido Final Blindado:** R$ 2.995.000,00.
- **ROI da Tecnologia:** **500%** (O sistema se pagou 5 vezes no primeiro ciclo de volatilidade).

---

## 🛡️ Compliance e Auditoria (Hedge Accounting - CPC 48 / IFRS 9)
Para tesourarias corporativas e cooperativas auditadas por Big4 (PwC, EY, KPMG, Deloitte), operações com derivativos exigem rigorosa documentação. 
O AgroQuant possui um módulo nativo que emite o **Termo de Designação de Hedge**, testando a correlação entre passivo e derivativo e gerando uma **assinatura criptográfica (Hash SHA-256)**. Isso garante a imutabilidade dos dados executados, enquadrando a operação nas regras da CVM e garantindo o diferimento tributário (Hedge Accounting).

---

## 📈 Roadmap: Escalonamento Institucional
Embora o MVP utilize arquivos `.json` para a esteira de dados, a lógica central foi desenhada para escalabilidade em nível Enterprise:

### 1. Integração com ERPs (SAP / TOTVS / Sankhya)
Substituição dos módulos estáticos por conectores nativos. O motor passará a ler o custo real da nota fiscal de ração e da reposição diretamente do banco de dados do ERP, disparando o Hedge baseado no fluxo de caixa real e dinâmico da instituição.

### 2. Infraestrutura Cloud & MLOps
Migração para microsserviços orquestrados (AWS EKS / Databricks) para processamento estocástico e previsão de *Basis Risk* usando simulações de Monte Carlo.

### 3. Inteligência de Tesouraria com GenAI (LLMs)
Implementação de "Co-piloto de Tesouraria" baseado em RAG (Retrieval-Augmented Generation) para traduzir os cálculos matriciais complexos em Notas Técnicas redigidas em linguagem natural para o Comitê de Risco.

---

## 🛠️ Como Executar o Repositório
1. Clone o repositório e instale as dependências: `pip install pandas requests lxml`
2. Os parâmetros globais podem ser ajustados em `data/config_projeto.json`.
3. Para rodar o DRE e gerar o termo de compliance, execute: 
   `python agroquant_engine.py`

## 🤝 Contatos e Contribuições
Projeto desenvolvido por **Wilton Marques do Amaral** (Engenharia de Dados Financeiros e Estruturação ALM). 
Interessado em debater teses quantitativas ou escalar esta solução? Conecte-se via LinkedIn!