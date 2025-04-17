from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from graph.utils import get_author_papers, get_paper_references, get_paper_details, get_paper_citations, get_recommendations
from graph.models import AuthorPapersCache, PaperCitationsCache, PaperDetailsCache, PaperRecommendationsCache, PaperReferencesCache

import dataclasses

# Create your views here.
@api_view(['GET'])
def details(request: Request) -> Response:
    if request.method == 'GET':
        if 'id' in request.query_params:
            paper_id = request.query_params['id']
            try:
                paper_details = PaperDetailsCache.objects.get(paper_id=paper_id)
                return Response(status=status.HTTP_200_OK, data=paper_details.details)
            except PaperDetailsCache.DoesNotExist:
                try:
                    paper = get_paper_details(paper_id)
                    paper = dataclasses.asdict(paper)
                    PaperDetailsCache.objects.create(paper_id=paper_id, details=paper)
                    return Response(status=status.HTTP_200_OK, data=paper)
                except Exception:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': 'Internal server error'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'id is required'})
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'only GET method is supported'})

@api_view(['GET'])
def references(request: Request) -> Response:
    if request.method == 'GET':
        if 'id' in request.query_params:
            paper_id = request.query_params['id']
            try:
                paper_references = PaperReferencesCache.objects.get(paper_id=paper_id)
                return Response(status=status.HTTP_200_OK, data=paper_references.references)
            except PaperReferencesCache.DoesNotExist:
                try:
                    references = get_paper_references(paper_id)
                    references = [dataclasses.asdict(reference) for reference in references]
                    PaperReferencesCache.objects.create(paper_id=paper_id, references=references)
                    return Response(status=status.HTTP_200_OK, data=references)
                except Exception as e:
                    print(e)
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': 'Internal server error'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'id is required'})
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'only GET method is supported'})

@api_view(['GET'])
def citations(request: Request) -> Response:
    if request.method == 'GET':
        if 'id' in request.query_params:
            paper_id = request.query_params['id']
            try:
                paper_citations = PaperCitationsCache.objects.get(paper_id=paper_id)
                return Response(status=status.HTTP_200_OK, data=paper_citations.citations)
            except PaperCitationsCache.DoesNotExist:
                try:
                    citations = get_paper_citations(paper_id)
                    citations = [dataclasses.asdict(citation) for citation in citations]
                    PaperCitationsCache.objects.create(paper_id=paper_id, citations=citations)
                    return Response(status=status.HTTP_200_OK, data=citations)
                except Exception:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': 'Internal server error'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'id is required'})
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'only GET method is supported'})

@api_view(['GET'])
def recommendations(request: Request) -> Response:
    if request.method == 'GET':
        if 'id' in request.query_params:
            paper_id = request.query_params['id']
            try:
                paper_recommendations = PaperRecommendationsCache.objects.get(paper_id=paper_id)
                return Response(status=status.HTTP_200_OK, data=paper_recommendations.recommendations)
            except PaperRecommendationsCache.DoesNotExist:
                try:
                    recommendations = get_recommendations(paper_id)
                    recommendations = [dataclasses.asdict(recommendation) for recommendation in recommendations]
                    PaperRecommendationsCache.objects.create(paper_id=paper_id, recommendations=recommendations)
                    return Response(status=status.HTTP_200_OK, data=recommendations)
                except Exception:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': 'Internal server error'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'id is required'})
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'only GET method is supported'})

@api_view(['GET'])
def author_papers(request: Request) -> Response:
    if request.method == 'GET':
        if 'id' in request.query_params:
            author_id = request.query_params['id']
            try:
                author_papers = AuthorPapersCache.objects.get(author_id=author_id)
                return Response(status=status.HTTP_200_OK, data=author_papers.papers)
            except AuthorPapersCache.DoesNotExist:
                print('does not exist')
                papers = get_author_papers(author_id)
                papers = [dataclasses.asdict(paper) for paper in papers]
                AuthorPapersCache.objects.create(author_id=author_id, papers=papers)
                return Response(status=status.HTTP_200_OK, data=papers)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'id is required'})
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'only GET method is supported'})
