import sys
import itertools

from clld.cliutil import Data
from clld.db.meta import DBSession
from clld.db.models import common
from csvw.dsv import reader as basereader
from clldutils.misc import slug
from nameparser import HumanName


import grammaticon
from grammaticon import models


def reader(*args, **kw):
    kw['encoding'] = 'latin1'
    return basereader(*args, **kw)


def get_contributor(data, name):
    name = HumanName(name.strip())
    id_ = slug(name.last + name.first)
    res = data['Contributor'].get(id_)
    if not res:
        res = data.add(common.Contributor, id_, id=id_, name=name.original)
    return res


def main(args):
    data = Data()
    print(args.data_file('x'))

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
    for i, ed in enumerate(['Martin Haspelmath', 'Robert Forkel']):
        common.Editor(dataset=dataset, contributor=get_contributor(data, ed), ord=i + 1)

    eng = data.add(common.Language, 'eng', name='English')

    for obj in reader(args.data_file('Feature_lists.csv'), dicts=True):
        contrib = data.add(
            models.Featurelist, obj['id'],
            id=slug(obj['name']),
            name=obj['name'],
            year=obj['year'],
            number_of_features=int(obj['number of features']) if obj['number of features'] else None,
            url=obj['year'])
        if obj['authors']:
            for i, author in enumerate(obj['authors'].split(',')):
                common.ContributionContributor(
                    contribution=contrib,
                    contributor=get_contributor(data, author),
                    ord=i + 1)

    #id,name,feature_area
    for name, objs in itertools.groupby(
            sorted(reader(args.data_file('Metafeatures.csv'), dicts=True), key=lambda i: i['name']),
            lambda i: i['name']):
        dbobj = None
        for obj in objs:
            if not dbobj:
                dbobj = data.add(
                    models.Metafeature, obj['id'],
                    id=slug(obj['id']), name=obj['name'], area=obj['feature_area'])
            else:
                data['Metafeature'][obj['id']] = dbobj

    DBSession.flush()
    #feature_ID,feature name,feature description,meta_feature_id,collection_id,collection URL,collection numbers
    for obj in reader(args.data_file('Features.csv'), dicts=True):
        if int(obj['collection_id']) == 8:
            obj['collection_id'] = '1'
        if (not obj['meta_feature_id']):  #or obj['meta_feature_id'] in ('89'):
            print('skipping: {}'.format(obj))
            continue
        vsid = (data['Featurelist'][obj['collection_id']].pk, data['Metafeature'][obj['meta_feature_id']].pk)
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet, vsid,
                id='{0}-{1}'.format(*vsid),
                contribution=data['Featurelist'][obj['collection_id']],
                parameter=data['Metafeature'][obj['meta_feature_id']],
                language=eng)
        models.Feature(
            valueset=vs, id=slug(obj['feature_ID']), name=obj['feature name'], description=obj['feature description'])

    for obj in reader(args.data_file('Concepts.csv'), dicts=True):
        data.add(
            models.Concept, obj['id'],
            id=obj.pop('id'), name=obj.pop('label'), description=obj.pop('definition'),
            **{k.replace(' ', '_'): v for k, v in obj.items()})

    for obj in reader(args.data_file('Concepts_metafeatures.csv'), dicts=True):
        if obj['meta_feature__id'] in ('89',):
            print('skipping: {}'.format(obj))
            continue
        if obj['concept_id'] and obj['meta_feature__id']:
            models.ConceptMetafeature(
                concept=data['Concept'][obj['concept_id']],
                metafeature=data['Metafeature'][obj['meta_feature__id']])

    for obj in reader(args.data_file('Concepthierarchy.csv'), dicts=True):
        child = data['Concept'].get(obj['concept_id'])
        if child:
            parent = data['Concept'].get(obj['concept_parent_id'])
            if parent:
                DBSession.add(models.ConceptRelation(parent=parent, child=child))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for param in DBSession.query(models.Metafeature):
        param.representation = len(set(a.contribution_pk for a in param.valuesets))

    for concept in DBSession.query(models.Concept):
        concept.in_degree = len(concept.parents)
        concept.out_degree = len(concept.children)

