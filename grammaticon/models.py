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
    quotation = Column(Unicode)
    comments = Column(Unicode)
    GOLD_counterpart = Column(Unicode)
    GOLD_URL = Column(Unicode)
    GOLD_comments = Column(Unicode)
    ISOCAT_counterpart = Column(Unicode)
    ISOCAT_URL = Column(Unicode)
    ISOCAT_comments = Column(Unicode)


@implementer(interfaces.IValue)
class Feature(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)


@implementer(interfaces.IParameter)
class Metafeature(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    area = Column(Unicode)


@implementer(interfaces.IContribution)
class Featurelist(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    year = Column(Unicode)
    url = Column(Unicode)
    number_of_features = Column(Integer)
    #id,name,URL,authors,number of features,year


class ConceptMetafeature(Base):
    concept_pk = Column(Integer, ForeignKey('concept.pk'))
    metafeature_pk = Column(Integer, ForeignKey('metafeature.pk'))

    concept = relationship(Concept, backref='metafeature_assocs')
    metafeature = relationship(Metafeature, backref='concept_assocs')
