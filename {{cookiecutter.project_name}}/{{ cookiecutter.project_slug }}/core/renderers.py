from rest_framework.renderers import JSONRenderer as Renderer


class JSONRenderer(Renderer):
    """
    Custom JSON renderer
    """

    def render(self, data: dict, accepted_media_type=None, renderer_context=None):
        """
        Render the response data
        """
        status_code = renderer_context["response"].status_code
        data = data or {}

        response: dict = data.get("response", {})
        response_dict = {
            "message": response.get("message", ""),
            "data": response.get("data", {}),
        }

        if int(status_code) >= 400:
            response_dict["data"] = None

            try:
                response_dict["message"] = data["detail"]
            except KeyError:
                response_dict["message"] = "An error occurred"

        renderer_context["response"].data = response_dict

        return super().render(data, accepted_media_type, renderer_context)
