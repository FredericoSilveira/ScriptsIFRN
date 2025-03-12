import pandas as pd
import re
import unicodedata
from rapidfuzz import process, fuzz


# Função para remover acentuação
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


# Função para normalizar o nome da escola, removendo acentuação, pontuação e substituindo abreviações
def normalize_school_name(school_name):
    if pd.isna(school_name):
        return ''

    # Tornar tudo minúsculo
    normalized = school_name.lower()

    # Remover acentuação
    normalized = remove_accents(normalized)

    # Substituições de abreviações por nomes completos (apenas isoladas)
    substitutions = {
        r'\besc\b\.?': 'escola',
        r'\bmun\b\.?': 'municipal',
        r'\bmul\b\.?': 'municipal',
        r'\best\b\.?': 'estadual',
        r'\bfed\b\.?': 'federal',
        r'\befed\b\.?': 'escola federal',
        r'\bprof\b\.?': 'professor',
        r'\bcaic\b': 'centro de atencao integral a crianca',
        r'\bce\b\.?': 'centro de educacao',
        r'\bc e\b': 'centro de educacao',
        r'\bc.e.\b': 'centro de educacao',
        r'\bc. e.\b': 'centro de educacao',
        r'\bem\b\.?': 'escola municipal',
        r'\be m\b\.?': 'escola municipal',
        r'\be.m.\b\.?': 'escola municipal',
        r'\be. m.\b\.?': 'escola municipal',
        r'\bcol\b\.?': 'colegio',
        r'\bdr\b\.?': 'doutor',
        r'\bee\b\.?': 'escola estadual',
        r'\be e\b\.?': 'escola estadual',
        r'\be.e.\b\.?': 'escola estadual',
        r'\be. e.\b\.?': 'escola estadual',
        r'\bef\b\.?': 'escola federal',
        r'\be f\b\.?': 'escola federal',
        r'\be.f.\b\.?': 'escola federal',
        r'\be. f.\b\.?': 'escola federal'
    }

    # Aplicar substituições com regex
    for abbr, full in substitutions.items():
        normalized = re.sub(abbr, full, normalized)

    # Remover pontuação e caracteres especiais
    normalized = re.sub(r'[^\w\s]', '', normalized)

    # Remover espaços extras
    normalized = " ".join(normalized.split())

    return normalized


# Função para remover termos duplicados
def remove_repeated_terms(school_name):
    # Lista de termos que devem ser únicos
    unique_terms = ['escola', 'municipal', 'estadual', 'federal', 'professor', 'centro de atencao integral a crianca',
                    'centro de educacao', 'colegio', 'doutor']

    # Remover repetições dos termos substituídos
    for term in unique_terms:
        pattern = r'\b({})\b(\s+\1\b)+'.format(re.escape(term))  # Detectar repetições consecutivas
        school_name = re.sub(pattern, r'\1', school_name)

    return school_name


# Carregar o arquivo Excel
file_path = '/Users/fred/Downloads/ESCOLAS-CORRELACAO-SUAP-MEC.xlsx'
data = pd.read_excel(file_path)

# Criar as colunas normalizadas para SUAP e MEC
data['SUAP Normal'] = data['SUAP'].apply(normalize_school_name)
data['MEC Normal'] = data['MEC'].apply(normalize_school_name)

# Remover os termos repetidos nas colunas normalizadas
data['SUAP Normal'] = data['SUAP Normal'].apply(remove_repeated_terms)
data['MEC Normal'] = data['MEC Normal'].apply(remove_repeated_terms)

# Exibir as primeiras linhas para verificar a normalização
print(data[['SUAP', 'MEC', 'SUAP Normal', 'MEC Normal']].head())

# Agora fazemos a comparação entre SUAP Normal e MEC Normal
similarity_percentages = []
names_equal = []
best_match_index = []

# Iterar sobre a coluna SUAP Normal
for suap_school in data['SUAP Normal']:
    # Encontrar o melhor resultado de correspondência na coluna MEC Normal
    best_match, best_match_score, best_match_row = process.extractOne(suap_school, data['MEC Normal'],
                                                                      scorer=fuzz.token_sort_ratio)

    # Armazenar o percentual de similaridade
    similarity_percentages.append(best_match_score)

    # Verificar se a similaridade é maior ou igual a 90%
    names_equal.append("Sim" if best_match_score >= 90 else "Não")

    # Armazenar a linha da correspondência (1-indexada)
    best_match_index.append(data[data['MEC Normal'] == best_match].index[0] + 1)

# Adicionar os resultados como novas colunas no dataframe
data['Percentual de Semelhança'] = similarity_percentages
data['Nomes Iguais (>=90%)'] = names_equal
data['Melhor Linha MEC'] = best_match_index

# Filtrar os dados com similaridade maior ou igual a 90%
data_90_or_more = data[data['Percentual de Semelhança'] >= 90]

# Filtrar os dados com similaridade entre 75% e 90%
data_between_75_and_90 = data[(data['Percentual de Semelhança'] >= 75) & (data['Percentual de Semelhança'] < 90)]

# Exportar as duas planilhas
data_90_or_more.to_excel('/Users/fred/Downloads/comparacao_escolas_90_ou_mais.xlsx', index=False)
data_between_75_and_90.to_excel('/Users/fred/Downloads/comparacao_escolas_75_a_90.xlsx', index=False)

# Exibir a confirmação da exportação
print("As planilhas foram exportadas com sucesso!")
