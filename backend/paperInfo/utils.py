import requests
from .serializers import *
from nltk import FreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer

import spacy
stopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

nlp = spacy.load("en_core_web_sm")


import requests
from .serializers import *
from nltk import FreqDist

# --- Chain of Responsibility Base Class ---
class PaperHandler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, paper_id):
        raise NotImplementedError("Must override handle method in subclass")


# --- Handler 1: Check in Database ---
class DatabaseHandler(PaperHandler):
    def handle(self, paper_id):
        paper = PaperInfo.get_paper_by_id(paper_id)
        if paper:
            print("From DB")
            return {
                'paperId': paper.paperId,
                'title': paper.title,
                'abstract': paper.abstract,
                'year': paper.year,
                'authors': paper.authors,
                'keywords': paper.keywords,
                'paperPdf': paper.paperPdf,
                'venue': paper.venue,
                'venue_type': paper.venue_type,
                'venue_link': paper.venue_link,
            }
        elif self._successor:
            return self._successor.handle(paper_id)
        return {'error': 'Paper not found in database'}


# --- Handler 2: Fetch from Semantic Scholar API ---
class APIHandler(PaperHandler):
    def handle(self, paper_id):
        print("From API")
        url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,abstract,year,authors,venue,publicationVenue,tldr,externalIds'
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return self._successor.handle((paper_id, data)) if self._successor else data
        except requests.exceptions.RequestException as e:
            return {'error': f'Error fetching data from API: {e}'}


# --- Handler 3: Extract, Serialize, and Save ---
class SerializationHandler(PaperHandler):
    def handle(self, input_data):
        paper_id, data = input_data

        keyword_text = data.get('abstract') or data.get('title', '')
        keywords = extract_keywords(keyword_text)

        abstract = data.get('abstract', "")
        tldr = data.get('tldr', {}).get('text', "")
        paper_info = {
            'paperId': data['paperId'],
            'title': data['title'],
            'abstract': abstract + "\n " + tldr,
            'year': data.get('year', ''),
            'authors': ', '.join(author['name'] for author in data.get('authors', [])),
            'keywords': ','.join(keywords),
            'paperPdf': (
                f"https://arxiv.org/pdf/{data['externalIds']['ArXiv']}.pdf"
                if 'ArXiv' in data['externalIds'] else
                f"https://sci-hub.se/{data['externalIds']['DOI']}"
                if 'DOI' in data['externalIds'] else ""
            ),
            'venue': data.get('venue', ''),
            'venue_type': data.get('publicationVenue', {}).get('type', "conference"),
            'venue_link': data.get('publicationVenue', {}).get('url', "/"),
        }

        serializer = PaperInfoSerializer(data=paper_info)
        if serializer.is_valid():
            serializer.save()
        else:
            return {'error': f'Invalid data: {serializer.errors}'}

        return paper_info


# --- Adapter: Connect Chain to paperInfo() ---
class PaperInfoAdapter:
    def __init__(self):
        self.handler_chain = DatabaseHandler(
            APIHandler(
                SerializationHandler()
            )
        )

    def get_paper_info(self, paper_id):
        return self.handler_chain.handle(paper_id)


# --- Entry Point (DO NOT CHANGE FUNCTION SIGNATURE) ---
def paperInfo(id):
    print(id)
    if id:
        adapter = PaperInfoAdapter()
        return adapter.get_paper_info(id)
    return {'error': 'Id required'}


# --- Keyword Extraction Utility ---
# def extract_keywords(text):
#     words = text.split()
#     words = [word.lower() for word in words if word.isalpha()]
#     freq_dist = FreqDist(words)
#     return [word for word, _ in freq_dist.most_common(5)]


def extract_keywords(abstract):
    words = abstract.split()

    stop_words = stopWords
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    print("1-------------------------------------------------")
    print(type(nlp))
    # print(nlp[:100])
    doc = nlp(' '.join(words))

    print("2-------------------------------------------------")
    print(type(doc))
    print(doc)
    
    pos_tags = [(token.text, token.pos_) for token in doc]

    print("3-------------------------------------------------")
    print(type(pos_tags))
    print(pos_tags[:100])
    
    keywords = [word for word, pos in pos_tags if pos.startswith('N') or pos.startswith('J')]

    print("4-------------------------------------------------")
    print(type(keywords))
    print(keywords[:100])
    freq_dist = FreqDist(keywords)

    num_keywords = 5
    top_keywords = [word for word, freq in freq_dist.most_common(num_keywords)]

    return top_keywords