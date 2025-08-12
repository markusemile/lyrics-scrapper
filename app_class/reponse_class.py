from app_model import ResponseModel
from typing import Optional


class AppResponse:

    def __init__(self, success: bool, res: Optional[ResponseModel] = None):
        self.success = success
        self.res = res

    def to_dict(self):

        response = {"success": self.success, "status_code": self.res.status_code}

        if self.res.message:
            response["message"] = self.res.message

        if self.res.data:
            response["data"] = self.res.data

        return response

    def __repr__(self):
        res = self.to_dict()
        return f"<AppResponse {res}"
