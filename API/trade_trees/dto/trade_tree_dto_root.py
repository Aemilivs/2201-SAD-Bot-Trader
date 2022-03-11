# Design notes:
# Layer purposed for definiton of a contract between the user and API.
from datetime import datetime, timezone

class TradeTreeRootDTO:
    def __init__(self, id = 0, createdAt = datetime.utcnow(), updatedAt = datetime.utcnow()) -> None:
        self.id = id
        self.createdAt = createdAt
        self.updatedAt = updatedAt