import re
import unicodedata
from collections import Counter
from itertools import islice
from pathlib import Path

from nameparser import HumanName

from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
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


ID_CHARS = (
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '0123456789-_ \t\n')


def slug(s, remove_whitespace=True, lowercase=True):
    return ''.join(
        c.lower() if lowercase else c
        for c in unicodedata.normalize('NFKD', s)
        if c in ID_CHARS and (not remove_whitespace or not c.isspace()))


def iter_list_authors(coll):
    return (
        trimmed_name
        for name in coll.get('Authors', '').replace('et al.', '').split(',')
        if (trimmed_name := name.strip()))


def normalise_name(name):
    name = HumanName(name.strip())
    return slug(f'{name.last}{name.first}')


def make_contributors(csv_collections):
    # explicitly add the editors
    full_names = {'Martin Haspelmath', 'Johannes Englisch'}
    full_names.update(
        name
        for coll in csv_collections
        for name in iter_list_authors(coll))
    return {
        (id_ := normalise_name(full_name)): common.Contributor(
            id=id_,
            name=full_name)
        for full_name in sorted(full_names)}


def iter_contribution_contributors(csv_collections, collections, contributors):
    list_authors = (
        (coll['ID'], number, normalise_name(author))
        for coll in csv_collections
        for number, author in enumerate(iter_list_authors(coll), 1))
    return (
        common.ContributionContributor(
            contribution_pk=collections[list_id].pk,
            contributor_pk=contributors[author_id].pk,
            ord=number)
        for list_id, number, author_id in list_authors)


def make_collections(csv_collections, csv_features):
    collection_features = Counter(f['Collection_ID'] for f in csv_features)
    return {
        coll['ID']: models.Collection(
            id=slug(coll['Name']),
            name=coll['Name'],
            description=coll.get('Description'),
            url=coll.get('URL'),
            number_of_features=collection_features[coll['ID']],
            year=coll.get('Year'),
            contributor_list=coll.get('Contributors'))
        for coll in csv_collections}


def make_concepts(csv_concepts, csv_concept_features):
    feature_counts = Counter(cf['Concept_ID'] for cf in csv_concept_features)
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
            croft_url=concept.get('Croft_URL'),
            quotation=concept.get('Quotation'),
            number_of_features=feature_counts.get(concept['ID']))
        for concept in csv_concepts}


def latex_unescape(s):
    return bibtex.unescape(str(s)) if s is not None else s


def make_sources(bibtex_sources):
    sources = {}
    for record in bibtex_sources.entries.values():
        authors = record.persons.get('author')
        # author = ' and '.join(map(str, authors)) if authors else None
        author = ' and '.join(map(latex_unescape, authors)) if authors else None
        editors = record.persons.get('editor')
        # editor = ' and '.join(map(str, editors)) if editors else None
        editor = ' and '.join(map(latex_unescape, editors)) if editors else None

        # I don't like mutating the function parameters
        fields = {
            k.lower(): latex_unescape(v)
            for k, v in record.fields.items()}

        id_ = record.key
        bibtex_type = bibtex.EntryType.from_string(record.type)
        year = fields.pop('year', None)
        title = fields.pop('title', None)
        type_ = fields.pop('type', None)
        booktitle = fields.pop('booktitle', None)
        pages = fields.pop('pages', None)
        edition = fields.pop('edition', None)
        journal = fields.pop('journal', None)
        school = fields.pop('school', None)
        address = fields.pop('address', None)
        url = fields.pop('url', None)
        note = fields.pop('note', None)
        number = fields.pop('number', None)
        series = fields.pop('series', None)
        volume = fields.pop('volume', None)
        publisher = fields.pop('publisher', None)
        organisation = fields.pop('organization', None)
        chapter = fields.pop('chapter', None)
        howpublished = fields.pop('howpublished', None)

        # dump the leftovers into jsondata
        jsondata = fields

        if (persons := authors or editors):
            if len(persons) == 1:
                authoryear = '{} {}'.format(
                    ' '.join(persons[0].last_names),
                    year)
            elif len(persons) == 2:
                authoryear = '{} and {} {}'.format(
                    ' '.join(persons[0].last_names),
                    ' '.join(persons[1].last_names),
                    year)
            elif len(persons) > 2:
                authoryear = '{} et al. {}'.format(
                    ' '.join(persons[0].last_names),
                    year)
            else:
                raise AssertionError('Assuming all citations have authors')
        else:
            authoryear = year
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
            description=title or None,
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


def make_features(csv_features, collections):
    return {
        feature['ID']: models.Feature(
            id=slug(feature['ID']),
            name=feature.get('Name') or feature['ID'],
            description=feature.get('Description'),
            contribution_pk=collections[feature['Collection_ID']].pk,
            url=feature.get('Feature_URL'),
            id_in_collection=feature.get('ID_in_Collection'),
            number_of_languages=int(feature['Language_Count']) if 'Language_Count' in feature else None,
            comment=feature.get('Comment'))
        for feature in csv_features}


def iter_concept_features(csv_concept_features, concepts, features):
    return (
        models.ConceptFeature(
            concept_pk=concepts[assoc['Concept_ID']].pk,
            feature_pk=features[assoc['Feature_ID']].pk)
        for assoc in csv_concept_features)


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

    csv_collections = [
        {k: v for k, v in row.items() if v}
            for row in dsv.reader(csvw_folder / 'collections.csv', dicts=True)]
    csv_features = [
        {k: v for k, v in row.items() if v}
        for row in dsv.reader(csvw_folder / 'features.csv', dicts=True)]
    csv_concepts = [
        {k: v for k, v in row.items() if v}
        for row in dsv.reader(csvw_folder / 'concepts.csv', dicts=True)]
    csv_concept_features = [
        {k: v for k, v in row.items() if v}
        for row in dsv.reader(csvw_folder / 'concepts-features.csv', dicts=True)]
    csv_concept_hierarchy = list(drop_column_header(
        dsv.reader(csvw_folder / 'concept-hierarchy.csv'),
        ['Child_ID', 'Parent_ID']))
    bibtex_sources = parse_file(str(csvw_folder / 'sources.bib'))

    # fill data base

    dataset = models.GrammaticonDataset(
        id=grammaticon.__name__,
        name="Grammaticon",
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='https://grammaticon.clld.org',
        contact='martin_haspelmath@eva.mpg.de',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'},
        version="v1.0",
        doi='10.5281/zenodo.19602410',
        repo='https://github.com/clld/grammaticon-data',
        zenodo_concept_doi='10.5281/zenodo.19602409')
    DBSession.add(dataset)

    contributors = make_contributors(csv_collections)
    DBSession.add_all(contributors.values())

    collections = make_collections(csv_collections, csv_features)
    DBSession.add_all(collections.values())

    concepts = make_concepts(csv_concepts, csv_concept_features)
    DBSession.add_all(concepts.values())

    sources = make_sources(bibtex_sources)
    DBSession.add_all(sources.values())

    # Flushing to make sure primary keys are assigned.
    DBSession.flush()

    features = make_features(csv_features, collections)
    DBSession.add_all(features.values())

    DBSession.add_all(
        common.Editor(
            dataset_pk=dataset.pk,
            contributor_pk=contributors[eid].pk,
            ord=number)
        for number, eid in enumerate(['haspelmathmartin', 'englischjohannes'], 1))
    DBSession.add_all(iter_contribution_contributors(
        csv_collections, collections, contributors))

    DBSession.add_all(iter_concept_relations(csv_concept_hierarchy, concepts))
    DBSession.add_all(iter_concept_references(csv_concepts, concepts, sources))

    # Flushing to make sure primary keys are assigned.
    DBSession.flush()

    DBSession.add_all(iter_concept_features(csv_concept_features, concepts, features))


def prime_cache(_args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for concept in DBSession.query(models.Concept):
        concept.in_degree = len(concept.parents)
        concept.out_degree = len(concept.children)
