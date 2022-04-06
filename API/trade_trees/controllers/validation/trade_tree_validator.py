from schema import Schema, And, Use, SchemaError

from API.trade_trees.dbo.trade_tree_discriminator import TradeTreeDiscriminator
from API.trade_trees.dbo.trade_tree_outcome_operation import TradeTreeOutcomeOperation
from API.trade_trees.dbo.trade_tree_schema_operation import TradeTreeSchemaOperation

class TradeTreeValidator():
    def __init__(self):
        definitions = {
            'title': And(
                str,
                And(
                    Use(
                        str,
                        error="title have to be a string."
                    ),
                    lambda it: len(it) >= 4 and len(it) <= 50,
                    error="title have to be from 4 to 50 characters long."
                )
            ),
            'child': And(
                Use(dict),
                self.validate_child
            ),
            'outcomes': And(
                Use(list),
                self.validate_outcome
            )
        }

        self.schema = Schema(definitions, ignore_extra_keys=True)

    def validate(self, tree):
        return self.schema.validate(tree)

    def validate_child(self, child):
        discriminator_is_valid = self.validate_discriminator(child)
        children_are_valid = self.validate_children(child)

        return discriminator_is_valid and children_are_valid

    def validate_children(self, branch):

        if "children" not in branch:
            children = []
        else:
            children = branch["children"]

        children_count = len(children)

        discriminator = branch["discriminator"]

        if discriminator.upper() == TradeTreeDiscriminator.AND.name:
            if(children_count > 1):
                pass
            else:
                raise SchemaError(
                    "One of branches contains `and` discriminator with not enough children.")

        if discriminator.upper() == TradeTreeDiscriminator.OR.name:
            if(children_count > 1):
                pass
            else:
                raise SchemaError(
                    "One of branches contains `or` discriminator with not enough children.")

        if discriminator.upper() == TradeTreeDiscriminator.NOT.name:
            if(children_count != 1):
                raise SchemaError(
                    "One of branches contains `not` discriminator with too many children.")

        if discriminator.upper() == TradeTreeDiscriminator.SCHEMA.name:
            if(children_count > 0):
                raise SchemaError(
                    "One of branches contains `schema` discriminator with children.")

        for child in children:
            self.validate_child(child)

        return True

    def validate_discriminator(self, branch):
        discriminator = branch["discriminator"]

        if discriminator.upper() == TradeTreeDiscriminator.AND.name:
            return True

        if discriminator.upper() == TradeTreeDiscriminator.OR.name:
            return True

        if discriminator.upper() == TradeTreeDiscriminator.NOT.name:
            return True

        if discriminator.upper() == TradeTreeDiscriminator.SCHEMA.name:
            return self.validate_operation(branch)

        raise SchemaError(
            "One of branches contains invalid discriminator `{discriminator}`.".format(
                discriminator=discriminator))

    def validate_operation(self, branch):
        operation = branch["operation"]

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_LESS_OR_EQUAL_COMPARISON.name:
            return True

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_LESS_COMPARISON.name:
            return True

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_EQUAL_COMPARISON.name:
            return True

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_MORE_COMPARISON.name:
            return True

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_MORE_OR_EQUAL_COMPARISON.name:
            return True

        if operation.upper() == TradeTreeSchemaOperation.STRING_STARTS_WITH_COMPARISON.name:
            return True

        if operation.upper() == TradeTreeSchemaOperation.STRING_EQUAL_COMPARISON.name:
            return True

        if operation.upper() == TradeTreeSchemaOperation.STRING_CONTAINS_COMPARISON.name:
            return True

        if operation.upper() == TradeTreeSchemaOperation.STRING_ENDS_WITH_COMPARISON.name:
            return True

        raise SchemaError(
            "One of schema branches contains invalid operation `{operation}`.".format(
                operation=operation))

    def validate_outcome(self, outcomes):
        if len(outcomes) < 1:
            raise SchemaError("Root does not contain any outcomes.")

        for outcome in outcomes:
            if "operation" not in outcome:
                raise SchemaError("Root contains an invalid outcome without an operation.")

            operation = outcome["operation"]

            if operation.upper() == TradeTreeOutcomeOperation.OPEN_POSITION.name:
                return True

            if operation.upper() == TradeTreeOutcomeOperation.CLOSE_POSITION.name:
                return True

            # TODO: operand validation

            # TODO: target validation

            raise SchemaError("Root contains an outcome with an invalid operation: `{operation}`.".format(operation=operation))