from api.neo import neo
from utils.String import String


class Publication:
    # -
    neo = None

    # - Sciencedirect
    title = ""
    keywords = []
    abstract = ""
    abstTypes = []
    authors = []
    availableOnlineDate = ""
    cid = ""
    contentType = ""
    documentSubType = ""
    doi = ""
    openAccess = False
    openArchive = False
    itemStage = ""
    pages = {"first": "", "last": ""}
    articleNumber = ""
    pdf = {"filename": "", "getAccessLink": "", "downloadLink": ""}
    pii = ""
    publicationDate = ""
    publicationDateDisplay = ""
    sourceTitle = ""
    sortDate = ""
    thirdParty = False
    volumeIssue = ""
    articleType = ""
    score = 0
    issn = ""
    sourceTitleUrl = ""
    link = ""
    articleTypeDisplayName = ""

    def __init__(self):
        # Initialiser la connexion à Neo4j
        self.neo = neo()

    def sciencedirect(self, json):

        if "title" in json:
            self.title = String.addslashed(json["title"])
        if "abstTypes" in json:
            self.abstTypes = json["abstTypes"]
        if "authors" in json:
            self.authors = json["authors"]
        if "availableOnlineDate" in json:
            self.availableOnlineDate = json["availableOnlineDate"]
        if "cid" in json:
            self.cid = json["cid"]
        if "contentType" in json:
            self.contentType = String.addslashed(json["contentType"])
        if "documentSubType" in json:
            self.documentSubType = String.addslashed(json["documentSubType"])
        if "doi" in json:
            self.doi = json["doi"]
        if "openAccess" in json:
            self.openAccess = json["openAccess"]
        if "openArchive" in json:
            self.openArchive = json["openArchive"]
        if "itemStage" in json:
            self.itemStage = String.addslashed(json["itemStage"])
        if "pages" in json:
            self.pages = json["pages"]
        if "articleNumber" in json:
            self.articleNumber = json["articleNumber"]
        if "pdf" in json:
            self.pdf = json["pdf"]
        if "pii" in json:
            self.pii = json["pii"]
        if "publicationDate" in json:
            self.publicationDate = json["publicationDate"]
        if "publicationDateDisplay" in json:
            self.publicationDateDisplay = json["publicationDateDisplay"]
        if "sourceTitle" in json:
            self.sourceTitle = String.addslashed(json["sourceTitle"])
        if "sortDate" in json:
            self.sortDate = json["sortDate"]
        if "thirdParty" in json:
            self.thirdParty = json["thirdParty"]
        if "volumeIssue" in json:
            self.volumeIssue = json["volumeIssue"]
        if "articleType" in json:
            self.articleType = String.addslashed(json["articleType"])
        if "score" in json:
            self.score = json["score"]
        if "issn" in json:
            self.issn = json["issn"]
        if "sourceTitleUrl" in json:
            self.sourceTitleUrl = json["sourceTitleUrl"]
        if "link" in json:
            self.link = json["link"]
        if "articleTypeDisplayName" in json:
            self.articleTypeDisplayName = String.addslashed(json["articleTypeDisplayName"])

        return self

    def toObject(self):

        # Première page
        if 'first' in self.pages:
            page_first = self.pages['first']
        else:
            page_first = 0

        # Dernière page
        if 'last' in self.pages:
            page_last = self.pages['last']
        else:
            page_last = 0

        if 'filename' in self.pdf:
            pdf_filename = self.pdf['filename']
        else:
            pdf_filename = ""

        if 'getAccessLink' in self.pdf:
            pdf_access = self.pdf['getAccessLink']
        else:
            pdf_access = ""

        if 'downloadLink' in self.pdf:
            pdf_download = self.pdf['downloadLink']
        else:
            pdf_download = ""

        return {
            'title': self.title,
            'abstract': self.abstract,
            'availableOnlineDate': self.availableOnlineDate,
            'cid': self.cid,
            'contentType': self.contentType,
            'documentSubType': self.documentSubType,
            'doi': self.doi,
            'openAccess': str(self.openAccess),
            'openArchive': str(self.openArchive),
            'itemStage': self.itemStage,
            'pages_first': str(page_first),
            'pages_last': str(page_last),
            'articleNumber': self.articleNumber,
            'pdf_filename': pdf_filename,
            'pdf_access': pdf_access,
            'pdf_download': pdf_download,
            'pii': self.pii,
            'publicationDate': self.publicationDate,
            'publicationDateDisplay': self.publicationDateDisplay,
            'sourceTitle': self.sourceTitle,
            'sortDate': self.sortDate,
            'thirdParty': str(self.thirdParty),
            'volumeIssue': self.volumeIssue,
            'articleType': self.articleType,
            'score': str(self.score),
            'issn': self.issn,
            'sourceTitleUrl': self.sourceTitleUrl,
            'link': self.link,
            'articleTypeDisplayName': self.articleTypeDisplayName
        }

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

    def neo4j(self, query):

        # Créer un noeud
        self.neo.createNode("Publication", self.title, self.pii, self.toObject())

        # Créer la recherche
        self.neo.createNode("Query", String.addslashed(query), self.id(query))
        self.neo.createRelation("responseOf",
                                "Publication", {'pii': self.pii},
                                "Query", {'id': self.id(query)},
                                {'score': self.score})

        # Créer le type
        self.neo.createNode("ArticleType", String.addslashed(self.articleTypeDisplayName), self.id(self.articleType))
        self.neo.createRelation("articleIsTypeOf",
                                "Publication", {'pii': self.pii},
                                "ArticleType", {'id': self.id(self.articleType)})

        # Créer le type de content
        self.neo.createNode("ContentType", String.addslashed(self.contentType), self.id(self.contentType))
        self.neo.createRelation("contentIsTypeOf",
                                "Publication", {'pii': self.pii},
                                "ContentType", {'id': self.id(self.contentType)})

        # Pour tous les auteurs
        for author in self.authors:
            author_id = self.neo.id('author_' + author)
            # Créer un noeud
            self.neo.createNode("Author", author, author_id)
            # Lier l'auteur à la publication
            self.neo.createRelation("workedOn", "Author", {'id': author_id}, "Publication", {'pii': self.pii})

        # Pour tous les mots clés
        for keyword in self.keywords:
            keyword_id = self.neo.id('keyword_' + keyword)
            # Créer un noeud
            self.neo.createNode("Keyword", keyword, keyword_id)
            # Lier le mot clé à la publication
            self.neo.createRelation("hasKeyword",
                                    "Publication", {'pii': self.pii},
                                    "Keyword", {'id': keyword_id})

            # Lier le mot clé à la publication
            self.neo.createRelation("searchGiveKeyword",
                                    "Query", {'id': self.id(query)},
                                    "Keyword", {'id': keyword_id})
