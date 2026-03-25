import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAÇÕES VISUAIS ---
plt.style.use('ggplot') # Deixa os gráficos com visual moderno

def carregar_dados(caminho_arquivo):
    """Lê o arquivo CSV e prepara os dados."""
    try:
        df = pd.read_csv(caminho_arquivo)
        
        # Cálculo da média por disciplina (arredondado para 1 casa decimal)
        df['Media'] = df[['Nota1', 'Nota2', 'Nota3']].mean(axis=1).round(1)
        
        # Definição da Situação
        def calcular_situacao(media):
            if media >= 7: return "Aprovado"
            elif media >= 5: return "Recuperação"
            else: return "Reprovado"
            
        df['Situacao'] = df['Media'].apply(calcular_situacao)
        return df
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None

def gerar_graficos(aluno_df, nome_aluno):
    """Gera visualizações de desempenho para o aluno selecionado."""
    
    # Criando uma figura com dois subplots (1 linha, 2 colunas)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle(f'Análise de Desempenho: {nome_aluno}', fontsize=16, fontweight='bold')

    # 1. Gráfico de Barras - Médias por Disciplina
    cores = ['green' if m >= 7 else 'orange' if m >= 5 else 'red' for m in aluno_df['Media']]
    ax1.bar(aluno_df['Disciplina'], aluno_df['Media'], color=cores, edgecolor='black')
    ax1.axhline(y=7, color='blue', linestyle='--', label='Média Escolar (7.0)')
    ax1.set_title('Médias por Disciplina')
    ax1.set_ylim(0, 10)
    ax1.legend()

    # 2. Gráfico de Pizza - Distribuição de Situação
    contagem = aluno_df['Situacao'].value_counts()
    ax2.pie(contagem, labels=contagem.index, autopct='%1.1f%%', startangle=140, 
            colors=['#4CAF50', '#FFC107', '#F44336'])
    ax2.set_title('Status Geral das Disciplinas')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def main():
    arquivo = 'dados.csv'
    df = carregar_dados(arquivo)
    
    if df is not None:
        print("="*30)
        print(" SISTEMA DE BOLETIM ESCOLAR ")
        print("="*30)
        
        while True:
            alunos_disponiveis = df['Aluno'].unique()
            print(f"\nAlunos no sistema: {', '.join(alunos_disponiveis)}")
            
            nome = input("Digite o nome do aluno (ou 'sair'): ").strip().capitalize()
            
            if nome.lower() == 'sair':
                print("Encerrando sistema...")
                break
                
            aluno_df = df[df['Aluno'] == nome]
            
            if not aluno_df.empty:
                print(f"\nResultados para {nome}:")
                print(aluno_df[['Disciplina', 'Media', 'Situacao']].to_string(index=False))
                
                # Estatísticas Gerais
                media_geral = aluno_df['Media'].mean()
                print(f"\n>>> Média Geral: {media_geral:.2f}")
                
                gerar_graficos(aluno_df, nome)
            else:
                print(f"Aviso: Aluno '{nome}' não encontrado.")

if __name__ == "__main__":
    main()