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
# {
#     template_name: "test",
#     subject: "test",
#     body: "test"
# }

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
class Template:
    id: Optional[str] = None
    template_name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    author: Optional[str] = None

    @property
    def full_name(self):
        return f"{self.template_name.strip()} {self.subject.strip()}".strip()

    @staticmethod
    def from_dict(obj: Any) -> 'Template':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], str(obj.get("_id")))
        template_name = from_union([from_str, from_none], obj.get("template_name"))
        subject = from_union([from_str, from_none], obj.get("subject"))
        body = from_union([from_str, from_none], obj.get("body"))
        author = from_union([from_str, from_none], obj.get("author"))

        return Template(id=id, template_name=template_name, subject=subject,
                    body=body, author=author)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["template_name"] = from_union(
            [from_str, from_none], self.template_name)
        result["subject"] = from_union([from_str, from_none], self.subject)
        result["body"] = from_union([from_str, from_none], self.body)
        result["author"] = from_union([from_str, from_none], self.author)
        
        return result


def template_from_dict(s: Any) -> Template:
    return Template.from_dict(s)


def template_to_dict(x: Template) -> Any:
    return to_class(Template, x)
