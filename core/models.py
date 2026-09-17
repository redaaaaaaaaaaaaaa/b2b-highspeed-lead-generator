from pydantic import BaseModel, Field
from typing import Optional

class CompanyLead(BaseModel):
    """Schema di validazione per una scheda anagrafica aziendale."""
    name: str = Field(..., description="Ragione sociale o nome azienda")
    category: str = Field("General", description="Settore merceologico")
    website: Optional[str] = Field(None, description="URL del profilo o sito web")
    rating: Optional[str] = Field(None, description="Valutazione o punteggio reputazione")
    location: Optional[str] = Field("Non specificata", description="Sede o paese")