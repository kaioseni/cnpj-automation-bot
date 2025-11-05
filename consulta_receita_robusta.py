import requests
import pandas as pd
import time
import json
import os
from datetime import datetime
from pandas import json_normalize

# ==========================
# CONFIGURAÇÕES PRINCIPAIS
# ==========================
ARQUIVO_CSV = 'CNPJS.csv'
ARQUIVO_SAIDA = 'dados_empresas.xlsx'
ARQUIVO_LOG = 'log_consulta.txt'
ARQUIVO_PROGRESO = 'progresso.json'
CONSULTAS_POR_LOTE = 3
INTERVALO_SEGUNDOS = 90  # pausa entre lotes
PAUSA_ENTRE_CNPJS = 2    # pausa entre requisições individuais

# ==========================
# FUNÇÕES AUXILIARES
# ==========================
def registrar_log(msg):
    """Registra mensagem no arquivo de log"""
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    print(msg)

def salvar_progresso(cnpjs_processados):
    """Salva progresso no arquivo JSON"""
    with open(ARQUIVO_PROGRESO, "w", encoding="utf-8") as f:
        json.dump(list(cnpjs_processados), f, ensure_ascii=False, indent=2)

def carregar_progresso():
    """Carrega lista de CNPJs já processados"""
    if os.path.exists(ARQUIVO_PROGRESO):
        with open(ARQUIVO_PROGRESO, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

# ==========================
# INÍCIO DO PROCESSAMENTO
# ==========================
registrar_log("=== Iniciando execução ===")

# Lê os CNPJs do CSV
df_cnpjs = pd.read_csv(ARQUIVO_CSV, dtype=str)
cnpjs = df_cnpjs['A2_CGC'].astype(str).str.replace(r'\D', '', regex=True).tolist()

# Carrega progresso anterior
cnpjs_processados = carregar_progresso()
registrar_log(f"CNPJs já processados: {len(cnpjs_processados)}")

# Filtra apenas os que faltam
cnpjs_restantes = [c for c in cnpjs if c not in cnpjs_processados]
registrar_log(f"CNPJs restantes: {len(cnpjs_restantes)}")

dados = []
inicio = time.time()

# Loop principal
for i in range(0, len(cnpjs_restantes), CONSULTAS_POR_LOTE):
    lote = cnpjs_restantes[i:i + CONSULTAS_POR_LOTE]
    registrar_log(f"🚀 Iniciando lote {i // CONSULTAS_POR_LOTE + 1}")

    for cnpj in lote:
        try:
            url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
            registrar_log(f"🔍 Consultando CNPJ: {cnpj}")
            r = requests.get(url, timeout=30)

            if r.status_code == 200:
                data = r.json()
                if data.get("status") != "ERROR":
                    dados.append(data)
                    registrar_log(f"✅ Sucesso: {cnpj}")
                else:
                    registrar_log(f"⚠️ Erro lógico ({data.get('message')}): {cnpj}")
            else:
                registrar_log(f"❌ HTTP {r.status_code} para {cnpj}")

        except Exception as e:
            registrar_log(f"⚠️ Exceção para {cnpj}: {e}")

        # Marca progresso e pausa
        cnpjs_processados.add(cnpj)
        salvar_progresso(cnpjs_processados)
        time.sleep(PAUSA_ENTRE_CNPJS)

    # Espera entre lotes
    if i + CONSULTAS_POR_LOTE < len(cnpjs_restantes):
        registrar_log(f"⏸ Pausando {INTERVALO_SEGUNDOS}s antes do próximo lote...")
        time.sleep(INTERVALO_SEGUNDOS)

# ==========================
# EXPORTAÇÃO FINAL
# ==========================
if dados:
    registrar_log("📊 Normalizando dados e exportando Excel...")

    # Normaliza dados principais
    df_resultado = json_normalize(dados)

    import ast
    import re

    # Função para converter string de lista/dicionário em objeto Python
    def parse_atividade(val):
        if isinstance(val, str):
            try:
                return ast.literal_eval(val)
            except:
                return []
        return val

    # ======= TRATAMENTO DE ATIVIDADE PRINCIPAL =======
    if 'atividade_principal' in df_resultado.columns:
        df_resultado['atividade_principal'] = df_resultado['atividade_principal'].apply(parse_atividade)
        # Remove . e - do código
        df_resultado['atv_principal_code'] = df_resultado['atividade_principal'].apply(
            lambda x: re.sub(r"[.-]", "", x[0]['code']) if x else None
        )
        df_resultado['atv_principal_text'] = df_resultado['atividade_principal'].apply(
            lambda x: x[0]['text'] if x else None
        )
        df_resultado = df_resultado.drop(columns=['atividade_principal'])

    # ======= TRATAMENTO DE ATIVIDADES SECUNDÁRIAS (opcional) =======
    if 'atividades_secundarias' in df_resultado.columns:
        df_resultado['atividades_secundarias'] = df_resultado['atividades_secundarias'].apply(parse_atividade)
        df_resultado['ativ_sec_code'] = df_resultado['atividades_secundarias'].apply(
            lambda x: re.sub(r"[.-]", "", x[0]['code']) if x else None
        )
        df_resultado['ativ_sec_text'] = df_resultado['atividades_secundarias'].apply(
            lambda x: x[0]['text'] if x else None
        )
        df_resultado = df_resultado.drop(columns=['atividades_secundarias'])

    # ======= TRATAMENTO REGEX CAMP CNPJ =======
    if 'cnpj' in df_resultado.columns:
    # Remove '.', '/' e '-' do CNPJ
         df_resultado['cnpj'] = df_resultado['cnpj'].astype(str).str.replace(r"[./-]", "", regex=True)

    # ======= TRATAMENTO REGEX CAMP CEP =======
    if 'cep' in df_resultado.columns:
        df_resultado['cep'] = df_resultado['cep'].astype(str).str.replace(r"[./-]", "", regex=True)

    # ======= TRATAMENTO REGEX CAMP TELEFONE ======
    if 'telefone' in df_resultado.columns:
        df_resultado['telefone'] = df_resultado['telefone'].astype(str).str.replace(r"[-]", "", regex=True)

    # Exporta para Excel
    df_resultado.to_excel(ARQUIVO_SAIDA, index=False)
    registrar_log(f"✅ Planilha '{ARQUIVO_SAIDA}' criada com sucesso!")
else:
    registrar_log("⚠️ Nenhum dado retornado para exportar.")