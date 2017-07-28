from sqlalchemy.orm import joinedload, aliased

from clld.db.models.common import ValueSet, Value, Parameter, Contribution
from clld.web.datatables.base import DataTable, Col, LinkCol
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values


class Concepts(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'description', sTitle='definition'),
            Col(self, 'GOLD_counterpart'),
            Col(self, 'ISOCAT_counterpart'),
        ]


class Metafeatures(Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'area'),
        ]


class Features(Values):
    def base_query(self, query):
        query = query.join(Value.valueset).options(joinedload(Value.valueset))

        if self.parameter:
            return query.join(ValueSet.contribution)\
                .filter(ValueSet.parameter_pk == self.parameter.pk)\
                .options(joinedload(Value.valueset, ValueSet.contribution))

        if self.contribution:
            return query.join(ValueSet.parameter)\
                .filter(ValueSet.contribution_pk == self.contribution.pk)\
                .options(joinedload(Value.valueset, ValueSet.parameter))

        return query.join(ValueSet.parameter).join(ValueSet.contribution)\
            .options(
                joinedload(Value.valueset, ValueSet.contribution),
                joinedload(Value.valueset, ValueSet.parameter))

    def col_defs(self):
        res = [
            LinkCol(self, 'name'),
        ]
        if not self.contribution:
            res.append(LinkCol(
                self,
                'featurelist',
                model_col=Contribution.name,
                get_object=lambda o: o.valueset.contribution))
        if not self.parameter:
            res.append(LinkCol(
                self,
                'metafeature',
                model_col=Parameter.name,
                get_object=lambda o: o.valueset.parameter))
        return res


def includeme(config):
    config.register_datatable('values', Features)
    config.register_datatable('parameters', Metafeatures)
    config.register_datatable('concepts', Concepts)
