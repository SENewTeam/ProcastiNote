# backend/paperInfo/specifications.py

from django.db.models import Q

class Specification:
    def as_q(self) -> Q:
        """Return a Django Q object for this specification."""
        raise NotImplementedError("Subclasses must implement as_q()")

    def __and__(self, other: 'Specification') -> 'Specification':
        return AndSpecification(self, other)

    def __or__(self, other: 'Specification') -> 'Specification':
        return OrSpecification(self, other)


class AndSpecification(Specification):
    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right

    def as_q(self) -> Q:
        return self.left.as_q() & self.right.as_q()


class OrSpecification(Specification):
    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right

    def as_q(self) -> Q:
        return self.left.as_q() | self.right.as_q()


class PaperNameSpecification(Specification):
    def __init__(self, paper_name: str):
        self.paper_name = paper_name

    def as_q(self) -> Q:
        return Q(title__icontains=self.paper_name)


class AuthorSpecification(Specification):
    def __init__(self, author: str):
        self.author = author

    def as_q(self) -> Q:
        return Q(authors__icontains=self.author)


class VenueTypeSpecification(Specification):
    def __init__(self, venue_type: str):
        self.venue_type = venue_type

    def as_q(self) -> Q:
        return Q(venue_type__iexact=self.venue_type)


class YearSpecification(Specification):
    def __init__(self, year: int):
        self.year = year

    def as_q(self) -> Q:
        return Q(year=self.year)
