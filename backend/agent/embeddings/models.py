from dataclasses import dataclass


@dataclass(slots=True)
class EmbeddingResult:
    """
    Result returned by an embedding provider.
    """

    vector: list[float]

    dimensions: int

    provider: str