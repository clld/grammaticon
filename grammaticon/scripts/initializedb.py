import unicodedata
from collections import Counter
from itertools import islice
from pathlib import Path

import sqlalchemy
from nameparser import HumanName

from csvw import dsv
from clld.db.meta import DBSession
from clld.db.models import common

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
            number_of_features=concept_features.get(concept['ID']))
        for concept in csv_concepts}


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
