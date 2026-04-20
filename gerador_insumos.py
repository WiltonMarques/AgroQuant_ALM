import json
import os
import logging
from datetime import datetime

# ==========================================
# CONFIGURAÇÃO DE LOGS
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class GeradorInsumos:
    def __init__(self):
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def calcular_custo_consolidado(self, params):
        """
        Simula a consolidação dos custos zootécnicos.
        Para o nosso Case, forçaremos o arredondamento para o alvo de R$ 230/@ 
        para bater com o simulador de viabilidade financeira.
        """
        # Custo Fixo de Entrada = Sanidade + Fixos
        custo_entrada = params['sanidade_protocolo_cabeca'] + params['operacional_fixo_cabeca']
        
        # Custo de Nutrição = Diária * Dias de Confinamento
        custo_nutricao = params['diaria_confinamento_nutricao'] * params['dias_ciclo']
        
        # Custo do Boi Magro = Peso Entrada * Preço Arroba Reposição
        custo_reposicao = params['peso_entrada_arrobas'] * params['preco_arroba_reposicao']
        
        custo_total_cabeca = custo_entrada + custo_nutricao + custo_reposicao
        
        # Custo final da arroba produzida
        custo_arroba_final = custo_total_cabeca / params['peso_saida_arrobas']
        
        return round(custo_arroba_final, 2)

    def executar(self):
        print("="*60)
        print("🌽 AGROQUANT ALM - PARAMETRIZAÇÃO DE INSUMOS E ZOOTECNIA")
        print("="*60)
        
        # Parâmetros baseados no nosso Estudo de Caso (Confinamento Modelo)
        # Ajustados matematicamente para resultar no Custo Físico de R$ 230/@
        parametros_operacionais = {
            "dias_ciclo": 180,
            "peso_entrada_arrobas": 13.5,
            "peso_saida_arrobas": 20.0,
            "preco_arroba_reposicao": 200.00,  # Boi Magro
            "diaria_confinamento_nutricao": 10.00, # Ração (Milho/Farelo) + Núcleo
            "sanidade_protocolo_cabeca": 50.00,    # Vacinas, Ivermectina, Mosquicidas
            "operacional_fixo_cabeca": 50.00      # Mão de obra, maquinário, depreciação
        }

        logging.info("Consolidando estrutura de custos físicos...")
        custo_arroba_calculado = self.calcular_custo_consolidado(parametros_operacionais)

        # Monta o Payload JSON
        payload = {
            "metadata": {
                "projeto": "AgroQuant ALM",
                "data_atualizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "origem": "Parametrização Interna (Estudo de Caso)",
                "descricao": "Estrutura de Custos Físicos e Zootécnicos do Confinamento"
            },
            "parametros": parametros_operacionais,
            "resultado_fisico": {
                "custo_total_por_arroba_produzida": custo_arroba_calculado
            }
        }

        # Salva em disco
        caminho_arquivo = os.path.join(self.data_dir, 'custos_producao.json')
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=4, ensure_ascii=False)
            
        print("-"*60)
        print("✅ Parâmetros Zootécnicos processados.")
        print(f"💰 Custo Físico Projetado: R$ {custo_arroba_calculado} por Arroba")
        print(f"📁 Local salvo: {caminho_arquivo}")
        print("="*60)

if __name__ == "__main__":
    gerador = GeradorInsumos()
    gerador.executar()