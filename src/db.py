from typing import Dict, List, Any

from src.models.user import User
from src.models.post import Post

class DummyDatabase:
    predictions: List[float] = list()
    scores: List[Any] = list()
    users: Dict[int, User] = {}
    posts: Dict[int, Post] = {}
    
db = DummyDatabase()