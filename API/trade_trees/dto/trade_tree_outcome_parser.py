# Design notes:
# Layer purposed for definiton of a contract between the user and API.
import uuid
from flask_restful import reqparse, inputs

class TradeTreeOutcomeParser(reqparse.RequestParser):
    def __init__(self) -> None:
        reqparse.RequestParser.__init__(self)
        # TODO Validation of id field for being a valid UUID. (After trade root is utilizing UUID)
        self.add_argument('id', type=int, help="Identification digits of a given trade tree outcome.", location='json')
        self.add_argument('operation', help="An action to perform upon positive evaluation of the trade tree.", location='json')
        self.add_argument('operand', help="The value describing scalar property of an operation.", location='json')
        self.add_argument('target', help="The target for the operation.", location='json')