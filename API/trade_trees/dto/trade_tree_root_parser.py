# Design notes:
# Layer purposed for definiton of a contract between the user and API.
import uuid
from flask_restful import reqparse, inputs


class TradeTreeRootParser(reqparse.RequestParser):
    def __init__(self) -> None:
        reqparse.RequestParser.__init__(self)
        self.add_argument('id', type=str, help='UUID identifying a user.')
        self.add_argument(
            'title',
            help='Title of the trade tree.',
            location='json')
        self.add_argument('is_active', type=inputs.boolean, location='json')
        self.add_argument('child', type=dict, location='json')
        self.add_argument(
            'outcomes',
            type=dict,
            action='append',
            location='json')
