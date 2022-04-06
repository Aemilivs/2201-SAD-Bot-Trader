import unittest
from schema import SchemaError

from trade_tree_validator import TradeTreeValidator

class TradeTreeValidatorTests(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.sut = TradeTreeValidator()

    def test_root_no_outcome(self):
        sut = TradeTreeValidator()
        input = {
            "title": "test_title",
            "child": {},
            "outcomes": []
        }
        
        self.assertRaises(SchemaError, sut.validate, input)

    def test_and_discriminator_without_children(self):
        sut = TradeTreeValidator()
        input = {
            "title": "test_title",
            "child": {
                "discriminator": "and",
                "children": []
            },
            "outcomes": [{"a": 1}]
        }
        
        self.assertRaises(SchemaError, sut.validate, input)
    
    def test_or_discriminator_without_children(self):
        sut = TradeTreeValidator()
        input = {
            "title": "test_title",
            "child": {
                "discriminator": "or",
                "children": []
            },
            "outcomes": [{"a": 1}]
        }
        
        self.assertRaises(SchemaError, sut.validate, input)

    def test_not_discriminator_without_children(self):
        sut = TradeTreeValidator()
        input = {
            "title": "test_title",
            "child": {
                "discriminator": "not",
                "children": []
            },
            "outcomes": [{"a": 1}]
        }
        
        self.assertRaises(SchemaError, sut.validate, input)

    def test_schema_discriminator_with_invalid_operation(self):
        sut = TradeTreeValidator()
        input = {
            "title": "test_title",
            "child": {
                "discriminator": "schema",
                "children": [],
                "operation": "foo"
            },
            "outcomes": [{"a": 1}]
        }
        self.assertRaises(SchemaError, sut.validate, input)

    def test_outcome_with_invalid_operation(self):
        sut = TradeTreeValidator()
        input = {
            "title": "test_title",
            "child": {
                "discriminator": "schema",
                "children": [],
                "operation": ""
            },
            "outcomes": [{"a": 1}]
        }
        
        self.assertRaises(SchemaError, sut.validate, input)

    def test_valid_root(self):
        sut = TradeTreeValidator()
        input = {
            "title": "Titlee",
            "is_active": True,
            "child": {
                "discriminator": "and",
                "children": [
                    {
                        "discriminator": "and",
                        "children": [
                            {
                                "discriminator": "schema",
                                "schema_path": "value",
                                "discriminant": "1",
                                "operation": "NUMERIC_EQUAL_COMPARISON"
                            },
                            {
                                "discriminator": "schema",
                                "schema_path": "foo",
                                "discriminant": "bar",
                                "operation": "STRING_EQUAL_COMPARISON"
                            }
                        ]
                    },
                    {
                        "discriminator": "schema",
                        "schema_path": "bug.value",
                        "discriminant": "1",
                        "operation": "numeric_Equal_Comparison"
                    }
                ]
            },
            "outcomes": [
                {
                    "operation": "open_Position",
                    "operand": "1",
                    "target": "BTC"
                },
                {
                    "operation": "close_position",
                    "operand": "1",
                    "target": "ETH"
                }
            ]
        }
        
        sut.validate(input)