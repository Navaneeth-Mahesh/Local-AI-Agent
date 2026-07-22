from  dataclasses import dataclass
@dataclass(slots=True, frozen=True)
class PromptTemplate:
    """
    Represents a reusable prompt template
    """
    
    name: str
    content: str

