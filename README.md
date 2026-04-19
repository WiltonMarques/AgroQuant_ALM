# 🌾 AgroQuant ALM: Motor Quantitativo de Dual-Hedge
**Status:** 🚧 Em Desenvolvimento | #BuildInPublic

Bem-vindo ao repositório do **AgroQuant ALM**. Como uma proposta de caso de uso, eu vou desenvolver este projeto para democratizar a Tesouraria Institucional Avançada para o agronegócio corporativo brasileiro, blindando a margem de lucro contra choques estocásticos.

## 📌 Da Porteira para Fora: A Dura Realidade do "Tomador de Preços"
O dia a dia de um empresário do agronegócio é marcado por um nível de excelência que poucos setores alcançam. O produtor domina a genética, o manejo e a agricultura de precisão. Contudo, toda essa previsibilidade desmorona sob a ótica financeira. 

A situação mais perigosa do produtor rural é a sua condição estrutural de ser um **Tomador de Preços (*Price Taker*)**. Ele vive espremido em um "sanduíche financeiro":
1. **Na compra (O Custo):** Adquire insumos e crédito atrelados a taxas macroeconômicas (CDI), sobre os quais tem zero poder de negociação.
2. **Na venda (A Receita):** Vende sua commodity baseado na cotação da B3 ou CBOT. Novamente, ele apenas aceita o preço imposto.

A eficiência no pasto não salva uma tesouraria desprotegida. Se o produtor trava a venda da arroba (BGI) mas deixa a dívida pós-fixada, um aumento na taxa Selic pelo Banco Central transfere todo o seu lucro operacional diretamente para o mercado financeiro.

## 🧬 A Física por trás do Código: Parâmetros Zootécnicos do Motor
O AgroQuant ALM não é apenas uma calculadora de juros; é um motor que traduz biologia em matemática financeira. Para calcular o *Break-even* dinâmico, o algoritmo ingere os custos físicos reais da operação:
1. **Reposição (CAPEX Biológico):** Modelagem baseada na aquisição do "Boi Magro" (média de 13@ a 14@).
2. **Conversão Alimentar (OPEX Nutricional):** Parametrização da ingestão de Matéria Seca (MS), exigindo de 7 kg a 8 kg de MS para a conversão de 1 kg de carcaça.
3. **Barreira Sanitária:** Alocação do Custo Fixo de Entrada referente ao controle de endo e ectoparasitas (Ivermectina, controle de moscas) e vacinação base (clostridioses e Doenças Respiratórias Bovinas). 

## 💡 A Solução: Matemática e Dual-Hedge
Somente após o sistema consolidar o Custo Zootécnico com o Custo do Passivo, a ordem de proteção é disparada. O motor orquestra duas execuções simultâneas:
1. **Hedge do Passivo:** Interpolação na Curva DI Futuro (DI1). O algoritmo sinaliza posição "Tomada", convertendo a dívida flutuante (CDI) em um custo pré-fixado imune ao Banco Central.
2. **Hedge do Ativo:** Com o Custo Financeiro constante, o motor recalcula o *Breakeven* e engatilha a trava da commodity (BGI Futuro). O lucro líquido é cravado no instante zero.

## 🚀 Prova de Conceito e Viabilidade (ROI)
Para validar a viabilidade, estruturamos a simulação do "Confinamento Modelo": 10.000 cabeças (200.000@), operando um ciclo de 6 meses com um custeio de R$ 30 Milhões. O custo de produção cravou em R$ 230/@ e o preço de venda travado a R$ 260/@. 

**O Choque de Mercado:** A Selic saltou de 10.50% para 13.50%.

**Confronto de Cenários (Sem Investimento vs. Com AgroQuant ALM):**
| Item | Operação Exposta (Sem Hedge) | Operação Blindada (AgroQuant ALM) |
| :--- | :--- | :--- |
| **Taxa CDI + Spread** | 13,5% + 3% = **16,5% a.a.** | 11% (Travado no DI1) + 3% = **14,0% a.a.** |
| **Custo Financeiro (6 meses)** | R$ 2.475.000,00 | R$ 2.100.000,00 |
| **Custo do Projeto Tecnológico** | R$ 0,00 | R$ 50.000,00 |
| **Lucro Líquido Final da Fazenda**| **R$ 3.525.000,00** | **R$ 3.850.000,00** |

**Apuração do ROI da Tecnologia:**
* **Ganho Bruto de Proteção:** R$ 375.000,00 (Diferença de juros economizada).
* **Ganho Líquido do Sistema:** R$ 325.000,00 (Ganho - Custo Tech).
* **ROI do Projeto:** **650%**.

Para cada R$ 1,00 investido na arquitetura do AgroQuant ALM, a operação recuperou R$ 6,50 que seriam corroídos pela taxa de juros. A tecnologia quantitativa paga-se integralmente no primeiro ciclo de volatilidade.

## 🛠️ Stack Arquitetural (Roadmap de Desenvolvimento)
Acompanhe o que será desenvolvido nos próximos *Commits*:
- [ ] **Core Engine:** Cálculos matriciais e interpolação da Curva DI (`Python`, `SciPy`, `NumPy`).
- [ ] **Data Ingestion:** Extração de *Market Data* via B3.
- [ ] **Compliance Module:** Geração de *Audit Reports* com registro de operações.

## 🤝 Contribua e Acompanhe
Desenvolvedores quantitativos, engenheiros de dados e profissionais de finanças são convidados a revisar a arquitetura, enviar *Pull Requests* e debater o código.