# Import necessary libraries
import pandas as pd
import io
import re
# Make sure openpyxl is available for Excel writing, pandas usually requires it.
# If running locally and it's not installed, you might need: pip install openpyxl

# --- Configuration ---
# Define the input filename accurately. Make sure this matches the file in your directory.
# Using the name from the successful read attempt in your log.
input_filename = "/Users/fred/Downloads/Relatorio_docentes.csv" # Adjusted based on your log
output_filename = '/Users/fred/Downloads/resumo_professores_linguas.xlsx' # Output Excel file

# --- Read the CSV file ---
df = None # Initialize DataFrame as None
read_successful = False # Flag to track if reading worked

# Try reading with semicolon separator first (common in Brazil/Portugal CSVs)
try:
    # Try UTF-8 encoding first with semicolon
    print(f"Tentando ler '{input_filename}' com separador ';' e encoding 'utf-8'...")
    df = pd.read_csv(input_filename, sep=';', encoding='utf-8')
    print("Arquivo lido com sucesso (separador ';', encoding 'utf-8').")
    read_successful = True
except FileNotFoundError:
    print(f"Erro Crítico: Arquivo '{input_filename}' não encontrado no diretório.")
except Exception as e:
    print(f"Falha ao ler com separador ';' e encoding 'utf-8': {e}")
    # If UTF-8 fails, try latin1 with semicolon
    try:
        print(f"Tentando ler '{input_filename}' com separador ';' e encoding 'latin1'...")
        df = pd.read_csv(input_filename, sep=';', encoding='latin1')
        print("Arquivo lido com sucesso (separador ';', encoding 'latin1').")
        read_successful = True
    except Exception as e2:
        print(f"Falha ao ler com separador ';' e encoding 'latin1': {e2}")

# If reading with semicolon failed, try with comma separator (standard default)
if not read_successful:
    print("\nTentando ler com separador ',' (vírgula)...")
    try:
        # Try UTF-8 encoding first with comma
        print(f"Tentando ler '{input_filename}' com separador ',' e encoding 'utf-8'...")
        df = pd.read_csv(input_filename, sep=',', encoding='utf-8')
        print("Arquivo lido com sucesso (separador ',', encoding 'utf-8').")
        read_successful = True
    except Exception as e:
        print(f"Falha ao ler com separador ',' e encoding 'utf-8': {e}")
        # If UTF-8 fails, try latin1 with comma
        try:
            print(f"Tentando ler '{input_filename}' com separador ',' e encoding 'latin1'...")
            df = pd.read_csv(input_filename, sep=',', encoding='latin1')
            print("Arquivo lido com sucesso (separador ',', encoding 'latin1').")
            read_successful = True
        except Exception as e2:
            print(f"Falha ao ler com separador ',' e encoding 'latin1': {e2}")
            # Add a check for the specific tokenizing error to give a hint
            if "Error tokenizing data" in str(e) or "Error tokenizing data" in str(e2):
                 print("\nDica: O erro 'tokenizing data' frequentemente indica que o separador (sep=',' ou sep=';') está incorreto ou há problemas de formatação no arquivo CSV (ex: aspas desbalanceadas, número incorreto de colunas em algumas linhas). Verifique a linha mencionada no erro no arquivo original.")


# Proceed only if the DataFrame was loaded successfully
if read_successful and df is not None:
    print("\nLeitura do arquivo concluída. Iniciando processamento dos dados...")
    # --- Standardize column names ---
    # Convert to lowercase, replace spaces and hyphens with underscores
    original_columns = df.columns.tolist() # Keep original for reference if needed
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    standardized_columns = df.columns.tolist()
    print(f"Colunas originais: {original_columns}")
    print(f"Colunas após padronização: {standardized_columns}")

    # --- Identify relevant columns (CORRECTED based on your log) ---
    # Use the standardized names identified from your file's columns
    col_area = 'disciplina_de_ingresso'
    col_titulacao = 'titulação' # Standardized from 'Titulação'
    col_habilitacao = 'formação___nome_do_curso_superior' # Standardized from 'Formação - Nome do Curso Superior'

    # --- Verify if these columns exist AFTER standardization ---
    required_cols = [col_area, col_titulacao, col_habilitacao]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"\nErro Crítico: Colunas necessárias não encontradas após padronização: {missing_cols}.")
        print(f"Colunas padronizadas disponíveis: {df.columns.tolist()}")
        print(f"Verifique se os nomes '{col_area}', '{col_titulacao}', '{col_habilitacao}' realmente existem na lista acima.")
        df = None # Indicate failure to prevent further processing

# Proceed only if essential columns exist
if df is not None:
    print("Colunas essenciais encontradas. Prosseguindo com a análise...")
    # --- Define language keywords ---
    languages = {
        'Inglês': r'ingles|inglês',
        'Espanhol': r'espanhol',
        'Francês': r'frances|francês',
        'Libras': r'libras'
    }

    # --- Filter for language teachers ---
    # Apply filter using the CORRECTED area column name
    df['lingua'] = None
    if col_area in df.columns:
         # Convert to string before applying string methods to avoid errors on non-string data
         mask = df[col_area].astype(str).str.contains('|'.join(languages.values()), case=False, na=False)
         # Assign language based on which pattern matched (more robust approach)
         for lang, pattern in languages.items():
             lang_mask = df[col_area].astype(str).str.contains(pattern, case=False, na=False)
             df.loc[mask & lang_mask & df['lingua'].isna(), 'lingua'] = lang # Assign only if not already assigned
    else:
         # This case should not happen due to the check above, but kept for safety
         print(f"Aviso: Coluna '{col_area}' não encontrada para filtrar línguas.")

    df_languages = df.dropna(subset=['lingua']).copy()
    print(f"Encontrados {len(df_languages)} registros de professores de línguas.")

    # --- Analyze and Group Data ---
    summary = []
    if not df_languages.empty:
        # Use the CORRECTED column names for grouping and analysis
        grouped = df_languages.groupby('lingua')
        for language, group in grouped:
            num_teachers = len(group)

            # Titulações
            titulacoes = []
            if col_titulacao in group.columns:
                titulacoes = group[col_titulacao].dropna().unique().tolist()
                titulacoes.sort()
            else:
                # Should not happen if check passed, but good practice
                print(f"Aviso: Coluna de titulação '{col_titulacao}' inesperadamente ausente no grupo '{language}'.")

            # Habilitações
            habilitacoes_details = []
            if col_habilitacao in group.columns:
                habilitacoes_list = group[col_habilitacao].dropna().unique().tolist()
                habilitacoes_list.sort()
                for hab in habilitacoes_list:
                    hab_lower = str(hab).lower()
                    lang_lower = language.lower()
                    tipo = "Não especificado/Outra" # Default type

                    # Refined check for dual/simple majors
                    is_dual_portuguese = re.search(r'portugues|português', hab_lower)
                    # Look for separators or common conjunctions indicating multiple subjects
                    has_separator_or_conjunction = re.search(r'[/ e ]| com ', hab_lower)
                    mentions_language = lang_lower in hab_lower

                    if mentions_language:
                        if is_dual_portuguese:
                             tipo = f"Dupla ({language}/Português)"
                        elif has_separator_or_conjunction:
                             # Check if it mentions another known language or seems complex
                             other_langs = [l for l_key, l_pattern in languages.items() if l_key != language and re.search(l_pattern, hab_lower, re.IGNORECASE)]
                             # Simple heuristic: more than 3 words might indicate complexity/dual, or another language found
                             if other_langs or len(re.findall(r'\b\w+\b', hab_lower)) > 3:
                                 tipo = "Dupla/Outra Combinação"
                             else:
                                 # Assume simple if only language + separator/conjunction and few words
                                 tipo = f"Simples (Letras {language})"
                        else:
                             # Only language mentioned, no Portuguese, no separator/conjunction
                             tipo = f"Simples (Letras {language})"
                    # Keep default "Não especificado/Outra" if language not mentioned or logic doesn't fit

                    habilitacoes_details.append(f"{hab} ({tipo})")
            else:
                 # Should not happen if check passed
                 print(f"Aviso: Coluna de habilitação '{col_habilitacao}' inesperadamente ausente no grupo '{language}'.")


            summary.append({
                'Língua': language,
                'Número de Professores': num_teachers,
                'Titulações (Tipos)': ', '.join(titulacoes) if titulacoes else 'Nenhuma encontrada ou coluna ausente',
                'Habilitações (Tipos e Classificação)': '; '.join(habilitacoes_details) if habilitacoes_details else 'Nenhuma encontrada ou coluna ausente'
            })
    else:
        print("Nenhum professor de línguas encontrado com base nos critérios e coluna de área.")

    # --- Create Summary DataFrame ---
    df_summary = pd.DataFrame(summary)

    # --- Generate Excel file ---
    if not df_summary.empty:
        try:
            df_summary.to_excel(output_filename, index=False, engine='openpyxl')
            print(f"\nArquivo Excel '{output_filename}' gerado com sucesso.")
        except ImportError:
            print("\nErro Crítico: A biblioteca 'openpyxl' é necessária para gerar arquivos .xlsx.")
            print("Por favor, instale-a (ex: pip install openpyxl) se estiver executando localmente.")
            output_filename = None
        except Exception as e:
            print(f"\nErro ao gerar o arquivo Excel: {e}")
            output_filename = None

        # Display the summary table as well if generated
        if output_filename:
            print("\nResumo dos Professores de Línguas:")
            try:
              # Try to display nicely if possible (e.g., in Jupyter environments)
              from IPython.display import display
              display(df_summary)
            except ImportError:
              # Fallback to plain text print
              print(df_summary.to_string(index=False))
    else:
        print("\nNenhum dado de resumo para gerar o arquivo Excel.")


elif not read_successful:
     # This message is shown if reading failed initially
     print(f"\nNão foi possível ler o arquivo '{input_filename}' com nenhuma das configurações tentadas.")
     print("Verifique se o arquivo existe no local esperado, se o nome está correto, se não está corrompido e se o separador/codificação estão corretos.")

# Final message if processing failed after successful read (e.g., missing columns)
elif df is None:
    print("\nProcessamento interrompido devido a erro na verificação das colunas necessárias.")

