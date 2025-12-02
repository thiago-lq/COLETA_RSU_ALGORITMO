"""
MODULO DE ALGORITMOS DE OTIMIZACAO
Implementa Prim para arvore geradora minima (coleta de lixo)
"""
import networkx as nx
import time

# Import relativo correto - DOIS níveis acima
from config.settings import ALGORITMO, PESO_PADRAO

class OtimizadorRotas:
    def __init__(self):
        self.algoritmo = ALGORITMO
        self.peso = PESO_PADRAO
        print(f"Otimizador configurado: {self.algoritmo.upper()}")
    
    def preparar_grafo(self, grafo):
        """
        Prepara o grafo para os algoritmos de otimizacao
        """
        print("Preparando grafo para otimizacao...")

        # 1. Converter para nao-direcionado se necessario
        if grafo.is_directed():
            grafo = grafo.to_undirected()
            print("Convertido para grafo nao-direcionado")
        
        # 2. Garantir que todas arestas tem peso
        arestas_sem_peso = 0
        for u, v, data in grafo.edges(data=True):
            if self.peso not in data or data[self.peso] <= 0:
                data[self.peso] = 100.0
                arestas_sem_peso += 1
        
        if arestas_sem_peso > 0:
            print(f"{arestas_sem_peso} arestas receberam peso padrao")
        
        # 3. Extrair maior componente conexo
        if not nx.is_connected(grafo):
            componentes = list(nx.connected_components(grafo))
            maior_componente = max(componentes, key=len)
            grafo = grafo.subgraph(maior_componente).copy()
            print(f"Extraido maior componente: {len(maior_componente)} nos")
        
        print(f"Grafo preparado: {len(grafo.nodes)} nos, {len(grafo.edges)} arestas")
        return grafo
    
    def calcular_rota_otimizada(self, grafo):
        """
        Calcula arvore geradora minima usando Prim
        """
        print(f"Calculando arvore geradora minima ({self.algoritmo.upper()})...")
        
        inicio = time.time()
        
        try:
            arvore = nx.minimum_spanning_tree(grafo, weight=self.peso, algorithm=self.algoritmo)
                
        except Exception as e:
            print(f"Erro no uso do algoritmo: {e}")
            return None, None
        
        tempo_execucao = time.time() - inicio
        
        metricas = self._calcular_metricas(grafo, arvore, tempo_execucao)
        
        print(f"Arvore calculada em {tempo_execucao:.3f} segundos")
        return arvore, metricas
    
    def _calcular_metricas(self, grafo_original, arvore_otimizada, tempo):
        """Calcula metricas de performance da otimizacao"""
        
        comprimento_total = sum(
            data[self.peso] 
            for _, _, data in grafo_original.edges(data=True)
        )
        
        comprimento_otimizado = sum(
            data[self.peso] 
            for _, _, data in arvore_otimizada.edges(data=True)
        )
        
        economia = comprimento_total - comprimento_otimizado
        percentual_economia = (economia / comprimento_total) * 100 if comprimento_total > 0 else 0
        
        metricas = {
            'comprimento_total_metros': comprimento_total,
            'comprimento_otimizado_metros': comprimento_otimizado,
            'economia_metros': economia,
            'economia_percentual': percentual_economia,
            'tempo_execucao_segundos': tempo,
            'numero_nos_original': len(grafo_original.nodes),
            'numero_arestas_original': len(grafo_original.edges),
            'numero_arestas_otimizado': len(arvore_otimizada.edges),
            'algoritmo_utilizado': self.algoritmo
        }
        
        print(f"Economia de distancia: {economia:.0f}m ({percentual_economia:.1f}%)")
        print(f"Reducao de rotas: {len(grafo_original.edges)} -> {len(arvore_otimizada.edges)} arestas")
        print(f"Comprimento total: {comprimento_total/1000:.1f}km -> {comprimento_otimizado/1000:.1f}km")
        
        return metricas