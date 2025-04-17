import requests
from dataclasses import dataclass

@dataclass
class Author:
    author_id: str
    name: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(author_id=data['authorId'], name=data['name'])


@dataclass
class Paper:
    paper_id: str
    title: str
    year: int
    abstract: str
    authors: list[Author]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(paper_id=data['paperId'], title=data['title'], year=data['year'], abstract=data['abstract'], authors=[Author.from_dict(author) for author in data['authors']])


def get_author_papers(author_id: str) -> list[Paper]:
    url = f'https://api.semanticscholar.org/graph/v1/author/{author_id}/papers?fields=url,abstract,title,year,authors'
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return [Paper.from_dict(paper) for paper in response.json()['data']]
    raise Exception('Internal server error')

def get_paper_details(paper_id: str) -> Paper:
    url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=url,abstract,title,year,authors'
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return Paper.from_dict(response.json())
    raise Exception('Internal server error')

def get_paper_references(paper_id: str) -> list[Paper]:
    url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references?fields=url,abstract,title,year,authors'
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return [Paper.from_dict(paper['citedPaper']) for paper in response.json()['data']]
    raise Exception('Internal server error')

def get_paper_citations(paper_id: str) -> list[Paper]:
    url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations?fields=url,abstract,title,year,authors'
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return [Paper.from_dict(paper['citingPaper']) for paper in response.json()['data']]
    raise Exception('Internal server error')

def get_recommendations(paper_id: str) -> list[Paper]:
    url = f'https://api.semanticscholar.org/recommendations/v1/papers/forpaper/{paper_id}?fields=url,abstract,title,year,authors'
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return [Paper.from_dict(paper) for paper in response.json()['recommendedPapers']]
    raise Exception('Internal server error')
