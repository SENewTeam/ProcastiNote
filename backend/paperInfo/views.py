# views.py
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from .models import PaperInfo
from .serializers import *
from nltk import FreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer

import spacy
stopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

# Load the English language model from spaCy
nlp = spacy.load("en_core_web_sm")

@api_view(['GET'])
def paperInfo(request):
    if request.method == 'GET':
        if 'id' in request.query_params:
            paper_id = request.query_params['id']
            paper = PaperInfo.get_paper_by_id(paper_id)
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
                return Response(status=status.HTTP_200_OK, data=paper_info)
            else :
                print("From API")
                url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,abstract,year,authors,venue,publicationVenue,tldr,externalIds'

                try:
                    response = requests.get(url, timeout=5)
                    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
                    data = response.json()
                    keywords = []
                    keywords = extract_keywords(data['abstract'])
                    print("Keywords:", keywords)

                    author_names = ''
                    for author in data['authors']:
                        author_names += author['name'] + ', '
                    paper_info = {
                        'paperId': data['paperId'],
                        'title': data['title'],
                        'abstract': data['abstract'] + "\n. It means : " + data['tldr']['text'],
                        'year': data['year'],
                        'authors': ', '.join(author['name'] for author in data['authors']),
                        'keywords':','.join(keyword for keyword in keywords),
                        'paperPdf': "https://arxiv.org/pdf/" + data['externalIds']['ArXiv'] + ".pdf",
                        # 'authors':author_names,
                        'venue': data['venue'],
                        'venue_type': data['publicationVenue']['type'],
                        'venue_link': data['publicationVenue']['url'],
                    }
                    serializer = PaperInfoSerializer(data=paper_info)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': f'Invalid data: {serializer.errors}'})
                    
                except requests.exceptions.RequestException as e:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': f'Error fetching data: {e}'})
                
                return Response(status=status.HTTP_200_OK, data=paper_info)
            
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Id required'})
    
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Only GET request is supported'})



def extract_keywords(abstract):
    words = abstract.split()

    # Remove stopwords (common words that usually don't carry much meaning)
    stop_words = stopWords
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    # Part-of-speech tagging to identify nouns and adjectives
    # pos_tags = pos_tag(words)
    doc = nlp(' '.join(words))

    # Extract part-of-speech tags
    pos_tags = [(token.text, token.pos_) for token in doc]


    # Filter out non-noun and non-adjective words
    keywords = [word for word, pos in pos_tags if pos.startswith('N') or pos.startswith('J')]

    # Calculate word frequency to identify important words
    freq_dist = FreqDist(keywords)

    # Choose the top N words as keywords
    num_keywords = 5
    top_keywords = [word for word, freq in freq_dist.most_common(num_keywords)]

    return top_keywords
