import chardet
import pandas as pd

def detectar_codificacao(arquivo):
    """Detecta a codificação de um arquivo lendo uma amostra inicial."""
    with open(arquivo, "rb") as f:
        resultado = chardet.detect(f.read(10000))  # Lê os primeiros 10.000 bytes
    return resultado["encoding"]

def converter_csv(arquivo_entrada, arquivo_saida, codificacao_destino):
    """Converte o CSV para a codificação desejada."""
    codificacao_origem = detectar_codificacao(arquivo_entrada)
    print(f"Codificação detectada: {codificacao_origem}")

    # Carregar o CSV com a codificação detectada
    df = pd.read_csv(arquivo_entrada, encoding=codificacao_origem)

    # Salvar com a nova codificação
    df.to_csv(arquivo_saida, encoding=codificacao_destino, index=False)
    print(f"Arquivo salvo como {arquivo_saida} com codificação {codificacao_destino}")

if __name__ == "__main__":
    arquivo_entrada = input("Digite o caminho do arquivo CSV: ")
    codificacao_origem = detectar_codificacao(arquivo_entrada)
    print(f"A codificação detectada é: {codificacao_origem}")

    # Solicitar codificação de destino
    codificacao_destino = input("Digite a codificação de destino (ex: utf-8, iso-8859-1, utf-16): ")

    # Definir nome do arquivo de saída
    arquivo_saida = arquivo_entrada.replace(".csv", f"_{codificacao_destino}.csv")

    # Converter o arquivo
    converter_csv(arquivo_entrada, arquivo_saida, codificacao_destino)
