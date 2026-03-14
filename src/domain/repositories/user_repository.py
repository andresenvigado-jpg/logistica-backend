from abc import ABC, abstractmethod
from src.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def find_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    def save(self, user: User) -> User: ...
