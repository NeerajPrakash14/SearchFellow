from typing import Optional, List, Dict

from pydantic import BaseModel



# define data classes for pydantic
class UpdateCount(BaseModel):
    item: str

