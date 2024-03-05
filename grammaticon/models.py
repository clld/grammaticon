from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import (
    Parameter, ValueSet, Value, Contribution, IdNameDescriptionMixin,
    ContributionContributor
)
from grammaticon.interfaces import IConcept


@implementer(IConcept)
class Concept(IdNameDescriptionMixin, Base):
    pk = Column(Integer, primary_key=True)
    quotation = Column(Unicode)
    comments = Column(Unicode)
    GOLD_counterpart = Column(Unicode)
    GOLD_URL = Column(Unicode)
    GOLD_comment = Column(Unicode)
    ISOCAT_counterpart = Column(Unicode)
    ISOCAT_URL = Column(Unicode)
    ISOCAT_comments = Column(Unicode)
    in_degree = Column(Integer, default=0)
    out_degree = Column(Integer, default=0)

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


@implementer(interfaces.IValue)
class Feature(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)


@implementer(interfaces.IParameter)
class Metafeature(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    area = Column(Unicode)
    representation = Column(Integer, default=0)


@implementer(interfaces.IContribution)
class FeatureList(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    year = Column(Unicode)
    url = Column(Unicode)
    number_of_features = Column(Integer)


class ConceptMetafeature(Base):
    concept_pk = Column(Integer, ForeignKey('concept.pk'))
    metafeature_pk = Column(Integer, ForeignKey('metafeature.pk'))

    concept = relationship(Concept, backref='metafeature_assocs')
    metafeature = relationship(Metafeature, backref='concept_assocs')
