from dataclasses import dataclass

from src.common.models import Client, Conversation


@dataclass
class CacheConversationTuple():
    conversation: Conversation | None = None
    client: Client | None = None
    last_state: str | None = None
    next_state: str | list[str] | None = None
    waithing_for: str | None = None


class ConversationCache:
    _instance = None
    _conversations_cache: dict[str, CacheConversationTuple] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    @classmethod
    def get_cache(cls):
        return cls._conversations_cache

    @classmethod
    def add_to_cache(cls, key: str, value: CacheConversationTuple):
        cls._conversations_cache[key] = value

    @classmethod
    def get_from_cache(cls, key: str):
        return cls._conversations_cache.get(key)

    @classmethod
    def remove_from_cache(cls, key: str):
        if key in cls._conversations_cache:
            del cls._conversations_cache[key]
