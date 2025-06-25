import os
from langchain_openai import ChatOpenAI
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

graph = Neo4jGraph(
    url=os.getenv("AURA_DB_URI"),
    username=os.getenv("AURA_DB_USERNAME"),
    password=os.getenv("AURA_DB_PWD")
)

CYPHER_GENERATION_TEMPLATE = """
Tu es un expert développeur Neo4j qui traduit les questions des utilisateurs en langage Cypher pour répondre aux questions sur le code de conception et de fabrication nucléaire RCC-MRx.
Tu dois utiliser les classes, relations et les propriétés du graphe pour répondre à la question.

Schéma: {schema}
Question: {question}
"""

cypher_generation_prompt = PromptTemplate(
    template=CYPHER_GENERATION_TEMPLATE,
    input_variables=["schema", "question"],
)

cypher_chain = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    cypher_prompt=cypher_generation_prompt,
    verbose=True,
    allow_dangerous_requests=True
)

result = cypher_chain.invoke({"query": "Quel sont les responsabilités du maître d'ouvrage?"})

print(result)