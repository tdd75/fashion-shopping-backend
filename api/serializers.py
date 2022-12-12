class ResponseListMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        result_data = {
            "status": 0,
            "message": "Success",
            "data": {
                "updatedAt": "2020-08-31 17:49:15",
                "serverTime": "2022-03-23 15:10:11",
            },
        }
        model_name = self.queryset.model._meta.model_name
        result_data["data"][model_name] = response.data
        response.data = result_data

        return response
