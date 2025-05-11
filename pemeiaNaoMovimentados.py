import pandas as pd
import os  # Importar o módulo os para manipulação de caminhos


def encontrar_estudantes_nao_movimentados(arquivo_registrados,
                                          coluna_cpf_registrados,
                                          arquivo_movimentados,
                                          coluna_cpf_movimentados,
                                          arquivo_saida):
    """
    Identifica estudantes registrados que não foram movimentados e salva em um novo arquivo Excel.

    Args:
        arquivo_registrados (str): Caminho completo para a planilha Excel de estudantes registrados.
        coluna_cpf_registrados (str): Nome da coluna contendo o CPF na planilha de registrados.
        arquivo_movimentados (str): Caminho completo para a planilha Excel de estudantes movimentados.
        coluna_cpf_movimentados (str): Nome da coluna contendo o CPF na planilha de movimentados.
        arquivo_saida (str): Caminho completo para o arquivo Excel de saída dos estudantes não movimentados.
    """
    try:
        # Ler a planilha de estudantes registrados
        # dtype={coluna_cpf_registrados: str} garante que o CPF seja lido como texto
        print(f"Tentando ler a planilha de registrados: '{arquivo_registrados}'...")
        df_registrados = pd.read_excel(arquivo_registrados, dtype={coluna_cpf_registrados: str})
        print(f"Lidos {len(df_registrados)} registros da planilha de registrados.")

        # Ler a planilha de estudantes movimentados
        # dtype={coluna_cpf_movimentados: str} garante que o CPF seja lido como texto
        print(f"Tentando ler a planilha de movimentados: '{arquivo_movimentados}'...")
        df_movimentados = pd.read_excel(arquivo_movimentados, dtype={coluna_cpf_movimentados: str})
        print(f"Lidos {len(df_movimentados)} registros da planilha de movimentados.")

        # Verificar se as colunas de CPF existem
        if coluna_cpf_registrados not in df_registrados.columns:
            print(
                f"ERRO: A coluna '{coluna_cpf_registrados}' não foi encontrada na planilha de registrados ('{os.path.basename(arquivo_registrados)}').")
            print(f"Colunas disponíveis: {df_registrados.columns.tolist()}")
            return
        if coluna_cpf_movimentados not in df_movimentados.columns:
            print(
                f"ERRO: A coluna '{coluna_cpf_movimentados}' não foi encontrada na planilha de movimentados ('{os.path.basename(arquivo_movimentados)}').")
            print(f"Colunas disponíveis: {df_movimentados.columns.tolist()}")
            return

        # Remover espaços em branco extras dos CPFs e garantir que sejam strings
        # Tratar CPFs ausentes (NaN) convertendo para string vazia antes do strip
        df_registrados[coluna_cpf_registrados] = df_registrados[coluna_cpf_registrados].fillna('').astype(
            str).str.strip()
        df_movimentados[coluna_cpf_movimentados] = df_movimentados[coluna_cpf_movimentados].fillna('').astype(
            str).str.strip()

        # Remover CPFs duplicados da planilha de movimentados para otimizar a busca,
        # mantendo a primeira ocorrência (não afeta a lógica de "não encontrado")
        df_movimentados = df_movimentados.drop_duplicates(subset=[coluna_cpf_movimentados])

        # Converter a coluna de CPFs dos movimentados para um conjunto (set) para busca rápida
        cpfs_movimentados = set(df_movimentados[coluna_cpf_movimentados])
        # Remover string vazia do conjunto se existir, para não dar falso positivo
        cpfs_movimentados.discard('')

        # Filtrar os estudantes registrados que NÃO estão na lista de CPFs movimentados
        # A função lambda verifica se o CPF de cada linha em df_registrados não está presente em cpfs_movimentados
        # Também ignora linhas onde o CPF do registrado é uma string vazia
        df_nao_movimentados = df_registrados[
            (~df_registrados[coluna_cpf_registrados].isin(cpfs_movimentados)) &
            (df_registrados[coluna_cpf_registrados] != '')
            ].copy()

        # .copy() é usado para evitar SettingWithCopyWarning, garantindo que estamos trabalhando com uma nova cópia do DataFrame

        if df_nao_movimentados.empty:
            print(
                "Nenhum estudante não movimentado encontrado (considerando CPFs válidos). Todos os registrados com CPF preenchido foram movimentados ou não possuem CPF na planilha de registrados.")
        else:
            # Salvar o resultado em um novo arquivo Excel
            df_nao_movimentados.to_excel(arquivo_saida, index=False)
            print(f"\nPlanilha de estudantes não movimentados salva como '{arquivo_saida}'.")
            print(f"Total de estudantes não movimentados: {len(df_nao_movimentados)}")

    except FileNotFoundError as e:
        print(f"ERRO: Arquivo não encontrado. Verifique o nome e o caminho do arquivo: {e.filename}")
        print(f"O script esperava encontrar o arquivo em: {os.path.abspath(e.filename)}")
    except KeyError as e:
        # Este erro é mais provável de ser pego pelas verificações de coluna acima, mas mantido por segurança.
        print(f"ERRO: Coluna não encontrada. Verifique os nomes das colunas de CPF: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("--- Script para Identificar Estudantes Não Movimentados ---")

    # Define o caminho base para os arquivos
    BASE_PATH = "/Users/fred/Downloads/"
    print(f"INFO: O script irá procurar os arquivos de entrada e salvar o arquivo de saída em: '{BASE_PATH}'")

    # Solicitar os NOMES dos arquivos e colunas ao usuário
    nome_arquivo_registrados_input = input(
        f"Digite o NOME do arquivo Excel de estudantes REGISTRADOS (ex: registrados.xlsx) que está em '{BASE_PATH}': ")
    coluna_cpf_registrados_input = input(
        f"Digite o nome da coluna de CPF na planilha '{nome_arquivo_registrados_input}': ")

    nome_arquivo_movimentados_input = input(
        f"Digite o NOME do arquivo Excel de estudantes MOVIMENTADOS (ex: movimentados.xlsx) que está em '{BASE_PATH}': ")
    coluna_cpf_movimentados_input = input(
        f"Digite o nome da coluna de CPF na planilha '{nome_arquivo_movimentados_input}': ")

    # Montar os caminhos completos dos arquivos
    arquivo_registrados_completo = os.path.join(BASE_PATH, nome_arquivo_registrados_input)
    arquivo_movimentados_completo = os.path.join(BASE_PATH, nome_arquivo_movimentados_input)

    nome_arquivo_saida = "nao_movimentados.xlsx"
    arquivo_saida_completo = os.path.join(BASE_PATH, nome_arquivo_saida)

    print("\nProcessando os dados...")
    encontrar_estudantes_nao_movimentados(
        arquivo_registrados_completo,
        coluna_cpf_registrados_input,
        arquivo_movimentados_completo,
        coluna_cpf_movimentados_input,
        arquivo_saida_completo
    )

    print("\n--- Fim do Script ---")
