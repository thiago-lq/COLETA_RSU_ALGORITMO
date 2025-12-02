"""
MÓDULO DE COLETA DE DADOS REAIS
Busca dados reais do OpenStreetMap para Montes Claros
"""
import requests
import networkx as nx
from config.settings import CIDADE, NOMINATIM_URL, OVERPASS_URL, TIMEOUT, USER_AGENT

class ColetorDados:
    def __init__(self):
        self.nominatim_url = NOMINATIM_URL
        self.overpass_url = OVERPASS_URL
        self.timeout = TIMEOUT
        self.headers = {'User-Agent': USER_AGENT}
        self.cidade = CIDADE
    
    def buscar_coordenadas_bairro(self, nome_bairro):
        """Converte nome do bairro em coordenadas (geocoding)"""
        print(f"Buscando coordenadas para: {nome_bairro}")
        
        """ Configurações do request """
        params = {
            'q': f"{nome_bairro}, {self.cidade}",
            'format': 'json',
            'limit': 1,
            'polygon_geojson': 1
        }
        
        """ Try catch, para buscar os dados e capturar erros """
        try:
            resposta = requests.get(
                self.nominatim_url,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
            resposta.raise_for_status()
            dados = resposta.json()
            
            if dados:
                lugar = dados[0]
                bbox = [
                    float(lugar['boundingbox'][0]),  # sul
                    float(lugar['boundingbox'][1]),  # norte
                    float(lugar['boundingbox'][2]),  # oeste  
                    float(lugar['boundingbox'][3])   # leste
                ]
                
                print(f"Bairro encontrado: {lugar['display_name']}")
                print(f"Bounding Box: {bbox}")
                return bbox
            else:
                print(" Bairro não encontrado no Nominatim")
                return None
                
        except Exception as e:
            print(f" Erro na busca de coordenadas: {e}")
            return None
    
    def buscar_dados_ruas(self, bbox):
        """Busca dados das ruas usando Overpass API"""
        print("  Buscando dados das ruas...")
        
        # Query Overpass QL - busca vias para veículos
        overpass_query = f"""
        [out:json][timeout:90];
        (
          // ==================== VIAS PRINCIPAIS ====================
          // Vias arteriais - Caminhões de lixo principais
          way["highway"~"primary|primary_link"]
            ({bbox[0]},{bbox[2]},{bbox[1]},{bbox[3]});
          
          // ==================== VIAS SECUNDÁRIAS ====================
          // Vias coletoras - Caminhões de coleta
          way["highway"~"secondary|secondary_link|tertiary|tertiary_link"]
            ({bbox[0]},{bbox[2]},{bbox[1]},{bbox[3]});

          // ==================== VIAS LOCAIS ====================
          // Ruas residenciais - caminhões menores
          way["highway"~"residential|unclassified|living_street"]
            ({bbox[0]},{bbox[2]},{bbox[1]},{bbox[3]});

          // ==================== VIAS DE SERVIÇO ====================
          // Apenas vias de serviço acessíveis para veículos
          // A expressão '!~' é para ignorar, ou seja, todos abaixo estão sendo ignorados
          way["highway"="service"]
            ["service"!~"parking_aisle|driveway|alley|emergency_access"]
            ["access"!~"private|no|destination"]
            ({bbox[0]},{bbox[2]},{bbox[1]},{bbox[3]});
        );
        //Resultados unificados
        (._;>;);
        out body;
        out skel qt;
        """
        try:
            """ Enviando a query ao Overpass API """
            resposta = requests.post(
                self.overpass_url,
                data={'data': overpass_query},
                headers=self.headers,
                timeout=120
            )
            resposta.raise_for_status()
            
            dados = resposta.json()
            print(f" Dados recebidos: {len(dados['elements'])} elementos")

            # Análise dos tipos de vias encontradas
            if dados['elements']:
                tipos_vias = {}
                for elemento in dados['elements']:
                    if elemento['type'] == 'way' and 'tags' in elemento:
                        tipo = elemento['tags'].get('highway', 'desconhecido')
                        tipos_vias[tipo] = tipos_vias.get(tipo, 0) + 1
                
                print("Tipos de vias encontradas:")
                for tipo, quantidade in tipos_vias.items():
                    print(f" {tipo}: {quantidade} vias")

            return dados
            
        except Exception as e:
            print(f" Erro ao buscar dados das ruas: {e}")
            return None
    
    def construir_grafo_real(self, dados_overpass):
        """Constrói grafo NetworkX a partir de dados reais do Overpass"""
        print("Construindo grafo a partir de dados reais...")
        
        G = nx.Graph()
        nodes_dict = {}
        
        # Fase 1: Processar nós (cruzamentos)
        elementos_nos = [e for e in dados_overpass['elements'] if e['type'] == 'node']
        print(f"   Processando {len(elementos_nos)} nós...")
        
        for node in elementos_nos:
            nodes_dict[node['id']] = {
                'lat': node['lat'],
                'lon': node['lon']
            }
            G.add_node(node['id'], y=float(node['lat']), x=float(node['lon']))
        
        # Fase 2: Processar arestas (vias/ruas)
        elementos_ways = [e for e in dados_overpass['elements'] if e['type'] == 'way']
        print(f"Processando {len(elementos_ways)} vias...")
        
        ruas_processadas = 0
        
        for way in elementos_ways:
            if 'tags' not in way:
                continue
                
            nodes_way = way['nodes']
            tags = way['tags']
            
            # Criar arestas entre nós consecutivos da via
            for i in range(len(nodes_way) - 1):
                node1, node2 = nodes_way[i], nodes_way[i + 1]
                
                if node1 in nodes_dict and node2 in nodes_dict:
                    # Calcular distância aproximada em metros
                    lat1, lon1 = nodes_dict[node1]['lat'], nodes_dict[node1]['lon']
                    lat2, lon2 = nodes_dict[node2]['lat'], nodes_dict[node2]['lon']
                    
                    comprimento = self._calcular_distancia_aproximada(lat1, lon1, lat2, lon2)
                    
                    G.add_edge(
                        node1, node2,
                        length=comprimento,
                        name=tags.get('name', f'Via_{way["id"]}'),
                        highway=tags.get('highway', 'desconhecido'),
                        osm_id=way['id']
                    )
                    ruas_processadas += 1
        
        print(f"Grafo construído: {len(G.nodes)} nós, {len(G.edges)} arestas")
        print(f"Ruas processadas: {ruas_processadas}")
        
        return G
    
    def _calcular_distancia_aproximada(self, lat1, lon1, lat2, lon2):
        """Calcula distância aproximada em metros entre coordenadas"""
        # Fórmula simplificada - 1 grau ≈ 111km
        delta_lat = (float(lat2) - float(lat1)) * 111320  # metros
        delta_lon = (float(lon2) - float(lon1)) * 111320 * abs(float(lat1))  # ajuste por latitude
        
        return (delta_lat**2 + delta_lon**2)**0.5
    
    def obter_grafo_bairro(self, nome_bairro):
        """
        Método principal: obtém grafo completo do bairro
        Retorna grafo real ou None se não conseguir
        """
        print(f"\n OBTENDO DADOS REAIS PARA: {nome_bairro}")
        print("=" * 50)
        
        # 1. Buscar coordenadas do bairro
        bbox = self.buscar_coordenadas_bairro(nome_bairro)
        if not bbox:
            print(" Não foi possível obter coordenadas do bairro")
            return None
        
        # 2. Buscar dados das ruas
        dados_ruas = self.buscar_dados_ruas(bbox)
        if not dados_ruas or len(dados_ruas['elements']) == 0:
            print(" Não foi possível obter dados das ruas")
            return None
        
        # 3. Construir grafo
        grafo = self.construir_grafo_real(dados_ruas)
        
        if grafo and len(grafo.nodes) > 0:
            print(f"\n GRAFO REAL OBTIDO COM SUCESSO!")
            print(f"   • Bairro: {nome_bairro}")
            print(f"   • Cruzamentos: {len(grafo.nodes)}")
            print(f"   • Trechos de rua: {len(grafo.edges)}")
            print(f"   • Extensão total: {sum(data['length'] for _, _, data in grafo.edges(data=True)):.0f} metros")
            return grafo
        else:
            print(" Grafo vazio ou inválido")
            return None
