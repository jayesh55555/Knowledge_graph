import os
from dotenv import load_dotenv
from llama_index.core import Document, Settings, StorageContext
from llama_index.core import KnowledgeGraphIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.vector_stores.simple import SimpleVectorStore
from llama_index.graph_stores.neo4j import Neo4jGraphStore
from neo4j import GraphDatabase

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")

Settings.llm = OpenAI(api_key=openai_api_key, temperature=0.1, model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(api_key=openai_api_key)

def connect_to_neo4j():
    return GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

driver = connect_to_neo4j()

def clear_database():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    print("Database cleared.")

def create_and_store(text):
    documents = [Document(text=text)]
    graph_store = Neo4jGraphStore(username=neo4j_user, password=neo4j_password, url=neo4j_uri, database="neo4j")
    vector_store = SimpleVectorStore()
    storage_context = StorageContext.from_defaults(graph_store=graph_store, vector_store=vector_store)

    index = KnowledgeGraphIndex.from_documents(documents, storage_context=storage_context, max_triplets_per_chunk=20)
    index.storage_context.graph_store.persist(persist_path="D:/knowledge_graph")

    query_engine = index.as_query_engine(include_text=False, response_mode="tree_summarize")
    response = query_engine.query("Summarize the key points of the text")
    print("Query Response:", response)

    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) as node_count")
        node_count = result.single()["node_count"]
        print(f"Number of nodes in the database: {node_count}")

def visualise():
    with driver.session() as session:
        node_result = session.run("MATCH (n) RETURN n")
        nodes = [record['n'] for record in node_result]

        rel_result = session.run("MATCH ()-[r]->() RETURN r")
        relationships = [record['r'] for record in rel_result]

    return nodes, relationships

def create_knowledge_graph(text):
    clear_database()
    create_and_store(text)
    nodes, relationships = visualise()
    print(f"Created {len(nodes)} nodes and {len(relationships)} relationships")

# Example text
text = """
Thank you for calling AT&T, my name is Erica. Can I have the wireless telephone number that they were calling about today? 406-539-1202 It's confirmed that number was 406-539-1202, is that correct? Yes. So how may I help you today? I got this letter saying I can get a Blackberry Torch. Okay, I will be more than happy to assist with that. But before we proceed, for the security of your account, can you please verify some information for me first? Yep. Can I have the first and last name of the account holder? Josh Milligan. Okay. And who am I speaking with today, if I may ask? Josh. Okay, Mr. Milligan, can you please verify the billing zip code? 59714. And also the last four digits of your Social Security number? 5528. Thanks so much for that information. So just to make it clear, did I understand correctly, you received a letter regarding the Blackberry Torch? Yes. And you want to take advantage of this offer? Yes. Okay, I'd be more than happy to assist you with that. I'll be filling out all the information needed for the exchange, and it will be processed within 24 hours from now. And I just want to let you know that the new device will arrive within three to five business days. Please do not return old phones until you receive the new device. And I just want to let you know that if the original phone is not returned within 30 days, you will be subject to a $150 charge billed to your account. Also, please don't forget to take the SIM card out of the original phone and place it in the new phone, okay? Okay. And also, you will be receiving a customer service summary that outlines your AT&T service by AT&T features by e-mail or U.S. mail. This summary will include an activation fee. However, this does not apply to you, and you will not be charged. We do apologize for any confusion this may cause. Any further questions regarding this, please feel free to dial 611 from the AT&T handset, okay? Okay. And I'll be sending a return label as well for you to return the old device. I'm just going to verify where they want me to send the return label. Do you want me to send it via email or to your shipping address? Shipping. Okay. I'm just going to verify that it will be 98 Maston Drive, Belgrade, Montana, 59714. Is that correct? Yes. Okay. And is this the same address where I'm going to ship the Blackberry Torch? Yes. Okay. And also, once you receive the return label, just simply affix it to the phone box and drop it in any USPS blue box, okay? Drop it in what? In any USPS blue box. Okay. Okay. So, I'm done filling out all the information needed here for the exchange. Sir, do you have any questions regarding the information that I provided you, Mr. Milligan? No. Is there anything else I can help you with? I don't think so. Okay. We do value and appreciate your business. Thank you for calling AT&T, and have a great day. Thank you. Okay. Goodbye. Bye.
"""

print("Creating knowledge graph:")
create_knowledge_graph(text)

driver.close()
