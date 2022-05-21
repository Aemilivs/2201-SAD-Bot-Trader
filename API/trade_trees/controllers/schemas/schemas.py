from turtle import title
from apiflask import Schema
from apiflask.fields import String, Date, Boolean, UUID, List, Nested
from apiflask.validators import Length, OneOf

from API.trade_trees.dbo.trade_tree_discriminator import TradeTreeDiscriminator
from API.trade_trees.dbo.trade_tree_outcome_operation import TradeTreeOutcomeOperation
from API.trade_trees.dbo.trade_tree_schema_operation import TradeTreeSchemaOperation
from API.trade_trees.dbo.trade_tree_time_series_operation import TradeTreeTimeSeriesOperation

class InitializeTradeTreeTableAPISchema(Schema):
    name = String(metadata={"examples": "Flash"})

class TradeTreeBranchAPISchema(Schema):
    discriminator = String(required=False, validate=OneOf(list(TradeTreeDiscriminator.__members__.keys())))
    discriminant = String()
    children = List(Nested(lambda: TradeTreeBranchAPISchema()))
    schema_path = String()
    operation = String(validate=OneOf(choices=[*list(TradeTreeSchemaOperation.__members__.keys()),*list(TradeTreeTimeSeriesOperation.__members__.keys())]))

class TradeTreeBranchOutcome(Schema):
    operation = String(required=True, validate=OneOf(choices=list(TradeTreeOutcomeOperation.__members__.keys())))
    operand = String(required=True)
    target = String(required=True)

class PostTradeTreeAPIInSchemaSuccess(Schema):
    title = String(required=True, validate=Length(4,50), metatdata={'description': 'The name of a trade tree.', 'example': 'Flash'})
    is_active = Boolean(required=False)
    child = Nested(nested=TradeTreeBranchAPISchema)
    outcomes = List(cls_or_instance=Nested(TradeTreeBranchOutcome))

class PostTradeTreeAPIOutSchemaSuccess(Schema):
    id = UUID(required=True)
    user_id = UUID(required=True)
    title = String(required=True, validate=Length(4,50), metatdata={'description': 'The name of a trade tree.', 'example': 'Flash'})
    is_active = Boolean(required=False)
    child = Nested(nested=TradeTreeBranchAPISchema)
    outcomes = List(cls_or_instance=Nested(TradeTreeBranchOutcome))
    created_at = String()
    updated_at = String()

class GetTradeTreeAPIOutSchemaSuccess(Schema):
    title = String(required=True, validate=Length(4,50), metatdata={'description': 'The name of a trade tree.', 'example': 'Flash'})
    is_active = Boolean(required=False)
    child = Nested(nested=TradeTreeBranchAPISchema)
    outcomes = List(cls_or_instance=Nested(TradeTreeBranchOutcome))

class TradeTreeHeadAPISchema(Schema):
    id = UUID()
    title = String()

class GetUserTradeTreeAPIOutSchemaSuccess(Schema):
    result = List(cls_or_instance=Nested(TradeTreeHeadAPISchema))

class PutTradeTreeAPIInSchemaSuccess(Schema):
    id = UUID(required=True)
    title = String(required=True, validate=Length(4,50), metatdata={'description': 'The name of a trade tree.', 'example': 'Flash'})
    is_active = Boolean(required=False)
    child = Nested(nested=TradeTreeBranchAPISchema)
    outcomes = List(cls_or_instance=Nested(TradeTreeBranchOutcome))

class PutTradeTreeAPIOutSchemaSuccess(Schema):
    result = Boolean()

class DeleteTradeTreeAPIOutSchemaSuccess(Schema):
    result = Boolean()

class EvaluateTradeTreeAPIOutSchemaSuccess(Schema):
    result = Boolean()
