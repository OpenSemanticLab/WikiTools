# generated by datamodel-codegen:
#   filename:  Entity.json
#   timestamp: 2023-07-03T16:55:11+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class LangCode(Enum):
    en = "en"
    de = "de"


from typing import Type, TypeVar
from uuid import uuid4

from osw.model.static import Ontology, OswBaseModel, _basemodel_decorator


class Label(OswBaseModel):
    text: str = Field(..., title="Text")
    lang: Optional[LangCode] = Field("en", title="Lang code")


class LangCode1(Enum):
    en = "en"
    de = "de"


class Description(OswBaseModel):
    text: str = Field(..., title="Text")
    lang: Optional[LangCode1] = Field("en", title="Lang code")


class CommonDefinitions(OswBaseModel):
    __root__: Any


class Entity(OswBaseModel):
    uuid: UUID = Field(default_factory=uuid4, title="UUID")
    name: Optional[str] = Field(None, title="Name")
    """
    Technical / Machine compatible name
    """
    label: List[Label] = Field(..., min_items=1, title="Labels")
    """
    Human readable names. You have to assign at least one.
    """
    short_name: Optional[List[Label]] = Field(None, title="Short name")
    """
    Abbreviation, Acronym, etc.
    """
    query_label: Optional[str] = Field(None, title="Label")
    description: Optional[List[Description]] = Field(None, title="Description")
    image: Optional[str] = Field(None, title="Image")
    based_on: Optional[List[str]] = Field(None, title="Based on")
    """
    Other entities on which this one is based, e.g. when it is created by copying
    """
    statements: Optional[List[Statement]] = Field(None, title="Statements")
    attachments: Optional[List[str]] = Field(None, title="File attachments")


class Statement1(OswBaseModel):
    uuid: UUID = Field(default_factory=uuid4, title="UUID")
    label: Optional[List[Label]] = Field(None, title="Label")
    """
    Human readable name
    """
    subject: Optional[str] = Field(None, title="Subject")
    substatements: Optional[List[Statement]] = Field(None, title="Substatements")


class Statement(OswBaseModel):
    __root__: Union[Statement1, CommonDefinitions, CommonDefinitions, CommonDefinitions]


Entity.update_forward_refs()
Statement1.update_forward_refs()
# generated by datamodel-codegen:
#   filename:  Item.json
#   timestamp: 2023-07-03T16:55:13+00:00


from enum import Enum
from typing import Any, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class Level(Enum):
    public = "public"
    internal = "internal"
    restricted = "restricted"


class ReadAccess(OswBaseModel):
    level: Optional[Level] = Field(None, title="Level")


class AccessRestrictions(OswBaseModel):
    read: Optional[ReadAccess] = Field(None, title="Read access")


class Item(Entity):
    type: Optional[List[str]] = Field(
        ["Category:Item"], min_items=1, title="Types/Categories"
    )
    entry_access: Optional[AccessRestrictions] = Field(
        None, title="Access restrictions"
    )


Entity.update_forward_refs()
Statement1.update_forward_refs()
Item.update_forward_refs()
