# ==================== CONFIGURAÇÕES DA CIDADE ====================
CIDADE = "Montes Claros, MG, Brasil" # Nome da cidade, estado, país
BAIRRO_FOCO = "Belvedere" # Nome do bairro

# ==================== CONFIGURAÇÕES DE API ====================
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search" # URL da API do Nominatim, GPS localizador
OVERPASS_URL = "https://overpass-api.de/api/interpreter" # URL da API do Overpass, listagem de ruas
TIMEOUT = 180 # Tempo limite para obter dados da API
USER_AGENT = "Coleta/1.0" # User-Agent para a API

# ==================== CONFIGURAÇÕES DO ALGORITMO ====================
ALGORITMO = "prim" # Algoritmo a ser usado, Prim ou Kruskal
PESO_PADRAO = "length" # Atributo usado para calcular o peso do padrão

# ==================== CONFIGURAÇÕES DE VISUALIZAÇÃO ====================
COR_REDE_COMPLETA = "blue" # Cor do mapa completo
COR_ROTA_OTIMIZADA = "red" # Cor do mapa otimizado
TAMANHO_PONTO = 30 # Tamanho do ponto
LARGURA_LINHA = 3 # Largura da linha

# ==================== CONFIGURAÇÕES DE SAÍDA ====================
PASTA_RESULTADOS = "resultados" # Pasta onde os resultados serão salvos
NOME_MAPA = "mapa_otimizacao.png" # Nome do arquivo de mapa
NOME_RELATORIO = "ruas_otimizadas.csv" # Nome do arquivo de ruas otimizadas