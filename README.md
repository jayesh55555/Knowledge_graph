# Knowledge Graph Builder with Neo4j & OpenAI

[![Neo4j Version](https://img.shields.io/badge/Neo4j-5.11.0-blue)](https://neo4j.com/)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-brightgreen)](https://python.org)

Transform unstructured text into interactive knowledge graphs using cutting-edge NLP and graph database technologies.

## Features
- 🧠 GPT-3.5 powered entity relationship extraction
- 🗃️ Neo4j graph database integration
- 🔄 Automated database initialization/cleanup
- 📊 Visual relationship mapping
- 📈 Triple validation and quality control
- 📦 Hybrid vector-graph storage system

## Quick Start
### Prerequisites
- Python 3.10+
- Neo4j Desktop/Server
- OpenAI API key

```
git clone https://github.com/yourusername/knowledge-graph-builder.git
cd knowledge-graph-builder
pip install -r requirements.txt
```

### Configuration
1. Create `.env` file:
```
OPENAI_API_KEY=your_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

2. Run the builder:
```
python knowledge_graph.py
```

## Usage Example
### Example 1: Albert Einstein
```
text = """Albert Einstein developed the theory of relativity..."""
create_knowledge_graph(text)
```

### Example 2: Marie Curie
```
text = """Marie Curie was a pioneering physicist and chemist who conducted groundbreaking research on radioactivity.
Born in Warsaw in 1867, she moved to Paris to further her studies. Curie discovered two new elements,
polonium and radium, and developed techniques for isolating radioactive isotopes. In 1903, she became
the first woman to win a Nobel Prize and remains the only person to win Nobel Prizes in two scientific fields.
Her work laid the foundation for many modern applications in nuclear physics and cancer treatment.
Despite facing gender discrimination in the scientific community, Curie's dedication to science never wavered.
Her legacy continues to inspire generations of scientists, particularly women in STEM fields."""
create_knowledge_graph(text)
```


## Visualization

### Einstein & Newton Graph
![Einstein & Newton Knowledge Graph](graph1.jpg)  
*Knowledge graph showing relationships between Einstein, Newton and their contributions to physics*

### Marie Curie Graph
![Marie Curie Knowledge Graph](graph.jpg)  
*Knowledge graph visualizing Marie Curie's life, achievements, and scientific contributions*

## Viewing the Knowledge Graph in Neo4j Browser

1. Open Neo4j Browser (typically at http://localhost:7474)
2. Connect using your credentials
3. Run the following Cypher query to view all nodes and relationships:
```
MATCH (n)-[r]->(m) RETURN n, r, m
```
4. Use the visualization tools in Neo4j Browser to explore and interact with your knowledge graph

## Architecture
```
graph TD
    A[Raw Text] --> B(Entity Extraction)
    B --> C[Triple Generation]
    C --> D[Neo4j Storage]
    D --> E[Graph Visualization]
    C --> F[Vector Storage]
```


