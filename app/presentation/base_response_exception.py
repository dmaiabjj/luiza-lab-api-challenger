class BaseResponseException(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return {'error': {'message': self.message, 'fields': dict(self.payload or ())}}


class NotFoundException(BaseResponseException):
    def __init__(self, message):
        super().__init__(message=message, payload=None, status_code=404)


class BadRequestException(BaseResponseException):
    def __init__(self, message, payload=None):
        super().__init__(message=message, payload=payload, status_code=400)
