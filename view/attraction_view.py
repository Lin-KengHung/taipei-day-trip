from pydantic import BaseModel, Field
from typing import Optional

class Attraction(BaseModel):
	id: int 
	name: str 
	category: str
	description: str
	address: str
	transport: str
	mrt: str | None = None
	lat: float
	lng: float
	images: list[str]
class AttractionListOut(BaseModel):
     nextPage: Optional[int] = Field(None, gt=0)
     data: list[Attraction]
class AttractionSingleOut(BaseModel):
    data: Attraction
class MrtsOut(BaseModel):
    data: list