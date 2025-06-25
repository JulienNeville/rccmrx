import os
from rdflib_neo4j import Neo4jStoreConfig
from rdflib_neo4j import HANDLE_VOCAB_URI_STRATEGY
from rdflib_neo4j import Neo4jStore
from rdflib import Graph
from dotenv import load_dotenv

load_dotenv()

# set the configuration to connect to your Aura DB

auth_data = {'uri': os.getenv("AURA_DB_URI"),
             'database': os.getenv("AURA_DB_USERNAME"),
             'user': os.getenv("AURA_DB_USERNAME"),
             'pwd': os.getenv("AURA_DB_PWD")}

# AUTH = (AURA_DB_USERNAME, AURA_DB_PWD)
# with GraphDatabase.driver(AURA_DB_URI, auth=AUTH) as driver:
#     driver.verify_connectivity()

# Define your prefixes

# <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
#          xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
#          xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
#          xmlns:owl="http://www.w3.org/2002/07/owl#"
#          xml:base="http://www.isiatech.com/ontologies/rccmrx_ontology.owl"
#          xmlns="http://www.isiatech.com/ontologies/rccmrx_ontology.owl#">

prefixes = {
    # "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    # "xsd":"http://www.w3.org/2001/XMLSchema#",
    # "rdfs":"http://www.w3.org/2000/01/rdf-schema#",
    # "owl":"http://www.w3.org/2002/07/owl#",
    # "base":"http://www.isiatech.com/ontologies/rccmrx_ontology.owl",
    # "xmlns":"http://www.isiatech.com/ontologies/rccmrx_ontology.owl#"
}

# Define your custom mappings
config = Neo4jStoreConfig(auth_data=auth_data,
                          custom_prefixes=prefixes,
                          handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.IGNORE,
                          batching=True)

neo4j_store=Neo4jStore(config=config)
graph_store = Graph(store=neo4j_store)

file_path = "C:\\Users\\julie\\OneDrive\\Dev\\Python_projects\\rccmrx\\ontology\\rccmrx_ontology.xml"
graph_store.parse(file_path,format="xml")
graph_store.close(True)