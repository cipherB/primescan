from rest_framework import serializers


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    """
    A one-time use serializer
    Sample usage:
        serialized_data = inline_serializer(
            fields={
                "username": serializers.CharField(max_length=50),
                "password": serializers.CharField(max_length=50),
                "email": serializers.CharField(max_length=50),
            },
            data=request.data)
    """
    serializer_class = create_serializer_class(name="inline_serializer", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
