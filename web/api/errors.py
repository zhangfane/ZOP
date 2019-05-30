from marshmallow import ValidationError

from web.api.views import blueprint_api


@blueprint_api.errorhandler(ValidationError)
def validate_error(e):
    pass
