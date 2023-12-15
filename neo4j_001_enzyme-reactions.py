#!/usr/bin/env python3

import neo4j

from neo4j import GraphDatabase

neo_port = '11003' # 11003  7687
neo_user = 'pyneouser' 
neo_pw = 'ABC123abc'
neo_db = 'test'

enzymes = ['α-Ketoglutarate dehydrogenase', 'Aconitase', 'Citrate synthase',
        'Fumarase', 'Isocitrate dehydrogenase', 'Malate dehydrogenase',
        'Succinyl-CoA synthetase']
print('Query the Neo4j Database')
print('to find')
print('Enzyme-associated Reactions in Citric Acid Cycle')
print()
print('Enzymes in Citric Acid Cycle: ')
print( enzymes )
print()

uri = "bolt://localhost:" + neo_port
driver = GraphDatabase.driver(uri, auth=(neo_user, neo_pw))

def get_reacions(tx, name):

    query = """MATCH (y:Enzyme)-[:CATALYSES]->(x)
               WHERE y.name = $name
               RETURN x.name AS reaction"""

    result = tx.run(query, name=name)
    return [r["reaction"] for r in result]

with driver.session(database=neo_db) as session:
    for i,enzyme in enumerate(enzymes):
        print(enzyme)
        reactions = session.read_transaction(get_reacions, enzyme)
        for reaction in reactions:
            print('-- ', reaction)
        print()

driver.close()

print()
print("In the Neo4J Browser run Cypher Query Language to see the Graph Visualization")
print("MATCH p=()-[r:CATALYSES]->() RETURN p")
print()
print()
