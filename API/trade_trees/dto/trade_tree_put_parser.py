# Design notes:
# Layer purposed for definiton of a contract between the user and API.
import uuid
from flask_restful import reqparse, inputs

class TradeTreePutParser(reqparse.RequestParser):
    def __init__(self) -> None:
        reqparse.RequestParser.__init__(self)
        # TODO Validation of id field for being a valid UUID. (After trade root is utilizing UUID)
        self.add_argument('id', type=int, help='Identification digits of a given trade tree.', location='json')
        self.add_argument('title', help='Title of the trade tree.', location='json')
        self.add_argument('is_active', type=inputs.boolean, location='json')