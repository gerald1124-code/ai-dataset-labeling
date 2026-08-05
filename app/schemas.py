from typing import Optional

from pydantic import BaseModel



class DatasetItem(BaseModel):

    text: str

    label: Optional[str] = None