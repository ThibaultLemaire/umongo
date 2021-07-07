from .embedded_document import EmbeddedDocumentImplementation
from .template import MetaImplementation, Template
from typing import Any, Optional

class DocumentTemplate(Template): ...

Document = DocumentTemplate

class DocumentOpts:
    instance: Any
    template: Any
    collection_name: Any
    abstract: Any
    indexes: Any
    is_child: Any
    strict: Any
    offspring: Any
    def __init__(
        self,
        instance,
        template,
        collection_name: Optional[Any] = ...,
        abstract: bool = ...,
        indexes: Optional[Any] = ...,
        is_child: bool = ...,
        strict: bool = ...,
        offspring: Optional[Any] = ...,
    ) -> None: ...

class MetaDocumentImplementation(MetaImplementation):
    def __init__(cls, *args, **kwargs) -> None: ...
    @property
    def collection(cls): ...
    @property
    def indexes(cls): ...

class DocumentImplementation(
    EmbeddedDocumentImplementation, metaclass=MetaDocumentImplementation
):
    opts: Any
    is_created: bool
    def __init__(self, **kwargs) -> None: ...
    def __eq__(self, other): ...
    def clone(self): ...
    @property
    def collection(self): ...
    @property
    def pk(self): ...
    @property
    def dbref(self): ...
    @classmethod
    def build_from_mongo(cls, data, use_cls: bool = ...): ...
    def from_mongo(self, data) -> None: ...
    def to_mongo(self, update: bool = ...): ...
    def update(self, data) -> None: ...
    def dump(self): ...
    def is_modified(self): ...
    def __setitem__(self, name, value) -> None: ...
    def __delitem__(self, name) -> None: ...
    def __setattr__(self, name, value) -> None: ...
    def __delattr__(self, name) -> None: ...
    def pre_insert(self) -> None: ...
    def pre_update(self) -> None: ...
    def pre_delete(self) -> None: ...
    def post_insert(self, ret) -> None: ...
    def post_update(self, ret) -> None: ...
    def post_delete(self, ret) -> None: ...