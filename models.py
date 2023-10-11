from pydantic import BaseModel


class RephraserStructure(BaseModel):
    text_to_rephrase: str
    number_of_variants: int = 2
    
class RephraserResponse(BaseModel):
    rephrased_variants: list[str]
    
class ContentGeneratorStructure(BaseModel):
    business_description: str
    sections: dict[str, dict[str, str]]
    
class ContentGeneratorResponse(BaseModel):
    title: str
    description: list[str]
    
class ContentGeneratorResponseStructure(BaseModel):
    response: dict[str, ContentGeneratorResponse]
    