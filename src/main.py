"""
SISTEMA COMPLETO DE OTIMIZAÇÃO DE ROTAS - MONTES CLAROS
Script principal que orquestra todo o processo
"""
from data.collector import ColetorDados
from models.optimizer import OtimizadorRotas
from utils.visualizer import Visualizador
from config.settings import BAIRRO_FOCO, CIDADE

def main():
    print(" SISTEMA DE OTIMIZAÇÃO DE ROTAS DE COLETA")
    print("=" * 60)
    print(f" FOCO: {BAIRRO_FOCO} - {CIDADE}")
    print("=" * 60)
    
    # PASSO 1: Coletar dados reais
    print("\n1️⃣  FASE 1: COLETA DE DADOS")
    print("-" * 40)
    
    coletor = ColetorDados()
    grafo_original = coletor.obter_grafo_bairro(BAIRRO_FOCO)
    
    if not grafo_original:
        print(" Não foi possível obter dados reais. Encerrando.")
        return
    
    # PASSO 2: Otimizar rotas
    print("\n2️⃣  FASE 2: OTIMIZAÇÃO DE ROTAS")
    print("-" * 40)
    
    otimizador = OtimizadorRotas()
    grafo_preparado = otimizador.preparar_grafo(grafo_original)
    arvore_otimizada, metricas = otimizador.calcular_rota_otimizada(grafo_preparado)
    
    if not arvore_otimizada:
        print(" Falha na otimização. Encerrando.")
        return
    
    # PASSO 3: Visualizar resultados
    print("\n FASE 3: VISUALIZAÇÃO DE RESULTADOS")
    print("-" * 40)
    
    visualizador = Visualizador()
    
    # Gerar mapa comparativo
    visualizador.criar_mapa_comparativo(grafo_preparado, arvore_otimizada, metricas, BAIRRO_FOCO)
    
    # Gerar relatório de ruas
    visualizador.gerar_relatorio_ruas(arvore_otimizada, BAIRRO_FOCO)
    
    # Relatório final
    visualizador.gerar_relatorio_execucao(metricas, BAIRRO_FOCO)
    
    print("\n PROJETO CONCLUÍDO COM SUCESSO!")
    print(" Verifique os arquivos na pasta 'resultados/'")

if __name__ == "__main__":
    main()