from sqlalchemy.orm import joinedload

from clld.db.models.common import Contribution
from clld.db.util import get_distinct_values
from clld.web.datatables.base import Col, DataTable, LinkCol, DetailsRowLinkCol
from clld.web.util.helpers import link, external_link
from clld.web.util.htmllib import HTML

from grammaticon import models


def _generate_separators(iterable):
    first_item = True
    for item in iterable:
        if first_item:
            first_item = False
        else:
            yield '; '
        yield item


def semicolon_separated_span(iterable):
    return HTML.span(*_generate_separators(iterable))


# TODO(johannes): un-dummy the columns and remove this
class DummyCol(Col):
    def format(*_args, **_kwargs):
        return ''


class FeatureConceptsCol(Col):
    """Column listing concepts for a given feature."""

    __kw__ = {'bSearchable': False, 'bSortable': False}

    def format(self, item):
        def _concept_label(c):
            return c.name or c.id or str(c)

        feature = self.get_obj(item)
        unique_concepts = {
            assoc.concept.pk: assoc.concept
            for assoc in feature.concept_assocs}
        concepts = sorted(unique_concepts.values(), key=_concept_label)
        return semicolon_separated_span(
            link(self.dt.req, concept, label=_concept_label(concept))
            for concept in concepts)


class ContributionCol(Col):
    def format(self, item):
        return link(self.dt.req, item, label=f'{item.name} features')


class Collections(DataTable):
    def col_defs(self):
        return [
            Col(self, 'name', sTitle='Collection name'),
            Col(self, 'year', model_col=models.Collection.year),
            ContributionCol(
                self, 'name', sTitle='Collection features',
                model_col=Contribution.name),
            Col(self, 'description', model_col=models.Collection.description),
            Col(self, 'contributor_list', sTitle='Feature contributors',
                model_col=models.Collection.contributor_list),
            Col(self,
                'number_of_features',
                sClass='right',
                bSearchable=False,
                input_size='mini',
                sTitle='#&nbsp;Features',
                model_col=models.Collection.number_of_features),
        ]

    def get_options(self):
        opts = super().get_options()
        opts['aaSorting'] = [[5, 'desc']]
        return opts


class SILLinkCol(Col):
    def format(self, item):
        if item.sil_url:
            return external_link(item.sil_url, label=item.sil_counterpart)
        else:
            return item.sil_counterpart


class WikiLinkCol(Col):
    def format(self, item):
        if item.wikipedia_url:
            return external_link(item.wikipedia_url, label=item.wikipedia_counterpart)
        else:
            return item.wikipedia_counterpart


class Concepts(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle='Concept name'),
            Col(self, 'description', sTitle='Definition'),
            WikiLinkCol(self, 'wikipedia_counterpart', sTitle='Wikipedia'),
            SILLinkCol(self, 'sil_counterpart', sTitle='SIL glossary'),
            Col(self, 'croft_definition', sTitle="Croft's comparative concept"),
            Col(self,
                'number_of_features',
                sClass='right',
                bSearchable=False,
                input_size='mini',
                sTitle='#&nbsp;Features',
                model_col=models.Concept.number_of_features),
            # Col(self, 'defined by', model_col=models.Concept.in_degree),
            # Col(self, 'defining', model_col=models.Concept.out_degree),
        ]


class Features(DataTable):
    __constraints__ = [Contribution]

    def base_query(self, query):
        if self.contribution:
            query = query.filter(
                models.Feature.contribution_pk == self.contribution.pk)
        else:
            query = query.join(models.Collection)

        query = query.options(
            joinedload(models.Feature.concept_assocs)
            .joinedload(models.ConceptFeature.concept))

        return query

    def col_defs(self):
        name = LinkCol(self, 'name', sTitle='Feature name')
        # TODO(johannes): fill with data
        languages = DummyCol(self, 'name', sTitle='Languages')
        contrib = LinkCol(
            self,
            'collection',
            model_col=Contribution.name,
            choices=get_distinct_values(Contribution.name),
            get_object=lambda o: o.contribution)
        concepts = FeatureConceptsCol(self, 'concepts', sTitle='Related concepts')
        if self.contribution:
            description = Col(self, 'description', sTitle='Feature description')
            return [name, description, concepts, languages]
        else:
            return [name, contrib, concepts]



class Sources(DataTable):

    """Default DataTable for Source objects."""

    __toolbar_kw__ = {'dl_formats': {'bib': 'BibTeX'}}

    def base_query(self, query):
        return query

    def col_defs(self):
        return [
            DetailsRowLinkCol(self, 'd'),
            LinkCol(self, 'name'),
            Col(self, 'description', sTitle='Title', format=lambda i: HTML.span(i.description)),
            Col(self, 'year'),
            Col(self, 'author'),
        ]


def includeme(config):
    config.register_datatable('concepts', Concepts)
    config.register_datatable('features', Features)
    config.register_datatable('contributions', Collections)
    config.register_datatable('sources', Sources)
