import pandas as pd
import os

def unificar_planilhas_excel(caminho_pasta, arquivos_entrada, arquivo_saida):
    """
    Unifica várias planilhas Excel em uma única.

    Args:
        caminho_pasta (str): O caminho para a pasta onde as planilhas estão localizadas.
        arquivos_entrada (list): Uma lista de nomes dos arquivos Excel de entrada (ex: ['Relatorio18.xls', 'Relatorio19.xls']).
        arquivo_saida (str): O nome do arquivo Excel de saída consolidado (ex: 'Relatorio_Consolidado.xlsx').
    """
    lista_dataframes = []
    arquivos_encontrados = 0

    print(f"Iniciando o processo de unificação para os arquivos em '{caminho_pasta}'...")

    for nome_arquivo in arquivos_entrada:
        caminho_completo_arquivo = os.path.join(caminho_pasta, nome_arquivo)
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(caminho_completo_arquivo):
                print(f"AVISO: O arquivo '{nome_arquivo}' não foi encontrado em '{caminho_pasta}'. Pulando este arquivo.")
                continue

            # Lê a planilha. A engine 'xlrd' é necessária para arquivos .xls
            # Se os seus arquivos .xls tiverem múltiplas abas e você quiser uma específica,
            # use o parâmetro sheet_name='nome_da_aba' ou sheet_name=0 (para a primeira aba)
            df = pd.read_excel(caminho_completo_arquivo, engine='xlrd')
            lista_dataframes.append(df)
            print(f"Arquivo '{nome_arquivo}' lido com sucesso.")
            arquivos_encontrados += 1
        except FileNotFoundError:
            print(f"ERRO: O arquivo '{nome_arquivo}' não foi encontrado no caminho especificado: '{caminho_completo_arquivo}'. Verifique o nome e o caminho.")
        except Exception as e:
            print(f"ERRO ao ler o arquivo '{nome_arquivo}': {e}")

    if not lista_dataframes:
        print("Nenhum dado foi lido. Verifique se os arquivos existem e estão no formato correto.")
        return

    # Concatena todos os DataFrames da lista em um único DataFrame
    # ignore_index=True garante que o índice do DataFrame consolidado seja contínuo
    df_consolidado = pd.concat(lista_dataframes, ignore_index=True)
    print(f"\nForam lidos e processados {arquivos_encontrados} arquivos.")

    # Define o caminho completo para o arquivo de saída
    caminho_completo_saida = os.path.join(caminho_pasta, arquivo_saida)

    try:
        # Salva o DataFrame consolidado em um novo arquivo Excel (.xlsx)
        # index=False evita que o índice do DataFrame seja escrito como uma coluna na planilha
        df_consolidado.to_excel(caminho_completo_saida, index=False, engine='openpyxl')
        print(f"\nPlanilhas unificadas com sucesso! O arquivo consolidado foi salvo como '{caminho_completo_saida}'.")
    except Exception as e:
        print(f"ERRO ao salvar o arquivo consolidado '{arquivo_saida}': {e}")

# --- Configuração ---
# Especifique o caminho para a pasta onde seus arquivos Excel estão localizados.
# Se o script estiver na mesma pasta que as planilhas, você pode usar "."
PASTA_DAS_PLANILHAS = "/Users/fred/Downloads/" # Exemplo: "C:/Users/SeuUsuario/Documentos/Relatorios"

# Lista dos nomes dos arquivos de entrada
NOMES_ARQUIVOS_ENTRADA = [f"Relatorio{ano}.xls" for ano in range(18, 25)] # Gera Relatorio18.xls até Relatorio24.xls

# Nome do arquivo de saída
NOME_ARQUIVO_SAIDA = "Relatorio_Consolidado.xlsx"

# --- Execução ---
if __name__ == "__main__":
    # Verifica se a pasta especificada existe
    if not os.path.isdir(PASTA_DAS_PLANILHAS):
        print(f"ERRO: A pasta especificada '{PASTA_DAS_PLANILHAS}' não existe. Verifique o caminho.")
    else:
        unificar_planilhas_excel(PASTA_DAS_PLANILHAS, NOMES_ARQUIVOS_ENTRADA, NOME_ARQUIVO_SAIDA)

