from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    """
    Input schema for CalculatorTool.
    """

    expression: str = Field(
        ...,
        min_length=1,
        description="Arithmetic expression to evaluate.",
    )