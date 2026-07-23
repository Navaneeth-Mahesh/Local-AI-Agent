from dataclasses import dataclass, field
@dataclass(slots=True)
class ContextItem:
    source: str
    content: str

@dataclass(slots=True)
class LLMContext:
    items: list[ContextItem] = field(default_factory=list)

    def add(
            self,
            source: str,
            content: str,
    ) -> None:
        self.items.append(
            ContextItem(
                source=source,
                content=content,
            )
        )