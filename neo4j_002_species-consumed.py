#!/usr/bin/env python3

import neo4j

from neo4j import GraphDatabase

neo_port = '11003' #'11003'7687
neo_user = 'pyneouser' 
neo_pw = 'ABC123abc'
neo_db = 'test'

print('Query the Neo4j Database')
print('to find')
print('Species Consumed in Citric Acid Cycle')
print()

uri = "bolt://localhost:" + neo_port
driver = GraphDatabase.driver(uri, auth=(neo_user, neo_pw))

cypherQuery = """MATCH (m:Molecule)
           OPTIONAL MATCH p=(m)<-[:PRODUCES]-()
           OPTIONAL MATCH s=(m)-[:SUBSTRATE]->()
           WITH m, count(p) AS produced, count(s) AS consumed
           WHERE produced < consumed
           RETURN DISTINCT m.name AS species, produced - consumed AS net
           ORDER BY net ASC"""

def get_reacions(tx):
    result = tx.run(cypherQuery)
    return [r for r in result]

with driver.session(database=neo_db) as session:
    reactions = session.read_transaction(get_reacions)
    for reaction in reactions:
        print('species: ', reaction['species'], 'net: ', reaction['net'])
    print()

driver.close()

print()
print('Cypher Query Language:')
lines = [line.strip() for line in cypherQuery.split('\n')]
for line in lines:
    print(line)
print()
print()
