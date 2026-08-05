from pydantic import BaseModel, Field, field_validator

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str = ""
    labels: list[str] = Field(min_length=2)

    @field_validator("labels")
    @classmethod
    def validate_labels(cls, values):
        cleaned = []
        for value in values:
            value = value.strip()
            if value and value not in cleaned:
                cleaned.append(value)
        if len(cleaned) < 2:
            raise ValueError("At least two unique labels are required")
        return cleaned

class ItemCreate(BaseModel):
    external_id: str = Field(min_length=1)
    text: str = Field(min_length=1)

class AnnotationCreate(BaseModel):
    label: str = Field(min_length=1)
    notes: str = ""
    annotator: str = ""
