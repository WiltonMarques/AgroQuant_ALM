import pandas as pd
import requests
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

class ExtratorCurvaDI:
    def __init__(self):
        self.url_b3 = "http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp"
        self.url_infomoney = "https://www.infomoney.com.br/ferramentas/juros-futuros-di/"
        
        # Headers para evitar bloqueios básicos
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def extrair_b3(self):
        """Tenta extrair dados oficiais da B3 (Dias Úteis vs Taxa)"""
        logging.info("Tentativa 1: Conectando à B3...")
        try:
            response = requests.get(self.url_b3, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            tabelas = pd.read_html(response.text, decimal=',', thousands='.')
            df_di = tabelas[0]
            
            df_limpo = df_di.iloc[:, [0, 1]].dropna() 
            df_limpo.columns = ['Dias_Uteis', 'Taxa_DI']
            
            curva_dict = dict(zip(df_limpo['Dias_Uteis'].astype(int), df_limpo['Taxa_DI'].astype(float)))
            logging.info("Sucesso! Dados extraídos da B3.")
            return curva_dict, "REAL (B3)"
        except Exception as e:
            logging.warning(f"Falha na B3: {e}")
            return None, None

    def extrair_infomoney(self):
        """Tenta extrair dados secundários do InfoMoney (Vencimento vs Taxa)"""
        logging.info("Tentativa 2: Conectando ao InfoMoney (Fallback)...")
        try:
            response = requests.get(self.url_infomoney, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            tabelas = pd.read_html(response.text, decimal=',', thousands='.')
            
            # O InfoMoney costuma ter várias tabelas, a de DI geralmente é a primeira ou segunda
            # Vamos procurar a tabela que tenha a coluna 'Vencimento' ou 'Último'
            df_di = None
            for tb in tabelas:
                if 'Vencimento' in tb.columns and 'Último' in tb.columns:
                    df_di = tb
                    break
                    
            if df_di is None:
                raise ValueError("Tabela de DI não encontrada no layout do InfoMoney.")
            
            df_limpo = df_di[['Vencimento', 'Último']].dropna()
            
            curva_dict = dict(zip(df_limpo['Vencimento'].astype(str), df_limpo['Último'].astype(float)))
            logging.info("Sucesso! Dados extraídos do InfoMoney.")
            return curva_dict, "REAL SECUNDÁRIO (InfoMoney)"
        except Exception as e:
            logging.warning(f"Falha no InfoMoney: {e}")
            return None, None

    def gerar_curva_sintetica(self):
        """Gera curva do Estudo de Caso caso não haja internet ou sites bloqueiem."""
        logging.info("Tentativa 3: Gerando Curva Sintética (Estudo de Caso)...")
        dias = [1, 21, 42, 63, 126, 189, 252, 504, 756, 1008]
        taxas = [10.50, 10.65, 10.80, 11.00, 11.50, 12.10, 12.80, 13.20, 13.40, 13.50]
        
        curva_dict = dict(zip(dias, taxas))
        logging.info("Curva sintética ativada.")
        return curva_dict, "SINTÉTICO (Estudo de Caso)"

    def executar(self):
        print("="*60)
        print("🚜 AGROQUANT ALM - INGESTÃO DE MARKET DATA (DI FUTURO)")
        print("="*60)
        
        # Cascata de resiliência: B3 -> InfoMoney -> Sintético
        curva, origem = self.extrair_b3()
        
        if not curva:
            curva, origem = self.extrair_infomoney()
            
        if not curva:
            curva, origem = self.gerar_curva_sintetica()

        payload = {
            "metadata": {
                "projeto": "AgroQuant ALM",
                "data_extracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "origem": origem,
                "descricao": "Curva de Juros Futuros (DI1)"
            },
            "curva_pontos": curva
        }

        caminho_arquivo = os.path.join(self.data_dir, 'curva_di.json')
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=4, ensure_ascii=False)
            
        print("-"*60)
        print(f"📡 Origem dos Dados: {origem}")
        print(f"✅ Vértices capturados: {len(curva)}")
        print(f"📁 Local salvo: {caminho_arquivo}")
        print("="*60)

if __name__ == "__main__":
    extrator = ExtratorCurvaDI()
    extrator.executar()