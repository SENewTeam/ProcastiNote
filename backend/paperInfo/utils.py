import requests
from .serializers import *
from nltk import FreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer

import spacy
stopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

nlp = spacy.load("en_core_web_sm")

def paperInfo(id):
    print(id)
    if id:
        paper_id = id
        paper = PaperInfo.get_paper_by_id(paper_id)
        print(id)
        if paper != None :
            print("From DB")
            paper_info = {
                    'paperId': paper.paperId,
                    'title': paper.title,
                    'abstract': paper.abstract,
                    'year': paper.year,
                    'authors': paper.authors,
                    'keywords':paper.keywords,
                    'paperPdf': paper.paperPdf,
                    # 'authors':author_names,
                    'venue': paper.venue,
                    'venue_type': paper.venue_type,
                    'venue_link': paper.venue_link,
                }
            return paper_info
        else :
            print("From API")
            url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,abstract,year,authors,venue,publicationVenue,tldr,externalIds'
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
                data = response.json()
                print(data)
                keywords = []
                keywordGenerationText = data['abstract'] if data['abstract'] else data['title']
                print(keywordGenerationText)
                keywords = extract_keywords(keywordGenerationText)
                print("Keywords:", keywords)

                author_names = ''
                # print("--------------------------------------------------")
                for author in data['authors']:
                    author_names += author['name'] + ', '
                
                abstract = data['abstract'] if data['abstract'] else ""
                tldr = data['tldr']['text'] if data['tldr'] and data['tldr']['text'] else ""
                # print("-_-_---------", abstract)
                # print("__________", tldr)
                paper_info = {
    'paperId': data['paperId'],
    'title': data['title'],
    'abstract': abstract + "\n " + tldr,
    'year': data['year'] if data['year'] else '',
    'authors': ', '.join(author['name'] for author in data['authors']),
    'keywords': ','.join(keyword for keyword in keywords),
    'paperPdf': (
        "https://arxiv.org/pdf/" + data['externalIds']['ArXiv'] + ".pdf"
        if 'ArXiv' in data['externalIds'] else
        f"https://sci-hub.se/{data['externalIds']['DOI']}" if 'DOI' in data['externalIds'] else ""
    ) or "",
    'venue': data['venue'] if data['venue'] else "",
    'venue_type': data['publicationVenue']['type'] if data['publicationVenue'] and 'type' in data['publicationVenue'] else "conference",
    'venue_link': data['publicationVenue']['url'] if data['publicationVenue'] and 'url' in data['publicationVenue'] else "/",
}
                # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                # print("paperPdf:", paper_info['paperPdf'])
                # print("venue:", paper_info['venue'])
                # print("venue_link:", paper_info['venue_link'])
                # print("--------------------------------------------------")
                serializer = PaperInfoSerializer(data=paper_info)
                if serializer.is_valid():
                    serializer.save()
                else:
                    data = {'error': f'Invalid data: {serializer.errors}'}
                    return data
                # print("-**************-------------------------------------")
                    
            except requests.exceptions.RequestException as e:
                data = {'error': f'Error fetching data: {e}'}
                return data
                
        return paper_info
            
    return {'error': 'Id required'}

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
