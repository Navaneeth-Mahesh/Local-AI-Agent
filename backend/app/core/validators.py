from pydantic import EmailStr, Field
from typing import Annotated


Username = Annotated[
    str,
    Field(
        min_length=3,
        max_length=30,
        pattern=r"^[a-zA-Z0-9_]+$",
    ),
]

Password = Annotated[
    str,
    Field(
        min_length=8,
        max_length=128,
    ),
]

Email = EmailStr