"""
MODULO DE VISUALIZACAO DE RESULTADOS
Gera mapas e relatorios da otimizacao
"""
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import os

# Import relativo correto
from config.settings import (COR_REDE_COMPLETA, COR_ROTA_OTIMIZADA, 
                            TAMANHO_PONTO, LARGURA_LINHA, PASTA_RESULTADOS,
                            NOME_MAPA, NOME_RELATORIO)

class Visualizador:
    def __init__(self):
        self.cor_rede = COR_REDE_COMPLETA
        self.cor_rota = COR_ROTA_OTIMIZADA
        self.tamanho_ponto = TAMANHO_PONTO
        self.largura_linha = LARGURA_LINHA
        self.pasta_resultados = PASTA_RESULTADOS
        
        os.makedirs(self.pasta_resultados, exist_ok=True)
    
    def criar_mapa_comparativo(self, grafo_original, arvore_otimizada, metricas, nome_bairro):
        print("Criando mapa comparativo...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        pos = {node: (data['x'], data['y']) for node, data in grafo_original.nodes(data=True)}
        
        self._plotar_grafo(ax1, grafo_original, pos, self.cor_rede, 
                          f"Malha Viaria Completa\n{len(grafo_original.nodes)} nos, {len(grafo_original.edges)} ruas")
        
        self._plotar_grafo(ax2, arvore_otimizada, pos, self.cor_rota,
                          f"Rota Otimizada\n{len(arvore_otimizada.edges)} ruas selecionadas")
        
        fig.suptitle(
            f'Otimizacao de Rotas de Coleta - {nome_bairro}\n'
            f'Economia: {metricas["economia_metros"]:.0f}m ({metricas["economia_percentual"]:.1f}%) - '
            f'Algoritmo: {metricas["algoritmo_utilizado"].upper()}',
            fontsize=16, 
            fontweight='bold'
        )
        
        plt.tight_layout()
        
        caminho_mapa = f"{self.pasta_resultados}/{NOME_MAPA}"
        plt.savefig(caminho_mapa, dpi=150, bbox_inches='tight')
        plt.show()
        
        print(f"Mapa salvo como: '{caminho_mapa}'")
    
    def _plotar_grafo(self, ax, grafo, pos, cor, titulo):
        nx.draw_networkx_edges(
            grafo, pos, ax=ax, 
            edge_color=cor, 
            width=self.largura_linha,
            alpha=0.7
        )
        
        nx.draw_networkx_nodes(
            grafo, pos, ax=ax,
            node_size=self.tamanho_ponto,
            node_color=cor,
            alpha=0.6
        )
        
        ax.set_title(titulo, fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        
        if pos:
            xs = [x for x, y in pos.values()]
            ys = [y for x, y in pos.values()]
            ax.set_xlim(min(xs) - 0.001, max(xs) + 0.001)
            ax.set_ylim(min(ys) - 0.001, max(ys) + 0.001)
    
    def gerar_relatorio_ruas(self, arvore_otimizada, nome_bairro):
        print("Gerando relatorio de ruas...")
        
        dados_ruas = []
        for u, v, data in arvore_otimizada.edges(data=True):
            dados_ruas.append({
                'Rua': data.get('name', f'Rua {u}-{v}'),
                'Comprimento (m)': int(data.get('length', 0)),
                'Comprimento (km)': round(data.get('length', 0) / 1000, 2),
                'Tipo de Via': data.get('highway', 'desconhecido').title(),
                'ID_OSM': data.get('osm_id', 'N/A')
            })
        
        df = pd.DataFrame(dados_ruas)
        df = df.sort_values('Comprimento (m)', ascending=False)
        
        caminho_relatorio = f"{self.pasta_resultados}/{NOME_RELATORIO}"
        df.to_csv(caminho_relatorio, index=False, encoding='utf-8')
        
        print(f"RESUMO DAS RUAS - {nome_bairro}:")
        print(f"Total de ruas na rota: {len(df)}")
        print(f"Extensao total: {df['Comprimento (m)'].sum():.0f}m ({df['Comprimento (km)'].sum():.2f}km)")
        print(f"Rua mais longa: {df.iloc[0]['Rua']} ({df.iloc[0]['Comprimento (m)']}m)")
        
        print(f"TOP 5 RUAS MAIS LONGAS:")
        print(df.head().to_string(index=False))
        
        print(f"Relatorio salvo como: '{caminho_relatorio}'")
        
        return df

    def gerar_relatorio_execucao(self, metricas, nome_bairro):
        print("\nRELATORIO FINAL DE EXECUCAO")
        print("=" * 50)
        print(f"BAIRRO: {nome_bairro}")
        print(f"ALGORITMO: {metricas['algoritmo_utilizado'].upper()}")
        print(f"TEMPO DE EXECUCAO: {metricas['tempo_execucao_segundos']:.3f}s")
        print(f"EXTENSAO TOTAL: {metricas['comprimento_total_metros']:.0f}m")
        print(f"EXTENSAO OTIMIZADA: {metricas['comprimento_otimizado_metros']:.0f}m")
        print(f"ECONOMIA: {metricas['economia_metros']:.0f}m ({metricas['economia_percentual']:.1f}%)")
        print(f"REDUCAO DE ROTAS: {metricas['numero_arestas_original']} -> {metricas['numero_arestas_otimizado']}")
        print("=" * 50)