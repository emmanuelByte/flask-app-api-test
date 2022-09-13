from flask.globals import current_app
from werkzeug.local import LocalProxy


max_per_page = LocalProxy(lambda: current_app.config.get('MAX_ITEMS_PER_PAGE') or 20) 

# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = pagination_meta_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast


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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class PaginationMeta:
    current_page: Optional[int] = None
    first_page: Optional[int] = None
    last_page: Optional[int] = None
    amount_per_page: Optional[int] = None
    total_amount: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PaginationMeta':
        assert isinstance(obj, dict)
        current_page = from_union([from_int, from_none], obj.get("current_page"))
        first_page = from_union([from_int, from_none], obj.get("first_page"))
        last_page = from_union([from_int, from_none], obj.get("last_page"))
        amount_per_page = from_union([from_int, from_none], obj.get("amount_per_page"))
        total_amount = from_union([from_int, from_none], obj.get("total_amount"))
        return PaginationMeta(current_page, first_page, last_page, amount_per_page, total_amount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["current_page"] = from_union([from_int, from_none], self.current_page)
        result["first_page"] = from_union([from_int, from_none], self.first_page)
        result["last_page"] = from_union([from_int, from_none], self.last_page)
        result["amount_per_page"] = from_union([from_int, from_none], self.amount_per_page)
        result["total_amount"] = from_union([from_int, from_none], self.total_amount)
        return result


def pagination_meta_from_dict(s: Any) -> PaginationMeta:
    return PaginationMeta.from_dict(s)


def pagination_meta_to_dict(x: PaginationMeta) -> Any:
    return to_class(PaginationMeta, x)
