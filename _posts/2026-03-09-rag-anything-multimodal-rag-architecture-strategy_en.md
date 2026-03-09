---
title: "RAG-Anything: Multimodal RAG Architecture & Strategy"
date: 2026-03-09 17:53:13 -0400
categories:
  - blog
tags:
  - multimodal RAG
  - RAG-Anything
  - cross-modal retrieval
  - dual-graph structure
  - vision-language model
  - enterprise RAG
  - document AI
  - LightRAG
layout: single
author_profile: true
read_time: true
comments: false
share: false
related: true
---

# Your RAG System Is Ignoring Half Your Documents

Imagine a RAG system analyzing last quarter's earnings presentation. It reads the text perfectly—but skips the charts showing revenue trends, the tables breaking down profit by division, and the graphs visualizing market share. The visual data containing key insights gets ignored as if it doesn't exist. This is the reality facing most text-only RAG systems today.

Real-world enterprise documents aren't purely text. Visualizations proving experimental results in academic papers, radiological images serving as diagnostic evidence in medical records, equations and diagrams explaining operating principles in technical documentation—all this non-textual content encodes critical information. Just as financial analysts look at charts first to understand market trends, and researchers prioritize experimental result tables over conclusions, the center of gravity often lies outside the text.

RAG-Anything, developed by researchers at the University of Hong Kong and published on arXiv, systematically addresses this problem. Released as arXiv:2510.12323v1 with open-source code on GitHub (https://github.com/HKUDS/RAG-Anything), this framework implements multimodal RAG that processes text, images, tables, and equations in an integrated fashion. Rather than bolting image processing onto existing systems, it proposes fundamentally different architecture for handling multimodal content.

## TL;DR

RAG-Anything is a multimodal RAG framework integrating text, image, table, and equation processing. Its core innovations are dual-graph structure and cross-modal hybrid retrieval. It achieved 63.4% accuracy on DocBench and 42.8% on MMLongBench, demonstrating significant improvements over previous state-of-the-art methods. On documents over 100 pages in DocBench, it achieved a 13.6-13.8 percentage point advantage over MMGraphRAG (with a 7.9 point gap in the 101-200 page range on MMLongBench). Built on LightRAG, you can deploy it immediately via `pip install raganything` and integrate with existing LightRAG instances.

## The Fundamental Limitation: Why Text Alone Isn't Enough

Most current RAG frameworks rest on an implicit assumption: the knowledge corpus consists of pure text. As the name Retrieval-Augmented Generation reveals, the retrieval target has been text chunks, and the generation context has been textual. But this fundamentally misaligns with real information environments.

Some systems recognize this and attempt a flattening approach—converting non-textual content into textual descriptions. Describing a chart as "this graph shows an increasing revenue trend from 2020 to 2024," or writing out an equation as "x squared plus y squared equals the radius squared." But this causes severe information loss. The spatial relationships in charts revealing inflection points, the structural meaning in tables enabling cross-category comparisons, the mathematical precision provided by symbolic notation—all of this gets lost or distorted in text conversion.

Implementing multimodal RAG requires solving three core technical challenges. First, **unified multimodal representation**: handling text, images, tables, and equations within a single knowledge space. Second, **structure-aware decomposition**: chunking documents while preserving structural relationships showing which images connect to which textual descriptions and which analytical context a table resides in. Third, **cross-modal retrieval**: finding relevant images for text queries, or retrieving explanatory text for visual patterns—connections across modalities. These demand not incremental improvements to existing text-centric pipelines, but fundamentally different architectural approaches.

## RAG-Anything's Core Architecture: Dual-Graph Structure

RAG-Anything's key innovation lies in its dual-graph structure. While LightRAG extracted entities and relationships from text to build a graph, RAG-Anything adds another layer: the Cross-Modal Knowledge Graph (Cross-Modal KG).

### Multimodal Knowledge Integration

The first stage is multimodal knowledge integration. RAG-Anything decomposes documents into atomic content units. Each unit cj is represented as a pair of type tj (text, image, table, equation) and actual content xj:

```python
cj = (tj, xj)
# tj ∈ {text, image, table, equation, ...}
# xj = actual content (image data, table structure, text, etc.)
```

Crucially, it preserves both modality type and structural context. An experimental result image from a paper isn't simply stored as an image file—it records connections to the textual description in that section, the caption, and the previous section discussing methodology.

### Two Complementary Graphs

RAG-Anything constructs two graph structures that complement each other:

**1. Entity-Relationship Graph (ER Graph)**

This graph follows LightRAG's tradition of extracting entities and relationships from textual content. But RAG-Anything extends this to all modalities. For an image showing neural network architecture, entities like "convolutional layer" and "pooling layer" are extracted from the visual structure itself, not just from accompanying text. For tables, column headers and row labels become entities with structural relationships between cells preserved.

```python
# Entity extraction from multimodal content
entity_i = {
  'name': 'Convolutional Layer',
  'source_modality': 'image',
  'source_content': cj,  # Reference to original image
  'attributes': {...}
}

# Relationship between entities
relation = {
  'source': entity_i,
  'target': entity_k,
  'type': 'feeds_into',
  'confidence': 0.95
}
```

**2. Cross-Modal Knowledge Graph (Cross-Modal KG)**

This is RAG-Anything's distinctive contribution. While the ER Graph captures knowledge within each modality, the Cross-Modal KG explicitly models relationships between modalities. When a paragraph describes "as shown in Figure 3," the Cross-Modal KG creates a `describes` edge from the text node to the image node. When a table caption explains "demographic breakdown of participants," the Cross-Modal KG records the `caption_of` relationship between text and table.

```python
# Cross-modal relationship
cross_modal_edge = {
  'source': text_node_p,
  'target': image_node_q,
  'relation': 'describes',
  'context': "experimental results showing..."
}
```

This dual structure provides two complementary search paths. The ER Graph enables reasoning across entities ("Find all methods mentioned in connection with ResNet architecture"), while the Cross-Modal KG enables cross-modal navigation ("Find images explained by this text" or "Find the text that explains this table's meaning").

### Vision-Language Model-Based Content Understanding

Understanding multimodal content requires more than OCR or image tagging. RAG-Anything employs Vision-Language Models (VLMs) to extract semantic understanding from images, tables, and equations. For images, it generates natural language descriptions ("a line graph showing exponential growth with three inflection points"), structural analysis ("bar chart comparing five categories across three time periods"), and connections to surrounding context.

For tables, rather than simply converting them to CSV format, it understands hierarchical headers, cell dependencies, and computational relationships. A financial statement table is understood not just as numbers in cells, but as a structure where "Net Income = Revenue - Expenses" with semantic relationships preserved.

```python
# VLM-based image understanding
image_embedding = vlm_encode(image_content)
image_description = vlm_describe(image_content)
# → "scatter plot showing positive correlation 
#    between variables X and Y with R² = 0.87"

image_entities = extract_entities(image_description)
# → ['scatter plot', 'positive correlation', 'X', 'Y', 'R²']
```

## Hybrid Retrieval: Finding Across Modalities

Having constructed the dual-graph structure, the next challenge is retrieval. How do you find relevant content when a query might need textual explanations, visual evidence, or both?

### Three-Stage Hybrid Retrieval

RAG-Anything implements a three-stage hybrid retrieval process:

**Stage 1: Initial Multi-Modal Retrieval**

The system performs parallel retrieval across all modalities. Text queries retrieve text chunks via semantic similarity, but simultaneously retrieve relevant images, tables, and equations using cross-modal embeddings. This differs fundamentally from sequential "retrieve text then find associated images" approaches—all modalities are first-class retrieval targets.

```python
query = "How does the proposed model compare to baseline?"

# Parallel retrieval across modalities
text_results = semantic_search(query, text_index)
image_results = cross_modal_search(query, image_index)
table_results = cross_modal_search(query, table_index)
```

**Stage 2: Graph-Based Expansion**

Initial retrieval results serve as starting points for graph traversal. If a relevant text chunk is retrieved, the system follows edges in the Cross-Modal KG to find associated images and tables. Conversely, when a relevant image is found, it traces back to explanatory text through `described_by` edges.

```python
# Graph expansion from retrieved text
retrieved_text_node = text_results[0]
related_visuals = cross_modal_kg.traverse(
    start=retrieved_text_node,
    edge_types=['describes', 'references'],
    max_depth=2
)
```

This graph-based expansion is particularly powerful for complex queries. A question like "What experimental setup led to the performance improvement?" might retrieve the results section text through initial retrieval, then graph traversal discovers the methodology diagram two sections earlier and the hyperparameter table in the appendix.

**Stage 3: Re-Ranking and Fusion**

The final stage re-ranks and fuses results from different modalities. Not all content is equally relevant, and not all modalities carry equal weight for every query. RAG-Anything learns to weight different modalities based on query characteristics.

```python
# Learned fusion with attention
query_type_vector = classify_query(query)
# → {visual_intent: 0.7, textual_intent: 0.4, tabular_intent: 0.8}

modality_weights = attention(
    query_vector, 
    [text_results, image_results, table_results],
    query_type_vector
)

final_ranking = weighted_fusion(
    all_results,
    modality_weights
)
```

For a query like "show the trend," the system learns to weight image and table results more heavily. For "explain the methodology," text receives higher priority, but related diagrams are still included.

## Benchmark Performance: Quantitative Validation

RAG-Anything was evaluated on two challenging multimodal QA benchmarks:

### DocBench Results

DocBench contains long academic papers (average ~40 pages) requiring understanding of text, figures, tables, and equations. RAG-Anything achieved:

- **Overall Accuracy: 63.4%** (vs. 49.6% for MMGraphRAG, the previous SOTA)
- **100+ page documents: 61.5%** (vs. 47.7% for MMGraphRAG)

The 13.8 percentage point gap on long documents is particularly significant. As documents grow longer, the structural advantages of the dual-graph approach become more pronounced. Navigating a 200-page technical report requires precisely the kind of cross-modal reasoning that the Cross-Modal KG enables.

### MMLongBench Results

MMLongBench tests even longer documents (some exceeding 1,000 pages) across diverse domains. Results:

- **Overall Accuracy: 42.8%** (vs. 34.9% for MMGraphRAG)
- **101-200 page range: 40.7%** (vs. 32.8% for MMGraphRAG)
- **800+ page documents: 39.4%** (vs. 30.2% for MMGraphRAG)

The 7.9-9.2 percentage point advantages demonstrate that RAG-Anything's architecture scales effectively to extremely long documents where traditional retrieval methods struggle.

### Modality-Specific Analysis

Breaking down performance by required modalities reveals interesting patterns:

| Required Modality | RAG-Anything | MMGraphRAG | Improvement |
|-------------------|--------------|------------|-------------|
| Text only         | 65.8%        | 52.1%      | +13.7 pts   |
| Text + Image      | 62.3%        | 48.9%      | +13.4 pts   |
| Text + Table      | 61.7%        | 47.3%      | +14.4 pts   |
| All modalities    | 58.4%        | 45.2%      | +13.2 pts   |

Notably, RAG-Anything maintains relatively stable performance across modality combinations, while baselines show significant degradation when multiple modalities are required. This suggests the Cross-Modal KG successfully bridges modalities rather than treating them as isolated silos.

## Practical Implementation: From Research to Production

RAG-Anything isn't just a research prototype—it's designed for real-world deployment:

### Installation and Setup

```bash
pip install raganything
```

Built on LightRAG, it inherits that framework's maturity and ecosystem compatibility. Existing LightRAG deployments can migrate with minimal code changes.

### Basic Usage

```python
from raganything import RAGAnything

# Initialize with multimodal support
rag = RAGAnything(
    working_dir="./rag_storage",
    enable_vision=True,
    enable_tables=True,
    enable_equations=True
)

# Insert multimodal document
rag.insert_document(
    "financial_report.pdf",
    extract_images=True,
    extract_tables=True
)

# Query with automatic multimodal retrieval
results = rag.query(
    "What was the revenue trend over the last 3 quarters?",
    return_modalities=['text', 'image', 'table']
)

# Results include relevant text, charts, and tables
for result in results:
    print(f"Type: {result.modality}")
    print(f"Content: {result.content}")
    print(f"Relevance: {result.score}")
```

### Configuration Options

RAG-Anything provides extensive configurability:

```python
rag = RAGAnything(
    working_dir="./rag_storage",
    
    # Vision-Language Model configuration
    vlm_model="gpt-4-vision",  # or "llava", "qwen-vl", etc.
    vlm_temperature=0.1,
    
    # Graph construction parameters
    entity_extraction_threshold=0.7,
    cross_modal_edge_threshold=0.6,
    max_graph_depth=3,
    
    # Retrieval parameters
    top_k_per_modality=5,
    enable_graph_expansion=True,
    expansion_depth=2,
    
    # Fusion weights
    modality_weights={
        'text': 1.0,
        'image': 0.8,
        'table': 0.9,
        'equation': 0.7
    }
)
```

### Integration with Existing Systems

For teams with existing RAG pipelines, RAG-Anything can be integrated incrementally:

```python
# Hybrid approach: existing text RAG + RAG-Anything for multimodal
from raganything import MultiModalRetriever

# Existing text retrieval
text_results = existing_rag.retrieve(query)

# Add multimodal retrieval
mm_retriever = MultiModalRetriever(
    cross_modal_kg=loaded_graph
)
visual_results = mm_retriever.retrieve_visual(
    query,
    text_context=text_results
)

# Combine results
final_context = merge_multimodal_results(
    text_results,
    visual_results
)
```

## Performance Considerations and Optimization

Multimodal RAG introduces computational overhead. Some practical considerations:

### Index Size and Storage

Storing embeddings for images, tables, and equations increases index size:

- Text-only RAG: ~100-200 MB per 10k documents
- RAG-Anything: ~800MB-1.2GB per 10k documents (with images)

Storage optimization strategies:
- Image embedding compression (reducing dimensions from 768 to 256 preserves 95% of retrieval quality)
- Hierarchical storage (frequently accessed hot storage, rarely accessed cold storage)
- On-demand VLM processing (pre-compute for critical documents, process on-demand for others)

### Latency Profile

Typical query latencies:

- Text-only retrieval: 50-100ms
- Multimodal retrieval (no graph expansion): 150-250ms
- Full multimodal with graph expansion: 300-500ms