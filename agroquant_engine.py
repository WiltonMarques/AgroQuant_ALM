import json
import os
import logging

# Configuração limpa para o terminal executivo
logging.basicConfig(level=logging.INFO, format='%(message)s')

class AgroQuantEngine:
    def __init__(self):
        self.data_dir = "data"
        self.config_file = f"{self.data_dir}/config_projeto.json"
        
        # Carregamento Dinâmico das Configurações do Negócio
        self._carregar_configuracoes()

    def _carregar_configuracoes(self):
        """Lê os parâmetros globais do arquivo JSON de configuração."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Vinculando os valores do JSON aos atributos da classe
            self.capital_financiado = config['financeiro']['capital_financiado']
            self.spread_bancario = config['financeiro']['spread_bancario']
            self.custo_tecnologia = config['financeiro']['custo_tecnologia']
            self.selic_estresse = config['financeiro']['selic_estresse']
            self.cabecas_confinadas = config['operacional']['cabecas_confinadas']
            
            logging.info(f"✅ Configurações de Negócio carregadas ({self.config_file})")
            
        except FileNotFoundError:
            logging.error(f"❌ Erro crítico: Arquivo de configuração {self.config_file} não encontrado.")
            exit()
        except KeyError as e:
            logging.error(f"❌ Erro de Schema: Chave não encontrada no JSON de configuração: {e}")
            exit()

    def carregar_dados(self):
        """Lê os JSONs gerados pela nossa esteira ETL (Market Data e Zootecnia)."""
        try:
            with open(f'{self.data_dir}/curva_di.json', 'r', encoding='utf-8') as f:
                self.di_data = json.load(f)
            with open(f'{self.data_dir}/cotacoes_bgi.json', 'r', encoding='utf-8') as f:
                self.bgi_data = json.load(f)
            with open(f'{self.data_dir}/custos_producao.json', 'r', encoding='utf-8') as f:
                self.insumos_data = json.load(f)
                
            logging.info("✅ Dados de Mercado (B3/Insumos) carregados com sucesso.")
        except FileNotFoundError as e:
            logging.error(f"❌ Erro: Execute os extratores primeiro. Arquivo não encontrado: {e}")
            exit()

    def executar_alm(self):
        """Executa o cálculo do Dual-Hedge, Tributação e DRE Final."""
        # 1. PARÂMETROS OPERACIONAIS E FÍSICOS
        peso_saida = self.insumos_data['parametros']['peso_saida_arrobas']
        arrobas_totais = self.cabecas_confinadas * peso_saida
        custo_fisico_arroba = self.insumos_data['resultado_fisico']['custo_total_por_arroba_produzida']
        custo_operacional_total = arrobas_totais * custo_fisico_arroba
        
        # Puxa o preço travado na B3 para daqui a 6 meses
        preco_venda_travado = self.bgi_data['cotacoes']['curva_futura']['BGI_Vencimento_M6']
        receita_bruta = arrobas_totais * preco_venda_travado

        # 2. MALHA TRIBUTÁRIA (Ex: Funrural 1.5% sobre a receita bruta)
        aliquota_funrural = 0.015
        imposto_recolhido = receita_bruta * aliquota_funrural
        receita_liquida = receita_bruta - imposto_recolhido

        # 3. HEDGE DE PASSIVO (O Motor ALM)
        # Pega a taxa DI Futuro travada no JSON (vértice 126 dias úteis = ~6 meses)
        di_travado = self.di_data['curva_pontos']['126']
        
        # Cálculo do custo do dinheiro para o período de 6 meses (taxa anual / 2)
        taxa_banco_sem_hedge = (self.selic_estresse + self.spread_bancario) / 2 / 100
        taxa_banco_com_hedge = (di_travado + self.spread_bancario) / 2 / 100

        despesa_juros_sem_hedge = self.capital_financiado * taxa_banco_sem_hedge
        despesa_juros_com_hedge = self.capital_financiado * taxa_banco_com_hedge

        # 4. APURAÇÃO DE RESULTADOS E ROI
        lucro_sem_hedge = receita_liquida - custo_operacional_total - despesa_juros_sem_hedge
        lucro_com_hedge = receita_liquida - custo_operacional_total - despesa_juros_com_hedge - self.custo_tecnologia

        # Quanto dinheiro deixou de ir para o banco e ficou na fazenda?
        capital_salvo = despesa_juros_sem_hedge - despesa_juros_com_hedge
        
        # Retorno sobre o investimento do projeto de tecnologia
        lucro_tecnologia = capital_salvo - self.custo_tecnologia
        roi_projeto = (lucro_tecnologia / self.custo_tecnologia) * 100

        # Dispara o painel executivo
        self.gerar_relatorio(receita_bruta, imposto_recolhido, custo_operacional_total, 
                             despesa_juros_sem_hedge, despesa_juros_com_hedge, 
                             lucro_sem_hedge, lucro_com_hedge, roi_projeto)

    def gerar_relatorio(self, rec_bruta, imposto, custo_op, juros_sem, juros_com, lucro_sem, lucro_com, roi):
        print("\n" + "="*75)
        print(" 🏛️  AGROQUANT ALM - DEMONSTRATIVO DE RESULTADOS (DRE) E ROI")
        print("="*75)
        print(f"🔹 Volume Negociado na B3 (BGI): {self.cabecas_confinadas * 20:,.0f} @")
        print(f"🔹 Receita Bruta da Operação:    R$ {rec_bruta:>14,.2f}")
        print(f"🔻 (-) Tributos (Funrural 1.5%): R$ {imposto:>14,.2f}")
        print(f"🔻 (-) Custo Físico de Produção: R$ {custo_op:>14,.2f}")
        print("-" * 75)
        print("📊 CUSTO FINANCEIRO (Dívida de R$ 30 Milhões)")
        print(f"   ► Sem Hedge (Juros 16.5% a.a): R$ {juros_sem:>14,.2f}")
        print(f"   ► Com Hedge (Travado 14% a.a): R$ {juros_com:>14,.2f}")
        print("-" * 75)
        print("💰 LUCRO LÍQUIDO DA OPERAÇÃO")
        print(f"   ► Fazenda Exposta:             R$ {lucro_sem:>14,.2f}")
        print(f"   ► Fazenda Blindada (AgroQuant):R$ {lucro_com:>14,.2f} 🏆")
        print("="*75)
        print("🚀 ANÁLISE DE VIABILIDADE DA TECNOLOGIA")
        print(f"   ► Custo de Implantação Cloud:  R$ {self.custo_tecnologia:>14,.2f}")
        print(f"   ► Capital Salvo do Banco:      R$ {(juros_sem - juros_com):>14,.2f}")
        print(f"   ► Retorno do Investimento:     {roi:>14.0f}% (ROI)")
        print("="*75 + "\n")

if __name__ == "__main__":
    engine = AgroQuantEngine()
    engine.carregar_dados()
    engine.executar_alm()