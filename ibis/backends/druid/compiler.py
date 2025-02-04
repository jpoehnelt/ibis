from __future__ import annotations

import contextlib

import sqlalchemy as sa

import ibis.backends.druid.datatypes as ddt
from ibis.backends.base.sql.alchemy import AlchemyCompiler, AlchemyExprTranslator
from ibis.backends.druid.registry import operation_registry


class DruidExprTranslator(AlchemyExprTranslator):
    _registry = operation_registry.copy()
    _rewrites = AlchemyExprTranslator._rewrites.copy()
    _dialect_name = "druid"

    type_mapper = ddt.DruidType

    def translate(self, op):
        result = super().translate(op)
        with contextlib.suppress(AttributeError):
            result = result.scalar_subquery()
        return sa.type_coerce(result, self.type_mapper.from_ibis(op.output_dtype))


rewrites = DruidExprTranslator.rewrites


class DruidCompiler(AlchemyCompiler):
    translator_class = DruidExprTranslator
