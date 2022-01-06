from neo4j import GraphDatabase
import re
import time

from utils.Terminal import Terminal


class neo:
    # Connexion à la base
    driver = None

    # Identifiant de connexion
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "123456"
    database = "neo4j"

    # 1) On s'assure qu'on a les bons identifiants

    # Constructeur
    def __init__(self):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    # Fermer la connexion
    def close(self):
        self.driver.close()

    # Créer un identifiant
    def id(self, str, replace="_"):
        tmp = str.lower()
        tmp = tmp.replace(' ', replace)
        tmp = tmp.replace('.', replace)
        tmp = tmp.replace('-', replace)
        tmp = tmp.replace("'", replace)
        tmp = tmp.replace('"', replace)
        tmp = tmp.replace("_", replace)
        return tmp

    # Escape String
    def escape(self, str):
        tmp = re.sub(re.compile('<.*?>'), '', str)
        tmp = tmp.replace('"', '\\"')
        tmp = tmp.replace('.', '\\.')
        tmp = tmp.replace("'", "\\'")
        return tmp

    # Créer un noeud
    def createNode(self, node="", name="", id="", params={}):
        with self.driver.session(database=self.database) as session:

            # Préparer la requête
            request = 'MERGE ( n:' + node + ' {id: "' + str(id) + '"}) ON CREATE '
            request += 'SET n.name = "' + str(name) + '", '
            request += 'n.created = ' + str(time.time()) + ' '

            # Ajouter les paramètres
            if len(params) > 0:
                # request += 'ON MATCH SET '
                request += 'SET n.updated = ' + str(time.time()) + ', '
                for param in params:
                    request += ' n.' + param + ' = "' + str(params[param]) + '", '

            # Finaliser la requête
            request += ";"
            request = request.replace(', ;', ';')

            # Lancer la requête
            session.run(request)

            # Création du noeud
            #Terminal.subtitle("Noeud (" + node + ") : " + name)

    # Créer un lien entre 2 noeuds
    def createRelation(self, relation="", node1="", params1={}, node2="", params2={}, attr={}):
        with self.driver.session(database=self.database) as session:

            # Rechercher le premier noeud
            request = "MATCH (a:" + node1 + " {"
            if len(params1) > 0:
                for param in params1:
                    request += param + ': "' + str(params1[param]) + '", '

            # Rechercher le second noeud
            request += "}), (b:" + node2 + " {"
            if len(params2) > 0:
                for param in params2:
                    request += param + ': "' + str(params2[param]) + '", '

            params = ""

            # Ajouter la relation
            request += "}) MERGE (a)-[rel:" + relation + "]->(b)"

            # Ajouter les paramètres
            if len(attr) > 0:
                #params += " {"
                for a in attr:
                    params += "SET rel." + a + ' = "' + str(attr[a]) + '" '
                # params += "}"


            # Nettoyer la requête
            request = request.replace(', }', '}')

            # Lancer la requête
            session.run(request)

            # Création d'une relation
            #Terminal.subsubtitle("Relation (" + relation + ") : " +  node1 + " <--> " + node2)
