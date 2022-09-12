from api.utils.response import restify

UNVERIFIED_EMAIL_ERROR_CODE = 'unverified_email'
INVALID_CREDENTIALS_ERROR_CODE = 'invalid_credentials'
DUPLICATE_USER_ERROR_CODE = 'duplicate_user'
BAD_REQUEST_ERROR_CODE = 'bad_request'
INVALID_RESET_TOKEN_ERROR_CODE = 'invalid_token'
USER_DOES_NOT_EXIST_ERROR_CODE = 'user_not_exist'

UnverifiedEmailError = (restify(False, "User's email isn't verified", error_code=UNVERIFIED_EMAIL_ERROR_CODE), 403)
InvalidCredentialsError = (restify(False, "Invalid login details", error_code=INVALID_CREDENTIALS_ERROR_CODE), 401)
DuplicateUserError = (restify(False, "User already exists", error_code=DUPLICATE_USER_ERROR_CODE), 409)
InvalidResetTokenError = (restify(False, "Invalid token", error_code=INVALID_RESET_TOKEN_ERROR_CODE), 401)
UserDoesNotExistError = (restify(False, "User doesn't exist", error_code=USER_DOES_NOT_EXIST_ERROR_CODE), 404)

def SchemaValidationError(errors=None):
    return restify(False, "Invalid request", errors=errors, error_code=BAD_REQUEST_ERROR_CODE), 400
