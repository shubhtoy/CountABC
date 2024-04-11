from pydantic import BaseModel, validator
from typing import Optional


class PyBase(BaseModel):
    namespace: str = "default"
    value: int = 0
    enable_reset: bool = False
    update_lowerbound: int = -1
    update_upperbound: int = 1


class RedBase(BaseModel):
    namespace: str = "default"
    value: Optional[int] = 1
    enable_reset: int = 0
    update_lowerbound: int = 0
    update_upperbound: int = 1


class ER_RedBase(BaseModel):
    namespace: bool = None
    value: bool = None
    enable_reset: bool = None
    update_lowerbound: bool = None
    update_upperbound: bool = None


class Stats(BaseModel):
    '''    "keys_created": ...,
    "keys_updated": ...,
    "requests": ...,
    "version": "..."
'''

    keys_created: int = 0
    keys_updated: int = 0
    requests: int = 0
    version: str = "0.0.1"
