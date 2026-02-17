---
title: "Graph RAG Agents: Beyond Basic RAG with Neo4j & Cypher"
date: 2026-02-17 16:58:14 -0500
categories:
  - blog
tags:
  - Graph RAG
  - RAG agents
  - Neo4j knowledge graph
  - Cypher queries
  - vector search limitations
  - entity extraction
  - agentic workflows
  - knowledge graph RAG
layout: single
author_profile: true
read_time: true
comments: false
share: false
related: true
---

# Beyond Basic RAG: Building Graph RAG Agents with Multiple Data Sources

## Introduction: Why Basic RAG Falls Short for Analytical Questions

"How many Python developers do we have in our company?"

Simple question, right? But here's what happens when you ask a standard document embedding-based RAG system: if you've set K=5, you'll get "Found 5 Python developers"—even when you actually have 28.

Consider building an employee knowledge management system. You'll need features like skill analysis, team similarity calculations, and collaboration potential exploration. Vector search alone hits three critical walls:

- **No aggregation**: "How many?" questions remain unanswered
- **No precise similarity calculations**: Semantic similarity can't compute actual skill overlap
- **No relationship traversal**: Flat document structures make "who collaborated with whom?" impossible to answer

Let's walk through evolving basic RAG into a graph-based system that solves these problems, step by step.

## Step 1: Document-Based Approach and Its Limitations

We'll start with the most intuitive approach: loading PDF resumes into Neo4j as document nodes.

```python
# Basic document RAG approach
from google import genai
from google.genai import types

# Create document nodes (with metadata, text, embeddings)
CREATE (d:Document {
  name: "john_doe_resume.pdf",
  text: "...",
  embedding: [0.1, 0.2, ...]
})
```

Next, build a simple agent with Google ADK, providing only a document search tool:

```python
agent = genai.Agent(
    model="gemini-2.0-flash-exp",
    tools=[document_search_tool]
)

# Queries that fail
response = agent.send_message("How many Python developers do we have?")
# → Inaccurate answer due to K=5 limit

response = agent.send_message("Who has similar skills to John Smith?")
# → Can't compute precise skill overlap with semantic similarity alone

response = agent.send_message("Which teams can collaborate on AI projects?")
# → Relationship traversal impossible with document structure
```

**The takeaway**: Document embeddings excel at "is this document relevant?" but fail at analytical questions requiring structural reasoning.

## Step 2: Designing Graph Data Models from Questions

Effective graph models work **backward from the questions you want to answer**:

- "Who knows what?" → `Person → KNOWS → Skill`
- "Who did what?" → `Person → DID → Accomplishment`

We'll define entities and relationships using Pydantic:

```python
from pydantic import BaseModel, Field
from typing import List, Literal

class Skill(BaseModel):
    name: str
    proficiency: Literal["beginner", "intermediate", "expert"]

class Accomplishment(BaseModel):
    description: str
    type: Literal["built", "led", "shipped", "optimized"]
    domains: List[str]  # ["AI", "backend", "infrastructure"]
    work_type: Literal["individual", "team"]

class Person(BaseModel):
    name: str
    email: str
    skills: List[Skill]
    accomplishments: List[Accomplishment]
```

This model grows progressively. Start simple, then expand with new nodes and relationships as needs evolve.

## Step 3: Entity Extraction and Graph Construction

Now we'll use an LLM to transform unstructured resume text into a structured graph:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Entity extraction prompt
extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract Person, Skill, and Accomplishment entities from the following resume."),
    ("human", "{resume_text}")
])

llm = ChatOpenAI(model="gpt-4")
chain = extraction_prompt | llm.with_structured_output(Person)

# Extract structured data from resume text
person_data = chain.invoke({"resume_text": resume_text})

# Create graph in Neo4j
CREATE (p:Person {name: $name, email: $email})
FOREACH (skill IN $skills |
  MERGE (s:Skill {name: skill.name})
  CREATE (p)-[:KNOWS {proficiency: skill.proficiency}]->(s)
)
FOREACH (acc IN $accomplishments |
  CREATE (a:Accomplishment {description: acc.description, type: acc.type})
  CREATE (p)-[:DID]->(a)
  FOREACH (domain IN acc.domains |
    MERGE (d:Domain {name: domain})
    CREATE (a)-[:IN_DOMAIN]->(d)
  )
)
```

**The result**: You now have a rich graph where people connect through shared skills, domains, and accomplishment types.

## Step 4: Building Graph-Based Agents with Cypher Queries

Using the Neo4j MCP server tool, agents can read the schema and generate Cypher queries dynamically:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Connect to Neo4j MCP server
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-neo4j"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Create agent with data model description
        agent = genai.Agent(
            model="gemini-2.0-flash-exp",
            system_instruction="""
            You have access to a Neo4j graph database.
            Data model: Person → KNOWS → Skill, Person → DID → Accomplishment → IN_DOMAIN → Domain
            """
        )
```

Now you'll get accurate results:

```python
# Aggregation queries deliver precise counts
response = agent.send_message("How many Python developers do we have?")
# Cypher: MATCH (p:Person)-[:KNOWS]->(s:Skill {name: 'Python'}) RETURN count(p)
# → 28 people (accurate!)

# Similarity calculations based on overlapping skills
response = agent.send_message("Who has the most similar skills to John Smith?")
# Cypher: MATCH (p1:Person {name: 'John Smith'})-[:KNOWS]->(s:Skill)<-[:KNOWS]-(p2:Person)
#         RETURN p2.name, count(s) as overlap ORDER BY overlap DESC

# Multi-hop traversal (0-3 hops)
response = agent.send_message("Find people with similar accomplishments in the AI domain")
# Flexible traversal connecting skills → domains → accomplishments
```

## Step 5: Adding New Data Sources Without Schema Refactoring

The real power of graphs emerges here. Let's add HR project collaboration data:

```python
# Add new relationships—no join tables needed
MATCH (p1:Person {email: $email1}), (p2:Person {email: $email2})
CREATE (p1)-[:COLLABORATED_WITH {
  project: $project_name,
  domain: $domain,
  duration_months: $duration
}]->(p2)
```

Then add a collaborator-finding tool:

```python
# Find people who've collaborated within a domain
MATCH (p1:Person)-[:COLLABORATED_WITH]->(p2:Person)
WHERE p1.name = $person_name
MATCH (p1)-[:DID]->(:Accomplishment)-[:IN_DOMAIN]->(d:Domain)
MATCH (p2)-[:DID]->(:Accomplishment)-[:IN_DOMAIN]->(d)
RETURN p2.name, d.name, count(*) as shared_projects
```

**The key insight**: Add new relationships without touching existing schema. Traditional SQL would require complete table redesign.

## Key Takeaways and Next Steps

What Graph RAG provides your agents:

✅ **Structural reasoning**: Aggregation, filtering, traversal, and explainability  
✅ **Progressive expansion**: Begin with Person, Skill, Accomplishment—expand as questions evolve  
✅ **Flexible schema**: No join table refactoring when new data sources arrive  
✅ **Precise analytics**: Accurate counts and calculations without vector search K limits

**Tools to get started**:
- **Neo4j**: Graph database
- **Neo4j MCP Server**: Enables agents to read schema and generate Cypher
- **Google ADK**: Agent framework
- **LangChain**: For entity extraction

Start with a simple model. As your questions grow more complex, your graph will naturally evolve with them. That's the beauty of Graph RAG.