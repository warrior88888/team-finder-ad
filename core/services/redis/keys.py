from enum import StrEnum
from typing import Any


class ThrottleAction(StrEnum):
    LOGIN_FAIL = "login_fail"
    AVATAR_RESET = "avatar_reset"


class RedisPrefix(StrEnum):
    ONLINE = "online"
    ANONYMOUS = "anon_visitor"
    THROTTLE = "throttle"

    def key(self, *parts: Any) -> str:
        return ":".join([self.value, *map(str, parts)])

    def pattern(self) -> str:
        return f"{self.value}:*"

    def extract_id(self, key: str) -> str:
        return key.removeprefix(f"{self.value}:")

    def extract_id_after_action(self, key: str, action: ThrottleAction) -> str:
        # Key format: "throttle:<action>:<id>" → returns "<id>"
        return key.removeprefix(f"{self.value}:{action}:")
