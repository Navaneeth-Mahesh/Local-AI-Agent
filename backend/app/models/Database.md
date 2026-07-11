## After creating user, message & conversation .py

Our DataBase looks like this 

User
│
├── id
├── username
├── email
└── password_hash
│
└──────────────┐
               │
               ▼
Conversation
│
├── id
├── title
└── user_id
│
└──────────────┐
               │
               ▼
Message
│
├── id
├── role
├── content
└── conversation_id



# Why Use cascade="all, delete-orphan"?

Imagine:

Delete User

# Should the user's conversations remain?

No.

Likewise:

Delete Conversation

# Should its messages remain?

No.

cascade="all, delete-orphan" ensures related child records are also removed, preventing orphaned data.


## init__.py :


from .conversation import Conversation
from .message import Message
from .user import User

__all__ = [
    "User",
    "Conversation",
    "Message",
]

Importing this module later ensures SQLAlchemy knows about all of our models before creating tables or running migrations.