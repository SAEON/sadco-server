class SADCOIdentityError(Exception):
    # code and description are sent to Hydra when rejecting a login request
    error_code = 'unknown_error'
    error_description = "An unknown error occurred."


class SADCOUserNotFound(SADCOIdentityError):
    error_code = 'user_not_found'
    error_description = "The user id or email address is not associated with any user account."


class SADCOClientNotFound(SADCOIdentityError):
    error_code = 'client_not_found'
    error_description = "Unknown client id."
