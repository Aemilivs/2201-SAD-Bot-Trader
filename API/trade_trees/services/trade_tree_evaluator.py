from cgitb import reset
from functools import reduce
from statistics import mean
from kink import inject

from API.trade_trees.dbo.trade_tree_discriminator import TradeTreeDiscriminator
from API.trade_trees.dbo.trade_tree_schema_operation import TradeTreeSchemaOperation
from API.trade_trees.dbo.trade_tree_time_series_operation import TradeTreeTimeSeriesOperation


@inject
class TradeTreeEvaluator():
    def __init__(self, adapter) -> None:
        self.adapter = adapter
        pass

    def evaluate_tree(self, tree):
        root_branch = tree["child"]

        result = self.evaluate_branch(root_branch)

        # TODO Introduce better error handling.
        if result is None:
            raise Exception("Invalid rule tree is attempted to be processed.")

        if result:
            # Trigger outcome
            # TODO introduce an execution of an actual outcome.
            print("Triggering an outcome")
            return True

        print("Outcomes have not been triggered.")
        return False

    def evaluate_branch(self, branch):
        discriminator = branch["discriminator"]

        if discriminator.upper() == TradeTreeDiscriminator.AND.name:
            return self.evaluate_conjuction(branch)

        if discriminator.upper() == TradeTreeDiscriminator.OR.name:
            return self.evaluate_disjunction(branch)

        if discriminator.upper() == TradeTreeDiscriminator.NOT.name:
            return self.evaluate_negation(branch)

        if discriminator.upper() == TradeTreeDiscriminator.SCHEMA.name:
            return self.evaluate_schema(branch)

        if discriminator.upper() == TradeTreeDiscriminator.TIME_SERIES.name:
            return self.evaluate_time_series(branch)

        return None

    # Logical operator AND
    def evaluate_conjuction(self, branch):

        def evaluate(left, right):
            return left and right

        children = branch["children"]

        if len(children) < 1:
            return None

        projection = map(self.evaluate_branch, children)
        results = list(projection)
        return reduce(evaluate, results)

    # Logical operator OR
    def evaluate_disjunction(self, branch):

        def evaluate(left, right):
            return left or right

        children = branch["children"]

        if len(children) < 1:
            return None

        projection = map(self.evaluate_branch, children)
        results = list(projection)
        return reduce(evaluate, results)

    # Logical operator NOT
    def evaluate_negation(self, branch):
        children = branch["children"]

        if len(children) != 1:
            return None

        child = children[0]
        result = self.evaluate_branch(child)
        return not result

    def evaluate_schema(self, branch):
        schema_path = branch["schema_path"]
        discriminant = branch["discriminant"]
        operation = branch["operation"]
        # TODO idea: parse discriminant in order to get all the arguments for
        # the api adapter

        # Placeholder for a payload returned by an adapter.
        payload = self.adapter.get_data('daily', discriminant, '1min')

        value = self.get_schema_value(payload, schema_path)

        # TODO Replace with a better validation;
        # Case when a payload does not contain the defined schema path.
        if value is None:
            return False

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_LESS_COMPARISON.name:
            return float(value) < float(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_LESS_OR_EQUAL_COMPARISON.name:
            return float(value) <= float(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_EQUAL_COMPARISON.name:
            return float(value) == float(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_MORE_COMPARISON.name:
            return float(value) > float(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_MORE_OR_EQUAL_COMPARISON.name:
            return float(value) >= float(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.STRING_EQUAL_COMPARISON.name:
            return value == discriminant

        if operation.upper() == TradeTreeSchemaOperation.STRING_STARTS_WITH_COMPARISON.name:
            return value.startswith(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.STRING_CONTAINS_COMPARISON.name:
            return discriminant in value

        if operation.upper() == TradeTreeSchemaOperation.STRING_ENDS_WITH_COMPARISON.name:
            return value.endswith(discriminant)

        return False

    def get_schema_value(self, payload, path):
        dot_index = path.find('.')

        if dot_index == -1:
            if path in payload:
                return payload[path]
            else:
                return None

        next_path = path[0:dot_index]
        rest = path[dot_index + 1:]

        return self.get_schema_value(payload[next_path], rest)

    def evaluate_time_series(self, branch):
        schema_path = branch["schema_path"]
        raw = branch["discriminant"].split(';')
        asset = raw[0]
        discriminant = float(raw[1])
        operation = branch["operation"]

        # NOTE Hardcoded API request to fetch daily metrics of 1 minute period.
        payload = self.adapter.get_data('daily', asset, '1min')

        values = self.get_time_series_values(payload, schema_path)

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MIN_LESS_COMPARISON.name:
            return min(values) < discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MIN_LESS_OR_EQUAL_COMPARISON.name:
            return min(values) <= discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MIN_EQUAL_COMPARISON.name:
            return min(values) == discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MIN_MORE_COMPARISON.name:
            return min(values) > discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MIN_MORE_OR_EQUAL_COMPARISON.name:
            return min(values) >= discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_AVERAGE_LESS_COMPARISON.name:
            return round(mean(values), 2) < discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_AVERAGE_LESS_OR_EQUAL_COMPARISON.name:
            return round(mean(values), 2) <= discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_AVERAGE_EQUAL_COMPARISON.name:
            return round(mean(values), 2) == discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_AVERAGE_MORE_COMPARISON.name:
            return round(mean(values), 2) > discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_AVERAGE_MORE_OR_EQUAL_COMPARISON.name:
            return round(mean(values), 2) >= discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MEAN_LESS_COMPARISON.name:
            return mean(values) < discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MEAN_LESS_OR_EQUAL_COMPARISON.name:
            return mean(values) <= discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MEAN_EQUAL_COMPARISON.name:
            return mean(values) == discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MEAN_MORE_COMPARISON.name:
            return mean(values) > discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MEAN_MORE_OR_EQUAL_COMPARISON.name:
            return mean(values) >= discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MAX_LESS_COMPARISON.name:
            return max(values) < discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MAX_LESS_OR_EQUAL_COMPARISON.name:
            return max(values) <= discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MAX_EQUAL_COMPARISON.name:
            return max(values) == discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MAX_MORE_COMPARISON.name:
            return max(values) > discriminant

        if operation.upper() == TradeTreeTimeSeriesOperation.TIME_SERIES_MAX_MORE_OR_EQUAL_COMPARISON.name:
            return max(values) >= discriminant

        return False

    def get_time_series_values(self, payload, schema_path):
        return list(map(lambda it: float(it[schema_path]), payload.values()))
