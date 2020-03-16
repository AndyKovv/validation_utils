
from .serializer_adapter import BaseSerializerAdapter


class BaseValidation:
    """
        Base validation object uses for validate
        income data with serializer
    """
    serializer_adapter = BaseSerializerAdapter

    def __new__(cls, *args, **kwargs):
        super().__new__(cls, *args, *kwargs)
        cls._status_code = 400
        cls._serializer_adapter = None
        cls._add_serializer_erorrs = None
        cls._raw_data = dict()
        cls._validated_data = dict()
        cls._serializer_errors = None

        return object().__new__(cls, *args, **kwargs)

    @property
    def validated_data(self):
        return getattr(self, '_validated_data', {})

    def add_serializer(self, serializer):
        """
            Method should add serializer with autodiscover
            :serializer - serializer instance
            :rtype - self
        """

        self._serializer_adapter = (
            self.serializer_adapter
            .build_(serializer)
        )
        return self

    def add_raw_data(self, data):
        """
            Method should add raw data
            :data - <dict> with raw data
            :rtype - self
        """
        self._raw_data = data
        return self

    def validate(self, many=False, raise_=False):
        """
            Method should validate income data
            :many - <bool>  value of many
        """
        self._required_attrib()

        # import pdb; pdb.set_trace()
        serializer_adapter_ = self._serializer_adapter.add_data(self._raw_data)

        if not serializer_adapter_.validate_data():
            self.add_serializer_errors(self.serializer)
            self._call_raise()

        self._validated_data = serializer_adapter_.validated_data
        return self

    def add_serializer_errors(self, serializer_errors):
        """
            Method should add serializer errors
            :serializer_errors - serializer instance with errors
            :trype - self
        """
        self._serializer_adapter_errors = serializer_errors
        return self

    def partial_validated_data(self, fields_list):
        """
            Method should get partial fields from serializer
            :fields_list - <tuple> with fields
            :rtype - <dict> with fields
        """
        return {
            key: value for key, value in self._validated_data.items()
            if key in fields_list
        }

    def raise_(self, status_code):
        """
            Method should raise error
        """
        raise NotImplementedError("Override method for raise custom error")

    def _call_raise(self):
        """
            Method should call raise from error mixin
            otherwice raise exeption from base class
        """
        # Try call raise_ from error class
        try:
            super(BaseValidation, self).raise_(self._status_code)
        except AttributeError:
            self.raise_(self._status_code)

    def _required_attrib(self):
        """
            Method should check required fields

        """
        serializer_exist = getattr(self, '_serializer_adapter')
        if not serializer_exist:
            raise AttributeError(
                'Serializer not exist'
                'call add_serializer() or set self._serializer_adapter manualy'
            )

        raw_data_exist = getattr(self, '_raw_data')
        if not raw_data_exist:
            raise (
                'Raw data not setted, please use, add_raw_data() method'
                'or set self._raw_data attrib'
            )
