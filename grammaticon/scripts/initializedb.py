from __future__ import unicode_literals, print_function
import sys

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clldutils.dsv import reader
from clldutils.misc import slug
from nameparser import HumanName

import grammaticon
from grammaticon import models


def get_contributor(data, name):
    name = HumanName(name.strip())
    id_ = slug(name.last + name.first)
    res = data['Contributor'].get(id_)
    if not res:
        res = data.add(common.Contributor, id_, id=id_, name=name.original)
    return res


def main(args):
    data = Data()

    dataset = common.Dataset(
        id=grammaticon.__name__,
        name="Grammaticon",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://www.shh.mpg.de",
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
    for obj in reader(args.data_file('Metafeatures.csv'), dicts=True):
        data.add(
            models.Metafeature, obj['id'],
            id=slug(obj['id']), name=obj['name'], area=obj['feature_area'])

    #feature_ID,feature name,feature description,meta_feature_id,collection_id,collection URL,collection numbers
    for obj in reader(args.data_file('Features.csv'), dicts=True):
        if not obj['meta_feature_id']:
            print('skipping')
            continue
        vs = common.ValueSet(
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

    for obj in reader(args.data_file('x_Concepts_Metafeatures.csv'), dicts=True):
        if obj['concept_id'] and obj['meta_feature__id']:
            models.ConceptMetafeature(
                concept=data['Concept'][obj['concept_id']],
                metafeature=data['Metafeature'][obj['meta_feature__id']])


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
