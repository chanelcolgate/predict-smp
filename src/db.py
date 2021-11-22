from typing import Dict

from src.models.user import User
from src.models.post import Post

class DummyDatabase:
	users: Dict[int, User] = {}
	posts: Dict[int, Post] = {}

db = DummyDatabase()