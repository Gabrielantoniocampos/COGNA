# -*- coding: utf-8 -*-
"""CÓDIGO_competencias_ERP

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YxHMxt_MV1JdLISOjf5HjrcXjt10bfsM
"""

!pip install pandas openpyxl

import pandas as pd
import openpyxl

# Caminhos dos arquivos
arquivo_bib = "/content/ADS.xlsx"
arquivo_sag = "/content/SAG completo com competencia (1) (1).xlsx"

# Carregar planilhas
df_bib = pd.read_excel(arquivo_bib)
df_sag = pd.read_excel(arquivo_sag)

# Padronizar colunas
df_bib.columns = df_bib.columns.str.strip().str.upper()
df_sag.columns = df_sag.columns.str.strip().str.upper()

# Padronizar textos para garantir comparação correta
for col in ['CURSO', 'DISCIPLINA', 'EMENTA']:
    df_bib[col] = df_bib[col].astype(str).str.upper().str.strip()
    df_sag[col] = df_sag[col].astype(str).str.upper().str.strip()

# Agrupar SAG por CURSO + DISCIPLINA + EMENTA, incluindo 'CÓDIGO ERP'
df_sag_agrupado = df_sag.groupby(['CURSO', 'DISCIPLINA', 'EMENTA']).agg({
    'CÓDIGO': 'first',
    'CÓDIGO ERP': 'first',
    'COMPETÊNCIA / HABILIDADE': lambda x: ' | '.join(sorted(set(x.dropna())))
}).reset_index()

# Fazer o merge SEM alterar a quantidade de linhas da planilha de cursos
df_final = pd.merge(
    df_bib,
    df_sag_agrupado,
    on=['CURSO', 'DISCIPLINA', 'EMENTA'],
    how='left'
)

# Reordenar colunas: original + as novas
colunas_originais = df_bib.columns.tolist()
df_final = df_final[colunas_originais + ['CÓDIGO', 'CÓDIGO ERP', 'COMPETÊNCIA / HABILIDADE']]

# Converter 'CÓDIGO ERP' para texto, preservando todos os valores como string
df_final['CÓDIGO ERP'] = df_final['CÓDIGO ERP'].astype(str).str.strip()

# Obter nome do curso na linha 2 (índice 1)
nome_curso = df_bib.loc[1, 'CURSO'].strip().upper().replace(" ", "_").replace("/", "_")

# Salvar com nome do curso
nome_arquivo = f"BIBLIOGRAFIAS_{nome_curso}.xlsx"
df_final.to_excel(nome_arquivo, index=False)

print(f"✅ Planilha gerada com sucesso! Nome do arquivo: {nome_arquivo}")