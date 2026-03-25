import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. CRIAÇÃO AUTOMÁTICA DOS DADOS ---
def inicializar_arquivos():
    """Cria o arquivo CSV caso ele não exista, para o projeto rodar de primeira."""
    if not os.path.exists('dados.csv'):
        conteudo = """Aluno,Disciplina,Nota1,Nota2,Nota3
Ana,Matematica,8.5,7.0,9.0
Ana,Portugues,6.0,5.5,6.5
Ana,Historia,9.5,8.0,10.0
Bruno,Matematica,4.0,5.0,3.5
Bruno,Portugues,7.5,8.0,7.0
Bruno,Historia,5.0,6.0,5.5
Carlos,Matematica,9.0,9.5,10.0
Carlos,Portugues,8.0,7.0,9.0
"""
        with open('dados.csv', 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print("✅ Arquivo 'dados.csv' criado com sucesso!")

# --- 2. LÓGICA DE PROCESSAMENTO ---
def processar_boletim():
    inicializar_arquivos()
    df = pd.read_csv('dados.csv')
    
    # Cálculo da Média e Situação
    df['Media'] = df[['Nota1', 'Nota2', 'Nota3']].mean(axis=1).round(1)
    
    def status(m):
        if m >= 7: return "Aprovado"
        elif m >= 5: return "Recuperação"
        else: return "Reprovado"
        
    df['Situacao'] = df['Media'].apply(status)
    return df

# --- 3. PARTE VISUAL (GRÁFICOS) ---
def gerar_relatorio_visual(df_aluno, nome_aluno):
    plt.style.use('seaborn-v0_8-muted') # Estilo moderno
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle(f'Relatório Acadêmico: {nome_aluno}', fontsize=16, fontweight='bold')

    # Gráfico de Barras
    cores = ['#2ecc71' if s == "Aprovado" else '#f1c40f' if s == "Recuperação" else '#e74c3c' 
             for s in df_aluno['Situacao']]
    
    ax1.bar(df_aluno['Disciplina'], df_aluno['Media'], color=cores, edgecolor='black')
    ax1.axhline(y=7, color='blue', linestyle='--', alpha=0.6, label='Média de Aprovação')
    ax1.set_title('Notas por Matéria')
    ax1.set_ylim(0, 10)
    ax1.legend()

    # Gráfico de Pizza
    counts = df_aluno['Situacao'].value_counts()
    ax2.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, shadow=True)
    ax2.set_title('Distribuição de Resultados')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# --- 4. MENU DE INTERAÇÃO ---
def menu():
    df = processar_boletim()
    
    while True:
        print("\n" + "="*40)
        print(f"{'SISTEMA DE NOTAS ESCOLARES':^40}")
        print("="*40)
        print(f"Alunos disponíveis: {', '.join(df['Aluno'].unique())}")
        
        escolha = input("\nDigite o nome do aluno para analisar (ou 'SAIR'): ").strip().capitalize()
        
        if escolha.upper() == 'SAIR':
            print("Encerrando... Até logo!")
            break
            
        dados_aluno = df[df['Aluno'] == escolha]
        
        if not dados_aluno.empty:
            print(f"\n📊 Resultados de {escolha}:")
            print("-" * 30)
            print(dados_aluno[['Disciplina', 'Media', 'Situacao']].to_string(index=False))
            print("-" * 30)
            print(f"MÉDIA GERAL: {dados_aluno['Media'].mean():.2f}")
            
            gerar_relatorio_visual(dados_aluno, escolha)
        else:
            print(f"❌ Aluno '{escolha}' não encontrado no sistema.")

if __name__ == "__main__":
    menu()