import json


class PinfluencerResponse:
    def __init__(self, status_code: int = 200, body=None):
        if body is None:
            body = {}

        self.status_code = status_code
        self.body = body

    def is_ok(self) -> bool:
        return 200 <= self.status_code < 300

    def as_json(self) -> dict:
        return {
            'statusCode': self.status_code,
            'body': json.dumps(self.body, default=str),
            'headers': {'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': '*',
                        'Access-Control-Allow-Methods': '*'},
        }

    @staticmethod
    def as_500_error(message="Unexpected server error. Please try later."):
        return PinfluencerResponse(500, {"message": message})

    @staticmethod
    def as_401_error(message: str = 'Not authorised'):
        return PinfluencerResponse(401, {"message": message})

    @staticmethod
    def as_404_error():
        return PinfluencerResponse(404, {"message": 'Not found'})

    @staticmethod
    def as_400_error(message: str = 'Client error, please check request.'):
        return PinfluencerResponse(400, {"message": message})