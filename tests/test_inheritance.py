import pytest

from umongo import Document, fields, exceptions

from .common import BaseTest


class TestInheritance(BaseTest):

    def test_cls_field(self):

        @self.instance.register
        class Parent(Document):
            last_name = fields.StrField()

            class Meta:
                allow_inheritance = True

        @self.instance.register
        class Child(Parent):
            first_name = fields.StrField()

        assert 'cls' in Child.schema.fields
        cls_field = Child.schema.fields['cls']
        assert not hasattr(Parent(), 'cls')
        assert Child().cls == 'Child'

        loaded = Parent.build_from_mongo(
            {'_cls': 'Child', 'first_name': 'John', 'last_name': 'Doe'}, use_cls=True)
        assert loaded.cls == 'Child'

    def test_simple(self):

        @self.instance.register
        class Parent(Document):
            last_name = fields.StrField()

            class Meta:
                allow_inheritance = True
                collection_name = 'parent_col'

        assert Parent.opts.abstract == False
        assert Parent.opts.allow_inheritance == True

        @self.instance.register
        class Child(Parent):
            first_name = fields.StrField()

        assert Child.opts.abstract == False
        assert Child.opts.allow_inheritance == False
        assert Child.opts.collection_name == 'parent_col'
        assert Child.collection.name == 'parent_col'
        child = Child(first_name='John', last_name='Doe')

    def test_abstract(self):

        # Cannot define a collection_name for an abstract doc !
        with pytest.raises(exceptions.DocumentDefinitionError):
            @self.instance.register
            class BadAbstractDoc(Document):
                class Meta:
                    abstract = True
                    collection_name = 'my_col'

        @self.instance.register
        class AbstractDoc(Document):
            abs_field = fields.StrField(missing='from abstract')

            class Meta:
                abstract = True

        assert AbstractDoc.opts.abstract == True
        assert AbstractDoc.opts.allow_inheritance == True
        # Cannot instanciate also an abstract document
        with pytest.raises(exceptions.AbstractDocumentError):
            AbstractDoc()

        @self.instance.register
        class StillAbstractDoc(AbstractDoc):
            class Meta:
                abstract = True

        assert StillAbstractDoc.opts.abstract == True
        assert StillAbstractDoc.opts.allow_inheritance == True

        @self.instance.register
        class ConcreteDoc(AbstractDoc):
            pass

        assert ConcreteDoc.opts.abstract == False
        assert ConcreteDoc.opts.allow_inheritance == False
        assert ConcreteDoc().abs_field == 'from abstract'

    def test_non_document_inheritance(self):

        class NotDoc:
            @staticmethod
            def my_func():
                return 42

        @self.instance.register
        class Doc(Document, NotDoc):
            a = fields.StrField()

        assert issubclass(Doc, NotDoc)
        assert isinstance(Doc(), NotDoc)
        assert Doc.my_func() == 42
        assert Doc(a='test').my_func() == 42
