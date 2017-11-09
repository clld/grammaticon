from itertools import product

from pyramid.view import view_config
from sqlalchemy.orm import joinedload
from clld.db.meta import DBSession

from grammaticon.models import ConceptRelation


@view_config(route_name='relations', renderer='json')
def relations(req):
    res = dict(edges=[], nodes=[])
    nodes = {}
    for rel in DBSession.query(ConceptRelation) \
            .options(
                joinedload(ConceptRelation.parent), joinedload(ConceptRelation.child)):
        res['edges'].append(dict(
            id=str(rel.pk),
            label='',
            size=0.5,
            source=rel.parent.id,
            target=rel.child.id))
        for node in [rel.parent, rel.child]:
            nodes[node.id] = dict(id=node.id, label=node.name, size=1)

    for node, (x, y) in zip(nodes.values(), product(range(10), range(10))):
        node['x'], node['y'] = x, y
        res['nodes'].append(node)

    return res
