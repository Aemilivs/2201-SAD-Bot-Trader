# Design notes:
# Layer purposed for definiton of a contract between the user and api.
import uuid
from flask_restful import reqparse, inputs


class TradeTreeBranchParser(reqparse.RequestParser):
    def __init__(self) -> None:
        reqparse.RequestParser.__init__(self)
        self.add_argument(
            'discriminator',
            type=str,
            help='Title of the trade tree.',
            location='json')
        self.add_argument(
            'children',
            required=False,
            type=dict,
            location='json')
        self.add_argument(
            'schema_path',
            required=False,
            type=str,
            location='json')
        self.add_argument(
            'discriminant',
            required=False,
            type=str,
            location='json')
        self.add_argument(
            'operation',
            required=False,
            type=str,
            location='json')
