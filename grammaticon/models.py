from zope.interface import implementer
from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.source import HasSourceNotNullMixin
from clld.db.models.common import Contribution, Dataset, IdNameDescriptionMixin

from grammaticon.interfaces import IConcept, IFeature


@implementer(interfaces.IDataset)
class GrammaticonDataset(CustomModelMixin, Dataset):
    pk = Column(Integer, ForeignKey('dataset.pk'), primary_key=True)
    version = Column(Unicode)
    doi = Column(Unicode)
    repo = Column(Unicode)
    zenodo_concept_doi = Column(Unicode)


@implementer(IConcept)
class Concept(IdNameDescriptionMixin, Base):
    pk = Column(Integer, primary_key=True)
    comments = Column(Unicode)
    wikipedia_counterpart = Column(Unicode)
    wikipedia_url = Column(Unicode)
    sil_counterpart = Column(Unicode)
    sil_url = Column(Unicode)
    croft_counterpart = Column(Unicode)
    croft_definition = Column(Unicode)
    croft_url = Column(Unicode)
    quotation = Column(Unicode)
    in_degree = Column(Integer, default=0)
    out_degree = Column(Integer, default=0)
    number_of_features = Column(Integer, default=0)

    @property
    def parents(self):
        return [assoc.parent for assoc in self.parent_assocs]

    @property
    def children(self):
        return [assoc.child for assoc in self.child_assocs]


class ConceptRelation(Base):
    # FIXME: add a unique constraint!
    parent_pk = Column(Integer, ForeignKey('concept.pk'))
    child_pk = Column(Integer, ForeignKey('concept.pk'))

    parent = relationship(Concept, foreign_keys=[parent_pk], backref='child_assocs')
    child = relationship(Concept, foreign_keys=[child_pk], backref='parent_assocs')


class ConceptReference(Base, HasSourceNotNullMixin):
    concept_pk = Column(Integer, ForeignKey('concept.pk'), nullable=False)
    concept = relationship(Concept, innerjoin=True, backref='references')


@implementer(IFeature)
class Feature(IdNameDescriptionMixin, Base):
    contribution_pk = Column(Integer, ForeignKey('contribution.pk'))
    contribution = relationship(Contribution, backref='features')

    url = Column(Unicode)
    id_in_collection = Column(Unicode)
    number_of_languages = Column(Integer)
    comment = Column(Unicode)


@implementer(interfaces.IContribution)
class Collection(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    year = Column(Unicode)
    url = Column(Unicode)
    number_of_features = Column(Integer)
    contributor_list = Column(Unicode)


class ConceptFeature(Base):
    concept_pk = Column(Integer, ForeignKey('concept.pk'))
    feature_pk = Column(Integer, ForeignKey('feature.pk'))

    concept = relationship(Concept, backref='feature_assocs')
    feature = relationship(Feature, backref='concept_assocs')
