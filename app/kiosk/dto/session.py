from dataclasses import dataclass


@dataclass
class RequestSessionAuthenticateDTO:
    name: str
    table_id: str
    session_id: str
