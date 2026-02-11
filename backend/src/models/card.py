from pydantic import BaseModel, Field
from typing import List, Optional

class AnkiCard(BaseModel):
    id: Optional[int] = Field(None, description="Anki Note ID")
    front: str = Field(..., description="Front content of the card (Question)")
    back: str = Field(..., description="Back content of the card (Answer)")
    tags: List[str] = Field(default_factory=list, description="List of tags")
    deck_name: str = Field(..., description="Name of the Anki deck")
    model_name: str = Field(..., description="Name of the Anki model")

    class Config:
        populate_by_name = True
