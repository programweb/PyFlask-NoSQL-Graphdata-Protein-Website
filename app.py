from flask import Flask, request, render_template, abort, redirect, url_for
import pymongo
import datetime
import glob
from py2neo import Node, Graph, Relationship
from neo4j import GraphDatabase
neo_uri_scheme = 'bolt'
neo_host_name = 'localhost'
neo_port = '11003' #'11003'7687
neo_user = 'pyneouser'
neo_pw = 'ABC123abc'


class HelloWorldExample:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            return 'done'

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

# py2neo.authenticate("localhost:7474", "test")
# print(dir(py2neo))


app = Flask(__name__)
app.config.from_object('config')

connector = "mongodb://{}:{}@{}".format(
        app.config['MONGODB_USERNAME'],
        app.config['MONGODB_PASSWORD'],
        app.config['MONGODB_SERVER'] )

client = pymongo.MongoClient(connector)
db = client[ app.config['MONGODB_COLLECTION'] ]

def getCommon(ttl, rowspan):
#    if( ttl == 'Error' ):
#        return {'title': 'error', 'url': 'fff', 'rowspan': rowspan,
#            'techLogoList':[], 'genes':[]}
    
    url = request.url_rule.rule # /gene/<symbol> on gene page
    title = ttl
    techLogoPaths = glob.glob('static/images/tech_logos/*_sm*')
    techLogoList = [logo.replace('static/images/tech_logos/', '') for logo in techLogoPaths]
    genes = list( db.demo.find({}) )
    return {'title': title, 'url': url, 'rowspan': rowspan,
        'techLogoList':techLogoList, 'genes':genes}

# this takes over (the other 404 handler made earlier)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404top.html', title = '404'), 404

@app.route("/")
def main():
    d = getCommon('Homepage', 1)
    return render_template('main.html', d=d)

@app.route("/data-intensive")
def book():
    d = getCommon('book', 1)
    return render_template('data-intensive.html', d=d)

@app.route("/certs")
def certs():
    d = getCommon('certs', 1)
    return render_template('certs.html', d=d)
    
@app.route("/benefits")
def benefits():
    d = getCommon('benefits', 1)
    return render_template('benefits.html', d=d)
    
@app.route("/cstore")
def cstore():
    d = getCommon('Column Store', 1)
    return render_template('colstore.html', d=d)
    
@app.route("/netwk")
def netwk():
    d = getCommon('Network', 1)
    import requests
    import pandas as pd
    import networkx as nx
    import numpy as np
    import matplotlib.pyplot as plt
    # from nxviz.plots import CircosPlot
    import nxviz
    
    """
    x = np.linspace(0, 10, 20)
    y1 = x**2.0
    y2 = x**1.5
    plt.plot(x, y1, 'bo-', linewidth=2, markersize=12, label='First')
    plt.plot(x, y2, 'gs-', linewidth=2, markersize=12, label='Second')
    plt.xlabel('X')
    #Text(0.5, 0, 'X')
    plt.ylabel('Y')
    #Text(0, 0.5, 'Y')
    plt.axis([-0.5, 10.5, -5, 105])
    #[-0.5, 10.5, -5, 105]
    plt.legend(loc="upper left")
    #plt.savefig('myplot.pdf')
    plt.savefig('myplot.svg')
    """
    
    """
    protein_list = ['A2M','ABCB11','ABL1','ACKR3','ACTA1','ADAM9','ANKRD20A1',
               'AP2A2', 'ARHGAP30', 'ASPHD1', 'B2M', 'BCAS2', 'BEND2', 'BIVM',
               'BOK','BTLA','CCN4','CCN5','CCN6','CHCHD4']
    proteins = '%0d'.join(protein_list)
    url = 'https://string-db.org/api/tsv/network?identifiers=' + proteins + '&species=9606'
    r = requests.get(url)
    lines = r.text.split('\n') # pull the text from the response object and split based on ne
    data = [l.split('\t') for l in lines] # split each line into its components based on tabs
    # convert to dataframe using the first row as the column names; drop empty, final row
    df = pd.DataFrame(data[1:-1], columns = data[0])
    # dataframe with the preferred names of the two proteins and the score of the interaction
    interactions = df[['preferredName_A', 'preferredName_B', 'score']]
    G=nx.Graph(name='Protein Interaction Graph')
    interactions = np.array(interactions) # convert to array for clarity

    for i in range(len(interactions)):
        interaction = interactions[i]
        a = interaction[0] # protein a node
        b = interaction[1] # protein b node
        w = int(float(interaction[2])*100) # score as weighted edge
        if w > 70: # only keep high scoring edges (was 80 can go 5-94)
            G.add_weighted_edges_from([(a,b,w)])

    # c = CircosPlot(G,figsize=(20, 20),node_labels=True,fontsize=14)
    """
    
    return render_template('netwk.html', d=d)
    

@app.route("/graphdb", methods=['GET'])
def graphdb():
    d = getCommon('Graph Database', 1)
    return render_template('graphdb.html', d=d, result='')
    
@app.route("/graphdb/<cql>", methods=['GET'])
def graphdbDemo(cql):
    # p = pypher()
    rstr = cql
    rstr = "<div class='cline'>$ ./neo4j_001_enzyme-reactions.py</div>"  # doesn't work
    rstr = '$ ./neo4j_001_enzyme-reactions.py' # probably pass back a list and let Flask do the ordered list
    #greeter = HelloWorldExample("bolt://localhost:" + neo_port, neo_user, neo_pw)
    # rstr = greeter.get_greeting("Likhomo Abuti")
    #greeter.close()
    neo_port = '11003' #'11003'7687
    neo_user = 'pyneouser'
    neo_pw = 'ABC123abc'
    neo_db = 'test'
    
    # https://neo4j.com/docs/api/python-driver/4.3/api.html#api-documentation
    uri = "bolt://localhost:" + neo_port
    driver = GraphDatabase.driver(uri, auth=(neo_user, neo_pw))
    session = driver.session(database=neo_db)
    # result = session.run("MATCH (n) RETURN n LIMIT 1") # get a node regardless of db
    # result = session.run("MATCH (a:Person) RETURN a.name AS name")
    # names = [record["name"] for record in result]
    session.close()
    driver.close()
    
    cqlResult = rstr
    d = getCommon('Graph Database', 1)
    return render_template('graphdb.html', d=d, result=cqlResult)
    
@app.route("/goneo")
def goneo():
    return redirect('http://localhost:11004')

@app.route("/scipy")
def scipy():
    d = getCommon('Scientific Programming', 1)
    return render_template('scipy.html', d=d)
    
@app.route("/search", methods=['POST', 'GET'])
def search():
    if 'st' in request.form:
        search_terms = request.form['st'].upper()
        ttl = 'Gene Search Results'
        #doc = db.demo.find_one({'symbol' : {'$regex': search_terms}})
        docList = list( db.demo.find({'symbol':{'$regex':search_terms}}) )
        
        #import re
        #regx = re.compile("^A", re.IGNORECASE)
        #docList = list( db.demo.find({"symbol": regx}) )

        if bool(docList) or not search_terms: # AND doc is NOT '': # exact match
            error=''
        else:
            error='No results were found for that search'
            #    app.logger.info(doc)
            #    return redirect(url_for('person', idnum=doc["id"]) )
    else:
        error=''
        search_terms = ''
        ttl = 'Gene Search'
        docList = list({}) #TODO change name to results or something
        
    d = getCommon(ttl, 2)

    return render_template('search.html', d=d, error=error, search_terms=search_terms, docList=docList)
    #return render_template('search.html', d=d, error='No results were found for that search', search_terms=search_terms, doc=doc)

@app.route("/get", methods=['POST'])
def get():
    name = request.form['name']
    doc = db.people.find_one({'name' : {'$regex': name}})
    if doc:
        app.logger.info(doc)
        return redirect(url_for('person', idnum=doc["id"]) )
    return render_template('main.html', error="Could not find that person")

@app.route("/save", methods=['POST'])
def save():
    entry = {
        "name": request.form['name'],
        "email": request.form['email'],
        "id": request.form['idnum'],
        "when": datetime.datetime.now(),
    }
    res = db.people.insert(entry)
    db.people.create_index("id", unique=True)
    return render_template('main.html')

@app.route("/list_genes", methods=['GET'])
def list_genes():
    d = getCommon('Gene List', 1)
    count = db.demo.count_documents({})
    genes = db.demo.find({})
    hdrList = [ 'gene','protein','chromosome','group','product','ensembl',
                'enzymes','definition','note',"accession<br>interval",
                'omim']
    length = len(hdrList)
    return render_template( 'list_genes.html', count=count, genes=genes, d=d,
                            hdrList=hdrList, len=length)
    
@app.route("/nav", methods=['GET'])
def gene_links():
    count = db.demo.count_documents({})
    genes = db.demo.find({})
    return render_template('incl/nav.html', count=count, genes=genes)


@app.route("/gene/<symbol>", methods=['GET'])
def gene(symbol):
    d = getCommon('Gene: ' + symbol, 1)
    gene = db.demo.find_one({ 'symbol': symbol })
    if not gene:
        abort(404)
    return render_template('gene.html', d=d, gene=gene)
    
@app.route("/list", methods=['GET'])
def list_people():
    d = getCommon('List', 1)
    count = db.people.count_documents({})
    people = db.people.find({})
    return render_template('list.html', count=count, people=people, d=d)

@app.route("/person/<idnum>", methods=['GET'])
def person(idnum):
    d = getCommon('Person', 1)
    person = db.people.find_one({ 'id': idnum })
    if not person:
        abort(404)
    return render_template('person.html', person=person, d=d)




# old search
#@app.route("/get", methods=['POST'])
#def get():
#    name = request.form['name']
#    doc = db.people.find_one({'name' : {'$regex': name}})
#    if doc:
#        app.logger.info(doc)
#        return redirect(url_for('person', idnum=doc["id"]) )
#    return render_template('main.html', error="Could not find that person")
