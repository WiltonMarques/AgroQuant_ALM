import pandas as pd
import requests
import json
import os
import logging
import io
from datetime import datetime

# ==========================================
# CONFIGURAÇÃO DE LOGS
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ExtratorBGI:
    def __init__(self):
        # Indicador oficial de preços físicos da Arroba no Brasil
        self.url_cepea = "https://www.cepea.esalq.usp.br/br/indicador/boi-gordo.aspx"
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def extrair_spot_cepea(self):
        """Tenta extrair o valor da @ de hoje (Spot) do CEPEA/USP"""
        logging.info("Tentativa 1: Conectando ao indicador CEPEA/Esalq (Spot)...")
        try:
            response = requests.get(self.url_cepea, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Correção do FutureWarning usando io.StringIO
            tabelas = pd.read_html(io.StringIO(response.text), decimal=',', thousands='.')
            df_cepea = tabelas[0]
            
            # O CEPEA mostra o valor em R$ na segunda coluna da primeira linha
            valor_spot = float(df_cepea.iloc[0, 1])
            logging.info(f"Sucesso! BGI Spot (CEPEA) capturado: R$ {valor_spot}")
            return valor_spot
        except Exception as e:
            logging.warning(f"Falha ao acessar CEPEA: {e}")
            return None

    def gerar_dados_sinteticos(self, spot_capturado):
        """
        Gera os dados do Estudo de Caso (Fallback).
        Se o Spot foi capturado, gera apenas a curva Futura com um prêmio (Contango).
        Se falhou tudo, usa os R$ 230,00 e R$ 260,00 do nosso Case Institucional.
        """
        logging.info("Gerando curva BGI Futuro (Estudo de Caso)...")
        
        if spot_capturado:
            # Se pegou o preço real de hoje, simula o futuro a 15% de ágio
            preco_spot = spot_capturado
            preco_futuro_6m = round(preco_spot * 1.15, 2)
            origem = "Híbrido (Spot Real / Futuro Sintético)"
        else:
            # Preços cravados do nosso Estudo de Caso
            preco_spot = 230.00
            preco_futuro_6m = 260.00
            origem = "SINTÉTICO (Estudo de Caso)"

        # Montando a curva futura de vencimentos (Ex: Outubro, Novembro)
        curva_futura = {
            "BGI_Vencimento_M1": round(preco_spot * 1.05, 2),
            "BGI_Vencimento_M3": round(preco_spot * 1.10, 2),
            "BGI_Vencimento_M6": preco_futuro_6m  # Alvo do nosso Hedge
        }
        
        return preco_spot, curva_futura, origem

    def executar(self):
        print("="*60)
        print("🐂 AGROQUANT ALM - INGESTÃO DE MARKET DATA (BGI B3/CEPEA)")
        print("="*60)
        
        # Tenta pegar o preço base real
        valor_spot = self.extrair_spot_cepea()
        
        # Gera o restante dos dados
        spot_final, curva_futuro, origem = self.gerar_dados_sinteticos(valor_spot)

        # Monta o Payload JSON
        payload = {
            "metadata": {
                "projeto": "AgroQuant ALM",
                "data_extracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "origem": origem,
                "descricao": "Cotações Arroba do Boi Gordo (Spot e Futuro B3)"
            },
            "cotacoes": {
                "preco_spot_atual": spot_final,
                "curva_futura": curva_futuro
            }
        }

        # Salva em disco
        caminho_arquivo = os.path.join(self.data_dir, 'cotacoes_bgi.json')
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=4, ensure_ascii=False)
            
        print("-"*60)
        print(f"📡 Origem: {origem}")
        print(f"💲 BGI Spot (Hoje): R$ {spot_final}")
        print(f"📈 BGI Futuro (6 Meses): R$ {curva_futuro['BGI_Vencimento_M6']}")
        print(f"📁 Local salvo: {caminho_arquivo}")
        print("="*60)

if __name__ == "__main__":
    extrator = ExtratorBGI()
    extrator.executar()