# Sistema de Otimização de Rotas de Coleta

Sistema para otimização de rotas de coleta de lixo usando algoritmos de grafos (Prim/Kruskal) e dados reais do OpenStreetMap. Desenvolvido para análise de bairros de qualquer cidade.

## Funcionalidades

- Coleta automática de dados de ruas do OpenStreetMap
- Construção de grafo da malha viária do bairro
- Aplicação de algoritmos de árvore geradora mínima (Prim/Kruskal)
- Cálculo de economia de distância para rotas de coleta
- Geração de mapas comparativos
- Relatório detalhado das ruas otimizadas

## Requisitos

- Python 3.8 ou superior
- Conexão com internet (para acessar APIs do OpenStreetMap)

## Instalação

### Método 1: Instalação básica (para uso)

```bash
# Clone o repositório
git clone https://github.com/seuusuario/coleta-montes-claros.git
cd src

# Instale dependências principais
pip install -r requirements.txt
```

### Método 2: Instalação completa (para desenvolvimento/análise)

```bash
# Clone o repositório
git clone https://github.com/seuusuario/coleta-montes-claros.git
cd src

# Instale todas as dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Configuração

Antes de executar, configure o arquivo `config/settings.py`:

```python
# config/settings.py

# CONFIGURAÇÕES DA CIDADE
CIDADE = "Montes Claros, MG, Brasil"  # Nome da cidade, estado, país
BAIRRO_FOCO = "Ibituruna"             # Nome do bairro para análise

# CONFIGURAÇÕES DO ALGORITMO
ALGORITMO = "prim"  # Algoritmo a ser usado: "prim" ou "kruskal"
```

### Configurações disponíveis:

1. **Localização**:
   - `CIDADE`: Cidade completa (formato: "Nome, Estado, País")
   - `BAIRRO_FOCO`: Nome do bairro para análise

2. **Algoritmo**:
   - `ALGORITMO`: "prim" (recomendado para grafos densos) ou "kruskal" (para grafos esparsos)

3. **API** (geralmente não precisa alterar):
   - `TIMEOUT`: Tempo limite para requisições (em segundos)
   - `USER_AGENT`: Identificação para a API

4. **Visualização**:
   - `COR_REDE_COMPLETA`: Cor do mapa completo
   - `COR_ROTA_OTIMIZADA`: Cor do mapa otimizado
   - `TAMANHO_PONTO`: Tamanho dos pontos (cruzamentos)
   - `LARGURA_LINHA`: Largura das linhas (ruas)

5. **Saída**:
   - `PASTA_RESULTADOS`: Pasta para salvar resultados
   - `NOME_MAPA`: Nome do arquivo do mapa
   - `NOME_RELATORIO`: Nome do arquivo do relatório

## Uso

### Execução básica:

```bash
python main.py
```

O sistema irá:
1. Buscar dados do bairro configurado no OpenStreetMap
2. Construir o grafo da malha viária
3. Aplicar o algoritmo de otimização
4. Gerar mapa comparativo em `resultados/mapa_otimizacao.png`
5. Gerar relatório em `resultados/ruas_otimizadas.csv`
6. Mostrar métricas de economia no console

### Exemplo de saída:

```
SISTEMA DE OTIMIZAÇÃO DE ROTAS DE COLETA
==========================================
FOCO: Ibituruna - Montes Claros
==========================================

FASE 1: COLETA DE DADOS
----------------------------------------
Buscando coordenadas para: Ibituruna
Bairro encontrado: Ibituruna, Montes Claros, MG, Brasil
Bounding Box: [-16.7563945, -16.7166345, -43.9059913, -43.8784719]
Buscando dados das ruas...
Dados recebidos: 7786 elementos
Tipos de vias encontradas:
 residential: 643 vias
 secondary: 7 vias
 tertiary: 27 vias
 ...
Construindo grafo a partir de dados reais...
Processando 6276 nós...
Processando 1510 vias...
Grafo construído: 3138 nós, 3663 arestas
Ruas processadas: 3663

GRAFO REAL OBTIDO COM SUCESSO!
Bairro: Ibituruna
Cruzamentos: 3138
Trechos de rua: 3663
Extensão total: 2024595 metros

FASE 2: OTIMIZAÇÃO DE ROTAS
----------------------------------------
Preparando grafo para otimização...
Grafo preparado: 3138 nós, 3663 arestas
Calculando árvore geradora mínima (PRIM)...
Algoritmo: Prim - eficiente para grafos densos
Economia de distância: 674595m (33.3%)
Redução de rotas: 3663 -> 3137 arestas
Comprimento total: 2024.6km -> 1350.0km
Árvore calculada em 0.163 segundos

FASE 3: VISUALIZAÇÃO DE RESULTADOS
----------------------------------------
Criando mapa comparativo...
Mapa salvo como: 'resultados/mapa_otimizacao.png'
Gerando relatório de ruas...
RESUMO DAS RUAS - Ibituruna:
Total de ruas na rota: 3137
Extensão total: 1350000.0m (1350.0km)
Rua mais longa: 'Av. Principal' (1500m)
Relatório salvo como: 'resultados/ruas_otimizadas.csv'

RELATÓRIO FINAL DE EXECUÇÃO
==========================================
BAIRRO: Ibituruna
ALGORITMO: PRIM
TEMPO DE EXECUÇÃO: 0.163s
EXTENSÃO TOTAL: 2024595m
EXTENSÃO OTIMIZADA: 1350000m
ECONOMIA: 674595m (33.3%)
REDUÇÃO DE ROTAS: 3663 -> 3137
==========================================

PROJETO CONCLUÍDO COM SUCESSO!
Verifique os arquivos na pasta 'resultados/'
```

## Estrutura do Projeto

```
src/
├── config/                 # Configurações
│   ├── __init__.py
│   └── settings.py        # Arquivo de configuração
├── data/                  # Coleta de dados
│   ├── __init__.py
│   └── collector.py       # Interface com APIs do OpenStreetMap
├── models/                # Algoritmos
│   ├── __init__.py
│   └── optimizer.py       # Implementação de Prim/Kruskal
├── utils/                 # Utilidades
│   ├── __init__.py
│   └── visualizer.py      # Geração de mapas e relatórios
├── resultados/            # Saídas geradas
│   └── .gitkeep           # Mantém pasta no git
├── requirements.txt       # Dependências principais
├── requirements-dev.txt   # Dependências de desenvolvimento
├── main.py               # Script principal
└── README.md             # Este arquivo
```

## Arquivos Gerados

1. **Mapa comparativo** (`resultados/mapa_otimizacao.png`):
   - Lado esquerdo: Malha viária completa
   - Lado direito: Rota otimizada
   - Mostra economia obtida

2. **Relatório de ruas** (`resultados/ruas_otimizadas.csv`):
   - Lista todas as ruas da rota otimizada
   - Ordenada por comprimento (mais longa primeiro)
   - Inclui: nome da rua, comprimento, tipo de via

## Dependências

### Principais (requirements.txt):
- `networkx`: Algoritmos de grafos
- `pandas`: Manipulação de dados
- `matplotlib`: Visualização
- `requests`: Comunicação com APIs
- `osmnx`: Interface com OpenStreetMap
- `geopandas`: Processamento geográfico

### Desenvolvimento (requirements-dev.txt):
- `jupyter`: Análise exploratória
- `black`: Formatação de código
- `pytest`: Testes automatizados

## API do OpenStreetMap

O sistema utiliza duas APIs do OpenStreetMap:

1. **Nominatim API**: Converte nomes de bairros em coordenadas geográficas
   - Função: Geocoding (encontrar localização)
   - URL: `https://nominatim.openstreetmap.org/search`

2. **Overpass API**: Retorna elementos de mapa dentro de uma área
   - Função: Consulta espacial (buscar ruas)
   - URL: `https://overpass-api.de/api/interpreter`

## Algoritmos Implementados

### Algoritmo de Prim
- Eficiente para grafos densos
- Complexidade: O(E log V)
- Implementação: `nx.minimum_spanning_tree(G, algorithm='prim')`

### Algoritmo de Kruskal  
- Eficiente para grafos esparsos
- Complexidade: O(E log E)
- Implementação: `nx.minimum_spanning_tree(G, algorithm='kruskal')`

Para trocar de algoritmo, altere `ALGORITMO` no `config/settings.py`.

## Solução de Problemas

### Erro "ModuleNotFoundError":
```bash
# Certifique-se que instalou as dependências:
pip install -r requirements.txt
```

### Erro de timeout (API lenta):
```python
# Aumente o TIMEOUT no config/settings.py:
TIMEOUT = 300  # 5 minutos
```

### Bairro não encontrado:
- Verifique o nome no OpenStreetMap
- Use formato: "Nome do Bairro, Cidade, Estado"

### Pasta resultados não existe:
```bash
# Crie manualmente:
mkdir resultados
```

## Exemplos de Uso

### Analisar outra cidade:
```python
# config/settings.py
CIDADE = "São Paulo, SP, Brasil"  # Nome da cidade, estado, país
```

### Analisar outro bairro:
```python
# config/settings.py
BAIRRO_FOCO = "Jaçanã"  # Ou outro bairro
```

### Usar algoritmo Kruskal:
```python
# config/settings.py
ALGORITMO = "kruskal"
```

## Limitações

1. Depende da disponibilidade das APIs do OpenStreetMap
2. Dados limitados à precisão do OpenStreetMap
3. Considera apenas vias acessíveis para veículos
4. Não considera restrições de horário ou trânsito

## Publicação Científica

Este trabalho foi desenvolvido para fins acadêmicos. O código está disponível para replicação dos resultados.

## Autores

- Thiago Lima Queiroz (thiagolq100@gmail.com)
