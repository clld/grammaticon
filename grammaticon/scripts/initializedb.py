import re
import unicodedata
from collections import Counter
from itertools import islice
from pathlib import Path

import sqlalchemy
from nameparser import HumanName

from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import EntryType
from csvw import dsv
from simplepybtex.database import parse_file

import grammaticon
from grammaticon import models


def drop_column_header(iterable, column_order):
    header = next(iterable)
    if header == column_order:
        return islice(iterable, 1, None)
    else:
        raise ValueError(
            f'wrong column order: {header!r} != {column_order!r}')


def slug(s, remove_whitespace=True, lowercase=True):
    return ''.join(
        c.lower() if lowercase else c
        for c in unicodedata.normalize('NFKD', s)
        if c.isascii() and (not remove_whitespace or not c.isspace()))


def iter_list_authors(ls):
    return (
        trimmed_name
        for name in ls.get('Authors', '').replace('et al.', '').split(',')
        if (trimmed_name := name.strip()))


def normalise_name(name):
    name = HumanName(name.strip())
    return slug(f'{name.last}{name.first}')


def make_contributors(csv_feature_lists):
    # explicitly add the editors
    full_names = {'Martin Haspelmath', 'Robert Forkel'}
    full_names.update(
        name
        for ls in csv_feature_lists
        for name in iter_list_authors(ls))
    return {
        (id_ := normalise_name(full_name)): common.Contributor(
            id=id_,
            name=full_name)
        for full_name in sorted(full_names)}


def iter_contribution_contributors(
    csv_feature_lists, feature_lists, contributors,
):
    list_authors = (
        (ls['ID'], number, normalise_name(author))
        for ls in csv_feature_lists
        for number, author in enumerate(iter_list_authors(ls), 1))
    return (
        common.ContributionContributor(
            contribution_pk=feature_lists[list_id].pk,
            contributor_pk=contributors[author_id].pk,
            ord=number)
        for list_id, number, author_id in list_authors)


def maybe_int(s):
    if s is None:
        return None
    else:
        return int(s)


def make_featurelists(csv_feature_lists):
    return {
        ls['ID']: models.FeatureList(
            id=slug(ls['Name']),
            name=ls['Name'],
            url=ls.get('URL'),
            number_of_features=maybe_int(ls.get('Number_of_Features')),
            year=ls.get('Year'))
        for ls in csv_feature_lists}


def make_metafeatures(csv_metafeatures):
    return {
        mf['ID']: models.Metafeature(
            id=mf['ID'],
            name=mf['Name'],
            area=mf.get('Feature_Area'))
        for mf in csv_metafeatures}


def make_valuesets(csv_features, feature_lists, metafeatures, dummy_language):
    return {
        (feature['Feature_List_ID'], feature['Metafeature_ID']):
        common.ValueSet(
            id='{}-{}'.format(
                (mf_pk := metafeatures[feature['Metafeature_ID']].pk),
                (list_pk := feature_lists[feature['Feature_List_ID']].pk)),
            language_pk=dummy_language.pk,
            contribution_pk=list_pk,
            parameter_pk=mf_pk)
        for feature in csv_features}


def iter_features(csv_features, valuesets):
    return (
        models.Feature(
            id=slug(feature['ID']),
            name=feature.get('Name') or feature['ID'],
            description=feature.get('Description'),
            valueset_pk=valuesets[feature['Feature_List_ID'], feature['Metafeature_ID']].pk)
        for feature in csv_features)


def make_concepts(csv_concepts, csv_features, csv_concept_metafeatures):
    metafeature_features = Counter(f['Metafeature_ID'] for f in csv_features)
    concept_features = {}
    for assoc in csv_concept_metafeatures:
        concept_id = assoc['Concept_ID']
        metafeature_id = assoc['Metafeature_ID']
        count = concept_features.get(concept_id) or 0
        concept_features[concept_id] = count + metafeature_features[metafeature_id]
    return {
        concept['ID']: models.Concept(
            id=concept['ID'],
            name=concept['Name'],
            description=concept.get('Description'),
            comments=concept.get('Comment'),
            wikipedia_counterpart=concept.get('Wikipedia_Counterpart'),
            wikipedia_url=concept.get('Wikipedia_URL'),
            sil_counterpart=concept.get('SIL_Counterpart'),
            sil_url=concept.get('SIL_URL'),
            croft_counterpart=concept.get('Croft_counterpart'),
            croft_definition=concept.get('Croft_definition'),
            quotation=concept.get('Quotation'),
            number_of_features=concept_features.get(concept['ID']))
        for concept in csv_concepts}


def make_sources(bibtex_sources):
    sources = {}
    for record in bibtex_sources.entries.values():
        authors = record.persons.get('author')
        author = ' and '.join(map(str, authors)) if authors else None
        editors = record.persons.get('editor')
        editor = ' and '.join(map(str, editors)) if editors else None

        # I don't like mutating the function parameters
        fields = {k.lower(): v for k, v in record.fields.items()}

        id_ = record.key
        bibtex_type = EntryType.from_string(record.type)
        year = record.fields.pop('year', None)
        title = record.fields.pop('title', None)
        type_ = record.fields.pop('type', None)
        booktitle = record.fields.pop('booktitle', None)
        pages = record.fields.pop('pages', None)
        edition = record.fields.pop('edition', None)
        journal = record.fields.pop('journal', None)
        school = record.fields.pop('school', None)
        address = record.fields.pop('address', None)
        url = record.fields.pop('url', None)
        note = record.fields.pop('note', None)
        number = record.fields.pop('number', None)
        series = record.fields.pop('series', None)
        volume = record.fields.pop('volume', None)
        publisher = record.fields.pop('publisher', None)
        organisation = record.fields.pop('organization', None)
        chapter = record.fields.pop('chapter', None)
        howpublished = record.fields.pop('howpublished', None)

        # dump the leftovers into jsondata
        jsondata = fields

        if (persons := authors or editors):
            authoryear = '{} {}'.format(' '.join(persons[0].last_names), year)
        else:
            auhoryear = year
        try:
            year_int = int(year or '', 10)
        except ValueError:
            year_int = None
        try:
            startpage = pages.split('-', maxsplit=1)[0].strip() if pages else ''
            startpage_int = int(startpage, 10)
        except ValueError:
            startpage_int = None
        try:
            pages_int = int(pages or '', 10)
        except ValueError:
            pages_int = None

        sources[record.key.lower()] = common.Source(
            id=id_,
            name=authoryear,
            bibtex_type=bibtex_type,
            author=author,
            editor=editor,
            # explicitly drop falsey values like empty strings
            year=year or 'nd',
            title=title or None,
            type=type_ or None,
            booktitle=booktitle or None,
            pages=pages or None,
            edition=edition or None,
            journal=journal or None,
            school=school or None,
            address=address or None,
            url=url or None,
            note=note or None,
            number=number or None,
            series=series or None,
            volume=volume or None,
            publisher=publisher or None,
            organization=organisation or None,
            chapter=chapter or None,
            howpublished=howpublished or None,
            year_int=year_int,
            startpage_int=startpage_int,
            pages_int=pages_int,
            jsondata=jsondata)
    return sources


def iter_concept_metafeatures(
    csv_concept_metafeatures, concepts, metafeatures,
):
    return (
        models.ConceptMetafeature(
            concept_pk=concepts[assoc['Concept_ID']].pk,
            metafeature_pk=metafeatures[assoc['Metafeature_ID']].pk)
        for assoc in csv_concept_metafeatures)


def iter_concept_relations(csv_concept_pairs, concepts):
    return (
        models.ConceptRelation(
            child_pk=concepts[child].pk,
            parent_pk=concepts[parent].pk)
        for child, parent in csv_concept_pairs)


def iter_concept_references(csv_concepts, concepts, sources):
    for csv_concept in csv_concepts:
        if (source_str := csv_concept.get('Source')):
            for ref in re.split(r'\s*;\s*', source_str):
                source_id, context = re.fullmatch(
                    r'\s*([^]]+)(?:\[([^]]*)\])?\s*', ref).groups()
                if (source := sources.get(source_id.lower())):
                    yield models.ConceptReference(
                        concept_pk=concepts[csv_concept['ID']].pk,
                        source_pk=source.pk,
                        key=source_id,
                        description=context)


def main(_args):
    # read data

    # cd from `somewhere/<repo>/grammaticon/scripts/initializedb.py`
    # to `somewhere/grammaticon-data/csvw`
    # FIXME: There Must Be a Better Way™
    csvw_folder = (
        Path(__file__).parent.parent.parent.parent
        / 'grammaticon-data' / 'csvw')

    csv_feature_lists = [
        {k: v for k, v in row.items() if v}
        for row in dsv.reader(csvw_folder / 'feature-lists.csv', dicts=True)]
    csv_metafeatures = [
        {k: v for k, v in row.items() if v}
        for row in dsv.reader(csvw_folder / 'metafeatures.csv', dicts=True)]
    csv_features = [
        {k: v for k, v in row.items() if v}
        for row in dsv.reader(csvw_folder / 'features.csv', dicts=True)]
    csv_concepts = [
        {k: v for k, v in row.items() if v}
        for row in dsv.reader(csvw_folder / 'concepts.csv', dicts=True)]
    csv_concept_metafeatures = [
        {k: v for k, v in row.items() if v}
        for row in dsv.reader(
            csvw_folder / 'concepts-metafeatures.csv', dicts=True)]
    csv_concept_hierarchy = list(drop_column_header(
        dsv.reader(csvw_folder / 'concept-hierarchy.csv'),
        ['Child_ID', 'Parent_ID']))
    bibtex_sources = parse_file(str(csvw_folder / 'sources.bib'))

    # fill data base

    dataset = common.Dataset(
        id=grammaticon.__name__,
        name="Grammaticon",
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='grammaticon.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    DBSession.add(dataset)

    contributors = make_contributors(csv_feature_lists)
    DBSession.add_all(contributors.values())

    feature_lists = make_featurelists(csv_feature_lists)
    DBSession.add_all(feature_lists.values())

    metafeatures = make_metafeatures(csv_metafeatures)
    # TODO: remove this hack when the data curation code produces unique names
    DBSession.execute(sqlalchemy.text("""
        ALTER TABLE parameter DROP CONSTRAINT parameter_name_key;
    """))
    DBSession.add_all(metafeatures.values())

    concepts = make_concepts(csv_concepts, csv_features, csv_concept_metafeatures)
    DBSession.add_all(concepts.values())

    sources = make_sources(bibtex_sources)
    DBSession.add_all(sources.values())

    dummy_language = common.Language(name='English')
    DBSession.add(dummy_language)

    # NOTE: Flushing to make sure primary keys are assigned.
    DBSession.flush()

    DBSession.add_all(
        common.Editor(
            dataset_pk=dataset.pk,
            contributor_pk=contributors[eid].pk,
            ord=number)
        for number, eid in enumerate(['haspelmathmartin', 'forkelrobert'], 1))
    DBSession.add_all(iter_contribution_contributors(
        csv_feature_lists, feature_lists, contributors))

    DBSession.add_all(iter_concept_metafeatures(
        csv_concept_metafeatures, concepts, metafeatures))
    DBSession.add_all(iter_concept_relations(csv_concept_hierarchy, concepts))
    DBSession.add_all(iter_concept_references(csv_concepts, concepts, sources))

    valuesets = make_valuesets(
        csv_features, feature_lists, metafeatures, dummy_language)
    DBSession.add_all(valuesets.values())

    # NOTE: Flushing to make sure primary keys are assigned.
    DBSession.flush()

    DBSession.add_all(iter_features(csv_features, valuesets))


def prime_cache(_args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for param in DBSession.query(models.Metafeature):
        param.representation = len({a.contribution_pk for a in param.valuesets})

    for concept in DBSession.query(models.Concept):
        concept.in_degree = len(concept.parents)
        concept.out_degree = len(concept.children)
