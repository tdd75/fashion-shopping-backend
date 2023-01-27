from rest_framework import serializers


class ManyToManyUpdateField(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        kwargs['write_only'] = True
        super().__init__(instance, data, **kwargs)

    add = serializers.ListField(
        child=serializers.IntegerField(), required=False)
    remove = serializers.ListField(
        child=serializers.IntegerField(), required=False)


class ManyToManyUpdateFieldsMixin(object):
    def save(self, **kwargs):
        many_to_many_data = {}
        for field_type in self.get_fields().values():
            if not isinstance(field_type, ManyToManyUpdateField):
                continue
            field = field_type.source
            data = self.validated_data.pop(field, None)
            if data is not None:
                many_to_many_data[field] = data
        instance = super().save(**kwargs)
        for field, data in many_to_many_data.items():
            if not data:
                continue
            add_ids = data.get('add', [])
            add_list = getattr(
                instance, field).model.objects.filter(pk__in=add_ids)
            getattr(instance, field).add(*add_list)
            remove_ids = data.get('remove', [])
            remove_list = getattr(
                instance, field).model.objects.filter(pk__in=remove_ids)
            getattr(instance, field).remove(*remove_list)
        return instance

class OwnerFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(OwnerFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(owner_id=request.user.id)