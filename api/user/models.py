# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = user_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]



@dataclass
class User:
    id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @property
    def full_name(self):
        return f"{self.first_name.strip()} {self.last_name.strip()}".strip()

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], str(obj.get("_id")))
        first_name = from_union([from_str, from_none], obj.get("first_name"))
        last_name = from_union([from_str, from_none], obj.get("last_name"))
        email = from_union([from_str, from_none], obj.get("email"))
        password = from_union([from_str, from_none], obj.get("password"))

        return User(id=id, first_name=first_name, last_name=last_name,
                    email=email, password=password)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["first_name"] = from_union(
            [from_str, from_none], self.first_name)
        result["last_name"] = from_union([from_str, from_none], self.last_name)
        result["email"] = from_union([from_str, from_none], self.email)
        result["password"] = from_union([from_str, from_none], self.password)
        
        return result


def user_from_dict(s: Any) -> User:
    return User.from_dict(s)


def user_to_dict(x: User) -> Any:
    return to_class(User, x)
