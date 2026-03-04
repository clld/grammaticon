from itertools import count, dropwhile, product

from pyramid.view import view_config
from sqlalchemy.orm import joinedload

from clld.db.meta import DBSession

from grammaticon.models import Concept, ConceptRelation


@view_config(route_name='relations', renderer='json')
def relations(req):
    nodes_by_pk = {
        concept.pk: {
            'id': concept.id,
            'label': concept.name,
            'size': 1,
            'x': 0,
            'y': 0,
        }
        for concept in DBSession.query(Concept)}
    edges = [
        {
            'id': rel.pk,
            'label': '',
            'size': 0.5,
            'source': nodes_by_pk[rel.parent_pk]['id'],
            'target': nodes_by_pk[rel.child_pk]['id'],
        }
        for rel in DBSession.query(ConceptRelation)]

    # needs to be a list specifically to be serialisable, apparently
    nodes = list(nodes_by_pk.values())

    # layout nodes in a nice grid by default
    grid_width = next(dropwhile(
        lambda n: n * n < len(nodes),
        count(0)))
    for node, (x, y) in zip(nodes, product(range(grid_width), range(grid_width))):
        node['x'] = x
        node['y'] = y

    return {'nodes': nodes, 'edges': edges}
