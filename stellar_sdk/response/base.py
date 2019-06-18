from schematics.models import Model


class BaseModel(Model):
    def __init__(self, raw_data=None, trusted_data=None, deserialize_mapping=None,
                 init=True, partial=True, strict=False, validate=False, app_data=None,
                 lazy=False, **kwargs):
        super().__init__(raw_data=raw_data, trusted_data=trusted_data, deserialize_mapping=deserialize_mapping,
                         init=init, partial=partial, strict=strict, validate=validate, app_data=app_data,
                         lazy=lazy, **kwargs)

        self.raw_data = raw_data

    def __str__(self):
        return str(self.raw_data)

    def __repr__(self):
        return "<Account instance: {}>".format(self.raw_data)
