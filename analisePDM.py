import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import numpy as np

# --- Configurações Iniciais ---
BASE_PATH = "/Users/fred/Downloads"  # ATENÇÃO: Confirme se este é o caminho correto
OUTPUT_GRAPH_PATH = os.path.join(BASE_PATH, "graficos_analise_institucional_v7.13_Indentation_Fix")

# Criar diretório para gráficos se não existir
if not os.path.exists(OUTPUT_GRAPH_PATH):
    os.makedirs(OUTPUT_GRAPH_PATH)

# Nomes dos arquivos de dados principais (Consolidados)
FILE_CONSOLIDADO_TECNICO_INTEGRADO = os.path.join(BASE_PATH, "Consolidado_Tecnico_Integrado.xlsx")
FILE_CONSOLIDADO_TECNICO_INTEGRADO_EJA = os.path.join(BASE_PATH, "Consolidado_Tecnico_Integrado_EJA.xlsx")

# Arquivos do Programa Pé de Meia
FILE_PDM_EMR_CSV = os.path.join(BASE_PATH, "status-estudante-programa-EMR-rede-223254_1-2024.csv")
FILE_PDM_EJA_CSV = os.path.join(BASE_PATH, "status-estudante-programa-EJA-rede-223254_1-2024.csv")

# Mapeamento de Campi para Regiões
CAMPUS_REGIAO_MAP = {
    'Leste Potiguar': ['CNAT', 'ZN', 'CAL', 'PAR', 'CANG', 'SGA', 'CM'],
    'Oeste Potiguar': ['MO', 'AP', 'IP', 'PF'],
    'Seridó': ['CA', 'JUC', 'PAAS', 'CN'],
    'Agreste Potiguar': ['JC', 'SPP', 'SC', 'NC'],
    'Central Potiguar': ['LAJ', 'MC']
}

# --- Nomes das Colunas (AJUSTADOS CONFORME ÚLTIMA INFORMAÇÃO DO USUÁRIO) ---
COL_ANO_INGRESSO = "Ano de Ingresso"
COL_ANO_CONCLUSAO = "Ano de Conclusão"
COL_ANO_PERIODO_REF = "Ano Letivo"
COL_PERIODO_REF = "Período Letivo"
COL_SITUACAO_PERIODO = "Situação no Período"
COL_CAMPUS = "Campus"
COL_CPF_CONSOLIDADO = "CPF"
COL_FREQUENCIA_ALUNO_PERIODO = "Frequência no Período"

COL_CPF_PDM = "CPF"
COL_SITUACAO_PDM = "Situação"

# --- Valores para Situação (VERIFIQUE E AJUSTE CONFORME SEUS DADOS) ---
VALOR_REPROVADO = "Reprovado"
VALOR_DEPENDENCIA = "Dependência"
VALOR_APROVADO = "Aprovado no período"
VALOR_PDM_ELEGIVEL = "Elegível"


# --- Funções Auxiliares ---
def clean_cpf(cpf_series):
    return cpf_series.astype(str).str.replace(r'[.\-\s]', '', regex=True).str.strip()


def to_numeric_silent(series):
    return pd.to_numeric(series, errors='coerce')


def format_consolidado_frequency(freq_series):
    if freq_series.dtype == 'object':
        freq_series = freq_series.str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
    return pd.to_numeric(freq_series, errors='coerce')


def processar_dados_consolidados(filepath, modalidade_nome):
    print(f"\nProcessando arquivo consolidado: {filepath} para Modalidade: {modalidade_nome}")
    try:
        df = pd.read_excel(filepath)
    except FileNotFoundError:
        print(f"ERRO: Arquivo {filepath} não encontrado.")
        return pd.DataFrame(), pd.DataFrame()

    expected_cols = [COL_ANO_INGRESSO, COL_ANO_CONCLUSAO, COL_ANO_PERIODO_REF,
                     COL_PERIODO_REF, COL_SITUACAO_PERIODO, COL_CAMPUS, COL_CPF_CONSOLIDADO,
                     COL_FREQUENCIA_ALUNO_PERIODO]
    for col in expected_cols:
        if col not in df.columns:
            print(f"AVISO: Coluna '{col}' não encontrada em {filepath}. Verifique o nome da coluna no script.")
            df[col] = np.nan

    if COL_CPF_CONSOLIDADO in df.columns and df[COL_CPF_CONSOLIDADO].notna().any():
        df[COL_CPF_CONSOLIDADO] = clean_cpf(df[COL_CPF_CONSOLIDADO])
    if COL_CAMPUS in df.columns:
        df[COL_CAMPUS] = df[COL_CAMPUS].fillna('N/A')

    if COL_FREQUENCIA_ALUNO_PERIODO in df.columns and df[COL_FREQUENCIA_ALUNO_PERIODO].notna().any():
        df['FrequenciaAluno'] = format_consolidado_frequency(df[COL_FREQUENCIA_ALUNO_PERIODO])
    else:
        df['FrequenciaAluno'] = np.nan

    all_dfs_agg = []

    if COL_ANO_INGRESSO in df.columns and df[COL_ANO_INGRESSO].notna().any() and \
            COL_CPF_CONSOLIDADO in df.columns and df[COL_CPF_CONSOLIDADO].notna().any():
        df_matriculados = df.copy()
        df_matriculados['Ano'] = to_numeric_silent(df_matriculados[COL_ANO_INGRESSO])
        df_matriculados.dropna(subset=['Ano', COL_CPF_CONSOLIDADO], inplace=True)

        if not df_matriculados.empty:
            df_matriculados['Ano'] = df_matriculados['Ano'].astype(int)
            df_matriculados = df_matriculados[(df_matriculados['Ano'] >= 2018) & (df_matriculados['Ano'] <= 2024)]

            if not df_matriculados.empty:
                matriculados_agg = df_matriculados.drop_duplicates(subset=['Ano', COL_CPF_CONSOLIDADO]) \
                    .groupby(['Ano', COL_CAMPUS]).size().reset_index(name='Count')
                matriculados_agg['TipoIndicador'] = 'Matriculado'
                all_dfs_agg.append(matriculados_agg)

    if COL_ANO_CONCLUSAO in df.columns and df[COL_ANO_CONCLUSAO].notna().any() and \
            COL_CPF_CONSOLIDADO in df.columns and df[COL_CPF_CONSOLIDADO].notna().any():
        df_concluidos = df.copy()
        df_concluidos['Ano'] = to_numeric_silent(df_concluidos[COL_ANO_CONCLUSAO])
        df_concluidos.dropna(subset=['Ano', COL_CPF_CONSOLIDADO], inplace=True)
        if not df_concluidos.empty:
            df_concluidos['Ano'] = df_concluidos['Ano'].astype(int)
            df_concluidos = df_concluidos[(df_concluidos['Ano'] >= 2018) & (df_concluidos['Ano'] <= 2024)]
            if not df_concluidos.empty:
                concluidos_agg = df_concluidos.drop_duplicates(subset=['Ano', COL_CPF_CONSOLIDADO]) \
                    .groupby(['Ano', COL_CAMPUS]).size().reset_index(name='Count')
                concluidos_agg['TipoIndicador'] = 'Concluído'
                all_dfs_agg.append(concluidos_agg)

    df_desempenho_individual_todos_anos = pd.DataFrame()

    if COL_ANO_PERIODO_REF in df.columns and df[COL_ANO_PERIODO_REF].notna().any() and \
            COL_PERIODO_REF in df.columns and df[COL_PERIODO_REF].notna().any() and \
            COL_CPF_CONSOLIDADO in df.columns and df[COL_CPF_CONSOLIDADO].notna().any() and \
            COL_SITUACAO_PERIODO in df.columns and df[COL_SITUACAO_PERIODO].notna().any():

        temp_df_periodo = df.copy()
        temp_df_periodo['AnoRef'] = to_numeric_silent(temp_df_periodo[COL_ANO_PERIODO_REF])
        temp_df_periodo['PeriodoRef'] = to_numeric_silent(temp_df_periodo[COL_PERIODO_REF])
        temp_df_periodo['AnoConclusaoNum'] = to_numeric_silent(temp_df_periodo[COL_ANO_CONCLUSAO])
        temp_df_periodo.dropna(subset=['AnoRef', 'PeriodoRef', COL_CPF_CONSOLIDADO], inplace=True)

        if not temp_df_periodo.empty:
            temp_df_periodo['AnoRef'] = temp_df_periodo['AnoRef'].astype(int)
            temp_df_periodo['PeriodoRef'] = temp_df_periodo['PeriodoRef'].astype(int)

            df_desempenho_ind = temp_df_periodo[
                (temp_df_periodo['AnoRef'] >= 2018) & (temp_df_periodo['AnoRef'] <= 2024)].copy()

            if modalidade_nome == "Técnico Integrado":
                df_desempenho_ind = df_desempenho_ind[df_desempenho_ind['PeriodoRef'] == 1].copy()

            cols_desempenho = [COL_CPF_CONSOLIDADO, 'AnoRef', 'PeriodoRef', COL_CAMPUS,
                               COL_SITUACAO_PERIODO, 'AnoConclusaoNum', 'FrequenciaAluno']
            cols_desempenho_existentes = [col for col in cols_desempenho if col in df_desempenho_ind.columns]

            if not df_desempenho_ind.empty and set(cols_desempenho_existentes).issuperset(set(cols_desempenho)):
                df_desempenho_individual_todos_anos = df_desempenho_ind[cols_desempenho_existentes].copy()
                df_desempenho_individual_todos_anos.rename(columns={
                    COL_CAMPUS: 'Campus', COL_CPF_CONSOLIDADO: 'CPF',
                    'AnoRef': 'Ano', 'PeriodoRef': 'Periodo',
                    'AnoConclusaoNum': 'AnoConclusao'
                }, inplace=True)
                df_desempenho_individual_todos_anos['Modalidade'] = modalidade_nome
            else:
                df_desempenho_individual_todos_anos = pd.DataFrame(
                    columns=['CPF', 'Ano', 'Periodo', 'Campus', COL_SITUACAO_PERIODO, 'AnoConclusao', 'FrequenciaAluno',
                             'Modalidade'])

        df_reprovados_hist = df[df[COL_SITUACAO_PERIODO] == VALOR_REPROVADO].copy()
        if not df_reprovados_hist.empty:
            df_reprovados_hist['Ano'] = to_numeric_silent(df_reprovados_hist[COL_ANO_PERIODO_REF])
            df_reprovados_hist['Periodo'] = to_numeric_silent(df_reprovados_hist[COL_PERIODO_REF])
            df_reprovados_hist.dropna(subset=['Ano', 'Periodo'], inplace=True)
            if not df_reprovados_hist.empty:
                df_reprovados_hist['Ano'] = df_reprovados_hist['Ano'].astype(int)
                df_reprovados_hist['Periodo'] = df_reprovados_hist['Periodo'].astype(int)
                df_reprovados_hist = df_reprovados_hist[
                    (df_reprovados_hist['Ano'] >= 2018) & (df_reprovados_hist['Ano'] <= 2024)]
                if modalidade_nome == "Técnico Integrado":
                    df_reprovados_hist = df_reprovados_hist[df_reprovados_hist['Periodo'] == 1].copy()
                if not df_reprovados_hist.empty:
                    reprovados_agg_hist = df_reprovados_hist.groupby(['Ano', 'Periodo', COL_CAMPUS]).size().reset_index(
                        name='Count')
                    reprovados_agg_hist['TipoIndicador'] = 'Reprovado'
                    all_dfs_agg.append(reprovados_agg_hist)

        df_dependencia_hist = df[df[COL_SITUACAO_PERIODO] == VALOR_DEPENDENCIA].copy()
        if not df_dependencia_hist.empty:
            df_dependencia_hist['Ano'] = to_numeric_silent(df_dependencia_hist[COL_ANO_PERIODO_REF])
            df_dependencia_hist['Periodo'] = to_numeric_silent(df_dependencia_hist[COL_PERIODO_REF])
            df_dependencia_hist.dropna(subset=['Ano', 'Periodo'], inplace=True)
            if not df_dependencia_hist.empty:
                df_dependencia_hist['Ano'] = df_dependencia_hist['Ano'].astype(int)
                df_dependencia_hist['Periodo'] = df_dependencia_hist['Periodo'].astype(int)
                df_dependencia_hist = df_dependencia_hist[
                    (df_dependencia_hist['Ano'] >= 2018) & (df_dependencia_hist['Ano'] <= 2024)]
                if modalidade_nome == "Técnico Integrado":
                    df_dependencia_hist = df_dependencia_hist[df_dependencia_hist['Periodo'] == 1].copy()
                if not df_dependencia_hist.empty:
                    dependencia_agg_hist = df_dependencia_hist.groupby(
                        ['Ano', 'Periodo', COL_CAMPUS]).size().reset_index(name='Count')
                    dependencia_agg_hist['TipoIndicador'] = 'Dependência'
                    all_dfs_agg.append(dependencia_agg_hist)
    else:
        print(
            f"AVISO: Colunas essenciais para indicadores de período não encontradas ou vazias em {filepath}. Análise de período e PDM comprometida.")
        df_desempenho_individual_todos_anos = pd.DataFrame(
            columns=['CPF', 'Ano', 'Periodo', 'Campus', COL_SITUACAO_PERIODO, 'AnoConclusao', 'FrequenciaAluno',
                     'Modalidade'])

    if not all_dfs_agg:
        df_historico_agregado = pd.DataFrame()
    else:
        df_historico_agregado = pd.concat(all_dfs_agg, ignore_index=True)
        if not df_historico_agregado.empty:
            df_historico_agregado['Modalidade'] = modalidade_nome
            df_historico_agregado.rename(columns={COL_CAMPUS: 'Campus'}, inplace=True)

    return df_historico_agregado, df_desempenho_individual_todos_anos


def carregar_dados_pdm(filepath_pdm, modalidade_nome):
    print(f"Carregando dados PDM: {filepath_pdm}")
    try:
        df_pdm = pd.read_csv(filepath_pdm, usecols=[COL_CPF_PDM, COL_SITUACAO_PDM], sep=';')
        df_pdm['CPF'] = clean_cpf(df_pdm[COL_CPF_PDM])

        if COL_SITUACAO_PDM in df_pdm.columns:
            df_pdm[COL_SITUACAO_PDM] = df_pdm[COL_SITUACAO_PDM].astype(str).str.strip()

        df_pdm['StatusPDM'] = np.where(df_pdm[COL_SITUACAO_PDM] == VALOR_PDM_ELEGIVEL,
                                       'Elegível PDM', 'Não Elegível PDM')
        df_pdm['Modalidade'] = modalidade_nome

        print(
            f"  DEBUG PDM: Contagem de StatusPDM classificados para {modalidade_nome} (VALOR_PDM_ELEGIVEL='{VALOR_PDM_ELEGIVEL}'):\n{df_pdm['StatusPDM'].value_counts(dropna=False)}")

        print(f"  - Dados PDM para {modalidade_nome} carregados: {len(df_pdm)} linhas.")
        return df_pdm[['CPF', 'StatusPDM', 'Modalidade']].drop_duplicates(subset=['CPF', 'Modalidade'])
    except FileNotFoundError:
        print(f"AVISO: Arquivo PDM {filepath_pdm} não encontrado.")
        return pd.DataFrame(columns=['CPF', 'StatusPDM', 'Modalidade'])
    except Exception as e:
        print(f"ERRO ao carregar ou processar arquivo PDM {filepath_pdm}: {e}")
        return pd.DataFrame(columns=['CPF', 'StatusPDM', 'Modalidade'])


# --- Processamento Principal ---
df_integrado_hist_agg, df_integrado_desempenho_ind = processar_dados_consolidados(FILE_CONSOLIDADO_TECNICO_INTEGRADO,
                                                                                  "Técnico Integrado")
df_eja_hist_agg, df_eja_desempenho_ind = processar_dados_consolidados(FILE_CONSOLIDADO_TECNICO_INTEGRADO_EJA,
                                                                      "Técnico Integrado EJA")

df_todos_indicadores_historicos = pd.concat([df_integrado_hist_agg, df_eja_hist_agg], ignore_index=True)
df_todo_desempenho_individual = pd.concat([df_integrado_desempenho_ind, df_eja_desempenho_ind], ignore_index=True)

df_pdm_emr_proc = carregar_dados_pdm(FILE_PDM_EMR_CSV, "Técnico Integrado")
df_pdm_eja_proc = carregar_dados_pdm(FILE_PDM_EJA_CSV, "Técnico Integrado EJA")
df_pdm_todos = pd.concat([df_pdm_emr_proc, df_pdm_eja_proc], ignore_index=True)
if not df_pdm_todos.empty:
    df_pdm_todos.drop_duplicates(subset=['CPF', 'Modalidade'], inplace=True)

# Combinar dados de desempenho individual (todos os anos) com PDM
df_desempenho_completo_pdm = pd.DataFrame(
    columns=['CPF', 'Ano', 'Periodo', 'Campus', COL_SITUACAO_PERIODO, 'AnoConclusao', 'FrequenciaAluno', 'Modalidade',
             'StatusPDM'])  # Inicializa com colunas
if not df_todo_desempenho_individual.empty and 'CPF' in df_todo_desempenho_individual.columns and \
        not df_pdm_todos.empty and 'CPF' in df_pdm_todos.columns and 'Modalidade' in df_todo_desempenho_individual.columns:
    df_desempenho_completo_pdm = pd.merge(df_todo_desempenho_individual, df_pdm_todos, on=['CPF', 'Modalidade'],
                                          how='left')
    if 'StatusPDM' in df_desempenho_completo_pdm.columns:
        df_desempenho_completo_pdm['StatusPDM'] = df_desempenho_completo_pdm['StatusPDM'].fillna('Sem Info PDM')
    else:
        df_desempenho_completo_pdm['StatusPDM'] = 'Sem Info PDM'
    print(
        f"\nDados de desempenho individual (todos os anos) combinados com PDM. Total de linhas: {len(df_desempenho_completo_pdm)}")
else:
    print("\nAVISO: Não foi possível combinar dados de desempenho individual com PDM.")

# --- Funções de Plotagem (Histórico) ---
sns.set_theme(style="whitegrid")


def plot_evolucao_geral(df_total, modalidade_sel, tipo_indicador_sel, output_path):
    if df_total.empty: return
    df_plot = df_total[
        (df_total['Modalidade'] == modalidade_sel) & (df_total['TipoIndicador'] == tipo_indicador_sel)].copy()
    if df_plot.empty: return

    if tipo_indicador_sel in ['Reprovado', 'Dependência']:
        if 'Periodo' not in df_plot.columns or 'Ano' not in df_plot.columns: return
        df_plot['AnoPeriodo'] = df_plot['Ano'].astype(str) + "." + df_plot['Periodo'].astype(str)
        df_agg = df_plot.groupby('AnoPeriodo')['Count'].sum().reset_index()
        if df_agg.empty: return
        try:
            df_agg['AnoNumeric'] = df_agg['AnoPeriodo'].apply(lambda x: float(x))
            df_agg = df_agg.sort_values('AnoNumeric').drop(columns=['AnoNumeric'])
        except ValueError:
            df_agg = df_agg.sort_values('AnoPeriodo')
        x_axis, x_label, title_suffix = 'AnoPeriodo', 'Ano e Período Letivo', f"{tipo_indicador_sel}s por Período"
    else:
        if 'Ano' not in df_plot.columns: return
        df_agg = df_plot.groupby('Ano')['Count'].sum().reset_index().sort_values('Ano')
        if df_agg.empty: return
        x_axis, x_label, title_suffix = 'Ano', 'Ano', f"{tipo_indicador_sel}s por Ano"

    plt.figure(figsize=(12, 7))
    ax = sns.lineplot(data=df_agg, x=x_axis, y='Count', marker='o', linewidth=2.5, markersize=8, legend=False,
                      color='royalblue')
    for _, row in df_agg.iterrows():
        ax.text(row[x_axis], row['Count'], f'{int(row["Count"])}', ha='center', va='bottom', fontsize=9, color='black',
                fontweight='medium')
    plt.title(f'Evolução Geral de {title_suffix} - {modalidade_sel}', fontsize=15, weight='bold')
    plt.xlabel(x_label, fontsize=12);
    plt.ylabel(f'Número de Alunos', fontsize=12)

    ax.spines['top'].set_visible(False);
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('grey');
    ax.spines['bottom'].set_color('grey')

    if x_axis == 'Ano':
        plt.gca().xaxis.set_major_locator(mticker.MaxNLocator(integer=True));
        if not df_agg.empty and not df_agg[x_axis].empty: plt.xticks(df_agg[x_axis].unique())
    else:
        plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.6, axis='y');
    plt.tight_layout()
    filename = os.path.join(output_path,
                            f"HIST_evolucao_geral_{tipo_indicador_sel.lower()}_{modalidade_sel.lower().replace(' ', '_')}.png")
    plt.savefig(filename);
    plt.close();
    print(f"Gráfico salvo: {filename}")


def plot_evolucao_regional(df_total, modalidade_sel, tipo_indicador_sel, regiao_nome, campi_da_regiao, output_path):
    if df_total.empty: return
    df_plot_campuses = df_total[
        (df_total['Modalidade'] == modalidade_sel) & (df_total['TipoIndicador'] == tipo_indicador_sel) & (
            df_total['Campus'].isin(campi_da_regiao))].copy()
    if df_plot_campuses.empty: return

    if tipo_indicador_sel in ['Reprovado', 'Dependência']:
        if 'Periodo' not in df_plot_campuses.columns or 'Ano' not in df_plot_campuses.columns: return
        df_plot_campuses['AnoPeriodo'] = df_plot_campuses['Ano'].astype(str) + "." + df_plot_campuses['Periodo'].astype(
            str)
        df_pivot = df_plot_campuses.groupby(['AnoPeriodo', 'Campus'])['Count'].sum().unstack(fill_value=0)
        if df_pivot.empty: return
        try:
            df_pivot['AnoNumeric'] = df_pivot.index.to_series().apply(lambda x: float(x))
            df_pivot = df_pivot.sort_values('AnoNumeric').drop(columns=['AnoNumeric'])
        except ValueError:
            df_pivot = df_pivot.sort_index()
        x_axis_col, x_label, title_suffix = df_pivot.index, 'Ano e Período Letivo', f"{tipo_indicador_sel}s por Período"
    else:
        if 'Ano' not in df_plot_campuses.columns: return
        df_pivot = df_plot_campuses.groupby(['Ano', 'Campus'])['Count'].sum().unstack(fill_value=0)
        if df_pivot.empty: return
        df_pivot = df_pivot.sort_index()
        x_axis_col, x_label, title_suffix = df_pivot.index, 'Ano', f"{tipo_indicador_sel}s por Ano"

    for campus_reg in campi_da_regiao:
        if campus_reg not in df_pivot.columns: df_pivot[campus_reg] = 0
    df_pivot = df_pivot.reindex(columns=campi_da_regiao, fill_value=0)
    num_campi_na_regiao = len(campi_da_regiao)
    if num_campi_na_regiao == 0: return
    palette = sns.color_palette("tab10", num_campi_na_regiao)
    plt.figure(figsize=(14, 7));
    ax = plt.gca()
    for i, campus_name in enumerate(campi_da_regiao):
        if campus_name in df_pivot.columns:
            sns.lineplot(x=x_axis_col, y=df_pivot[campus_name], label=campus_name, marker='o', linewidth=2,
                         markersize=7, color=palette[i % len(palette)], ax=ax)
            for x_val, y_count in zip(x_axis_col, df_pivot[campus_name]):
                if y_count > 0: ax.text(x_val, y_count, f'{int(y_count)}', ha='center', va='bottom', fontsize=8,
                                        color=palette[i % len(palette)], fontweight='normal')
    ax.spines['top'].set_visible(False);
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('grey');
    ax.spines['bottom'].set_color('grey')
    plt.title(f'Evolução por Campus ({title_suffix}) - {modalidade_sel} (Região: {regiao_nome})', fontsize=16,
              weight='bold')
    plt.xlabel(x_label, fontsize=12);
    plt.ylabel(f'Número de Alunos', fontsize=12)
    if x_label == 'Ano':
        ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True));
        if not x_axis_col.empty: plt.xticks(x_axis_col.unique())
    else:
        plt.xticks(rotation=45, ha='right')
    if num_campi_na_regiao > 0: ax.legend(title='Campus', bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.,
                                          fontsize=9, title_fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6, axis='y');
    plt.tight_layout(rect=[0, 0, 0.88, 1])
    filename_suffix = tipo_indicador_sel.lower().replace(' ', '_').replace('/', '_')
    regiao_filename = regiao_nome.lower().replace(' ', '_').replace('ã', 'a').replace('é', 'e')
    filename = os.path.join(output_path,
                            f"HIST_evolucao_regional_{regiao_filename}_{filename_suffix}_{modalidade_sel.lower().replace(' ', '_')}.png")
    plt.savefig(filename);
    plt.close();
    print(f"Gráfico salvo: {filename}")


# --- Funções de Plotagem (Análise PDM) ---
def plot_pdm_comparativo_anual(df_agg_pdm, modalidade_sel, metrica_nome, y_label, is_rate, output_path, x_col='Ano',
                               x_label_text='Ano'):
    if df_agg_pdm.empty: return
    df_plot = df_agg_pdm[
        (df_agg_pdm['Modalidade'] == modalidade_sel) &
        (df_agg_pdm['StatusPDM'].isin(['Elegível PDM', 'Não Elegível PDM']))
        ].copy()

    if df_plot.empty or metrica_nome not in df_plot.columns:
        print(f"Sem dados para plotar PDM Comparativo Anual: Mod: {modalidade_sel}, Metrica: {metrica_nome}")
        return

    df_plot = df_plot.sort_values(x_col)
    if df_plot.empty: return

    plt.figure(figsize=(12, 7))
    custom_palette = {"Elegível PDM": "cornflowerblue", "Não Elegível PDM": "lightskyblue"}
    ax = sns.barplot(data=df_plot, x=x_col, y=metrica_nome, hue='StatusPDM', palette=custom_palette, width=0.8)

    for p in ax.patches:
        height = p.get_height()
        if pd.notna(height) and height > 0:
            label_text = f'{height:.0f}' if not is_rate else f'{height:.1f}%'
            ax.text(p.get_x() + p.get_width() / 2., height + (plt.gca().get_ylim()[1] * 0.01), label_text,
                    ha='center', va='bottom', fontsize=9, color='black', weight='medium')

    ax.spines['top'].set_visible(False);
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False);
    ax.spines['bottom'].set_color('lightgrey')
    ax.set_yticks([]);
    ax.set_ylabel('')

    title_text = f'{y_label} Anual (2018-2024)\npor Status Pé de Meia (de 2024) - {modalidade_sel}'
    if "Período" in x_label_text:
        title_text = f'{y_label} por Período (2018-2024)\npor Status Pé de Meia (de 2024) - {modalidade_sel}'
        plt.xticks(rotation=45, ha='right')

    plt.title(title_text, fontsize=15, weight='bold', pad=20)
    plt.xlabel(x_label_text, fontsize=12, labelpad=10)
    if is_rate:
        current_max_y = df_plot[metrica_nome].max() if not df_plot[metrica_nome].empty and df_plot[
            metrica_nome].notna().any() else 0
        plt.ylim(0, max(100, current_max_y * 1.15 if pd.notna(current_max_y) else 100))

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, title='Status PDM (2024)', loc='upper center',
              bbox_to_anchor=(0.5, -0.15 if "Período" not in x_label_text else -0.25), ncol=2, frameon=False)

    plt.grid(False);
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    filename = os.path.join(output_path,
                            f"PDM_{metrica_nome.lower()}_anual_comparativa_{modalidade_sel.lower().replace(' ', '_')}.png")
    plt.savefig(filename);
    plt.close();
    print(f"Gráfico salvo: {filename}")
    print(f"NOTA: Este gráfico usa o Status PDM de 2024 para analisar {metrica_nome.lower()} de 2018-2024.")


# --- Cálculo dos Indicadores PDM Anuais (2018-2024) ---
df_pdm_concluidos_anual_agg = pd.DataFrame()
df_pdm_reprovacao_anual_periodo_agg = pd.DataFrame()
df_pdm_dependencia_anual_periodo_agg = pd.DataFrame()
df_pdm_media_freq_anual_agg = pd.DataFrame()

if not df_desempenho_completo_pdm.empty:
    print("\nCalculando indicadores anuais (2018-2024) por Status PDM...")

    if 'AnoConclusao' in df_desempenho_completo_pdm.columns and df_desempenho_completo_pdm[
        'AnoConclusao'].notna().any():
        df_concl_pdm = df_desempenho_completo_pdm.dropna(subset=['AnoConclusao', 'CPF']).copy()
        if not df_concl_pdm.empty:
            # A conversão para int e o filtro de ano já devem ter sido feitos em processar_dados_consolidados
            # Mas, para garantir, podemos re-aplicar se necessário, ou confiar que df_desempenho_completo_pdm já está correto.
            # A coluna 'AnoConclusao' em df_desempenho_completo_pdm é o 'AnoConclusaoNum' original.
            # A coluna 'Ano' em df_desempenho_completo_pdm é o 'AnoRef' (Ano Letivo de Referência).
            # Para concluídos, precisamos agrupar pelo ano em que a conclusão ocorreu.
            df_pdm_concluidos_anual_agg = df_concl_pdm[df_concl_pdm['AnoConclusao'].notna()] \
                .drop_duplicates(subset=['AnoConclusao', 'CPF', 'StatusPDM', 'Modalidade']) \
                .groupby([df_concl_pdm['AnoConclusao'].astype(int), 'Modalidade', 'StatusPDM']) \
                .size().reset_index(name='N_Concluidos')
            df_pdm_concluidos_anual_agg.rename(columns={'AnoConclusao': 'Ano'}, inplace=True)

    if COL_SITUACAO_PERIODO in df_desempenho_completo_pdm.columns and \
            'Ano' in df_desempenho_completo_pdm.columns and 'Periodo' in df_desempenho_completo_pdm.columns:

        df_total_situacao_periodo = df_desempenho_completo_pdm.dropna(
            subset=['CPF', 'Ano', 'Periodo', COL_SITUACAO_PERIODO]) \
            .drop_duplicates(subset=['CPF', 'Ano', 'Periodo', 'Modalidade', 'StatusPDM']) \
            .groupby(['Ano', 'Periodo', 'Modalidade', 'StatusPDM']) \
            .size().reset_index(name='TotalAlunosPeriodo')

        df_reprov_pdm_periodo = df_desempenho_completo_pdm[
            df_desempenho_completo_pdm[COL_SITUACAO_PERIODO] == VALOR_REPROVADO] \
            .dropna(subset=['CPF', 'Ano', 'Periodo']) \
            .drop_duplicates(subset=['CPF', 'Ano', 'Periodo', 'Modalidade', 'StatusPDM']) \
            .groupby(['Ano', 'Periodo', 'Modalidade', 'StatusPDM']) \
            .size().reset_index(name='N_Reprovados')

        df_depend_pdm_periodo = df_desempenho_completo_pdm[
            df_desempenho_completo_pdm[COL_SITUACAO_PERIODO] == VALOR_DEPENDENCIA] \
            .dropna(subset=['CPF', 'Ano', 'Periodo']) \
            .drop_duplicates(subset=['CPF', 'Ano', 'Periodo', 'Modalidade', 'StatusPDM']) \
            .groupby(['Ano', 'Periodo', 'Modalidade', 'StatusPDM']) \
            .size().reset_index(name='N_Dependencia')

        if not df_total_situacao_periodo.empty:
            df_pdm_reprovacao_anual_periodo_agg = pd.merge(df_total_situacao_periodo, df_reprov_pdm_periodo,
                                                           on=['Ano', 'Periodo', 'Modalidade', 'StatusPDM'],
                                                           how='left').fillna(0)
            if 'N_Reprovados' not in df_pdm_reprovacao_anual_periodo_agg.columns: df_pdm_reprovacao_anual_periodo_agg[
                'N_Reprovados'] = 0
            df_pdm_reprovacao_anual_periodo_agg['TaxaReprovacao'] = np.where(
                df_pdm_reprovacao_anual_periodo_agg['TotalAlunosPeriodo'] > 0,
                (df_pdm_reprovacao_anual_periodo_agg['N_Reprovados'] / df_pdm_reprovacao_anual_periodo_agg[
                    'TotalAlunosPeriodo'] * 100), 0).round(2)
            df_pdm_reprovacao_anual_periodo_agg['AnoPeriodo'] = df_pdm_reprovacao_anual_periodo_agg['Ano'].astype(
                str) + "." + df_pdm_reprovacao_anual_periodo_agg['Periodo'].astype(str)

            df_pdm_dependencia_anual_periodo_agg = pd.merge(df_total_situacao_periodo, df_depend_pdm_periodo,
                                                            on=['Ano', 'Periodo', 'Modalidade', 'StatusPDM'],
                                                            how='left').fillna(0)
            if 'N_Dependencia' not in df_pdm_dependencia_anual_periodo_agg.columns:
                df_pdm_dependencia_anual_periodo_agg['N_Dependencia'] = 0
                df_pdm_dependencia_anual_periodo_agg['TaxaDependencia'] = np.where(
                    df_pdm_dependencia_anual_periodo_agg['TotalAlunosPeriodo'] > 0,
                    (df_pdm_dependencia_anual_periodo_agg['N_Dependencia'] / df_pdm_dependencia_anual_periodo_agg[
                        'TotalAlunosPeriodo'] * 100), 0).round(2)
                df_pdm_dependencia_anual_periodo_agg['AnoPeriodo'] = df_pdm_dependencia_anual_periodo_agg['Ano'].astype(
                    str) + "." + df_pdm_dependencia_anual_periodo_agg['Periodo'].astype(str)

    if not df_desempenho_completo_pdm.empty and 'FrequenciaAluno' in df_desempenho_completo_pdm.columns and 'Ano' in df_desempenho_completo_pdm.columns:
        df_pdm_media_freq_anual_agg = df_desempenho_completo_pdm.groupby(['Ano', 'Modalidade', 'StatusPDM'])[
            'FrequenciaAluno'].mean().reset_index(name='MediaFrequencia')
        print("Média de Frequência Anual por Status PDM (2018-2024):\n", df_pdm_media_freq_anual_agg.head())

# --- Geração dos Gráficos ---
print("\nGerando gráficos históricos...")
if not df_todos_indicadores_historicos.empty:
    modalidades_historico = df_todos_indicadores_historicos['Modalidade'].unique()
    tipos_indicadores_historico = df_todos_indicadores_historicos['TipoIndicador'].unique()
    for mod in modalidades_historico:
        print(f"\n--- Modalidade (Histórico): {mod} ---")
        for indicador in tipos_indicadores_historico:
            print(f"  -- Indicador (Histórico): {indicador} --")
            plot_evolucao_geral(df_todos_indicadores_historicos, mod, indicador, OUTPUT_GRAPH_PATH)
            for regiao, campi_lista in CAMPUS_REGIAO_MAP.items():
                if not campi_lista: continue
                plot_evolucao_regional(df_todos_indicadores_historicos, mod, indicador, regiao, campi_lista,
                                       OUTPUT_GRAPH_PATH)
else:
    print("AVISO: Nenhum dado histórico agregado para gerar gráficos.")

# Gráficos PDM Anuais (2018-2024)
if not df_pdm_media_freq_anual_agg.empty:
    print("\nGerando gráficos de Média de Frequência Anual Comparativa PDM (2018-2024)...")
    for mod_pdm_freq in df_pdm_media_freq_anual_agg['Modalidade'].unique():
        plot_pdm_comparativo_anual(df_pdm_media_freq_anual_agg, mod_pdm_freq, 'MediaFrequencia', 'Média de Frequência',
                                   True, OUTPUT_GRAPH_PATH, x_col='Ano', x_label_text='Ano da Frequência')
else:
    print("AVISO: Nenhuma estatística de frequência anual PDM calculada para gerar gráficos.")

if not df_pdm_concluidos_anual_agg.empty:
    print("\nGerando gráficos de Contagem de Concluídos Anual Comparativa PDM (2018-2024)...")
    for mod_pdm_conc in df_pdm_concluidos_anual_agg['Modalidade'].unique():
        plot_pdm_comparativo_anual(df_pdm_concluidos_anual_agg, mod_pdm_conc, 'N_Concluidos', 'Nº de Concluídos', False,
                                   OUTPUT_GRAPH_PATH, x_col='Ano', x_label_text='Ano de Conclusão')
else:
    print("AVISO: Nenhuma estatística de concluídos anual PDM calculada para gerar gráficos.")

if not df_pdm_reprovacao_anual_periodo_agg.empty:
    print("\nGerando gráficos de Taxa de Reprovação Anual.Periodo Comparativa PDM (2018-2024)...")
    for mod_pdm_rep in df_pdm_reprovacao_anual_periodo_agg['Modalidade'].unique():
        plot_pdm_comparativo_anual(df_pdm_reprovacao_anual_periodo_agg, mod_pdm_rep, 'TaxaReprovacao',
                                   'Taxa de Reprovação', True, OUTPUT_GRAPH_PATH, x_col='AnoPeriodo',
                                   x_label_text='Ano.Período')
else:
    print("AVISO: Nenhuma estatística de reprovação anual.periodo PDM calculada para gerar gráficos.")

if not df_pdm_dependencia_anual_periodo_agg.empty:
    print("\nGerando gráficos de Taxa de Dependência Anual.Periodo Comparativa PDM (2018-2024)...")
    for mod_pdm_dep in df_pdm_dependencia_anual_periodo_agg['Modalidade'].unique():
        plot_pdm_comparativo_anual(df_pdm_dependencia_anual_periodo_agg, mod_pdm_dep, 'TaxaDependencia',
                                   'Taxa de Dependência', True, OUTPUT_GRAPH_PATH, x_col='AnoPeriodo',
                                   x_label_text='Ano.Período')
else:
    print("AVISO: Nenhuma estatística de dependência anual.periodo PDM calculada para gerar gráficos.")

print("\nProcessamento concluído! Gráficos salvos em:", OUTPUT_GRAPH_PATH)
