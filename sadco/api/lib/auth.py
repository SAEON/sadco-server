from dataclasses import dataclass
from typing import Optional

from fastapi import HTTPException
from fastapi.openapi.models import OAuth2, OAuthFlowClientCredentials, OAuthFlows
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from odp.api.models.auth import Permission
from odp.config import config
from sadco.const import SADCOScope
from sadco.lib.auth import get_client_permissions, get_user_permissions
from odp.lib.hydra import HydraAdminAPI, OAuth2TokenIntrospection

hydra_admin_api = HydraAdminAPI(config.HYDRA.ADMIN.URL)
hydra_public_url = config.HYDRA.PUBLIC.URL


@dataclass
class Authorized:
    """An Authorized object represents a statement that permission is
    granted for usage of the requested scope by the specified client
    and (if a user-initiated API call) the specified user. If such
    permission is denied, an HTTP 403 error is raised instead.

    Usage of the scope MAY be constrained to a set of grouping objects
    (providers or collections), if the scope is constrainable by such
    an object. Note that it is up to the API route handler to enforce any
    such constraint that might apply, by calling `enforce_constraint()`.
    """
    client_id: str
    user_id: Optional[str]
    scope: SADCOScope
    object_ids: Permission

    def enforce_constraint(self, object_ids: Permission) -> None:
        """For a constrainable scope, check whether access is allowed
        to the specified object ids, and raise an HTTP 403 error if not.

        The object type is given by `self.scope.constrainable_by`.

        Call `enforce_constraint('*')` if the API function requires
        the granted scope to be unconstrained.
        """
        if self.object_ids == '*':
            return

        if object_ids == '*':
            raise HTTPException(HTTP_403_FORBIDDEN)

        if not set(object_ids) <= set(self.object_ids):
            raise HTTPException(HTTP_403_FORBIDDEN)


def _authorize_request(request: Request, required_scope: SADCOScope) -> Authorized:
    auth_header = request.headers.get('Authorization')
    scheme, access_token = get_authorization_scheme_param(auth_header)
    if not auth_header or scheme.lower() != 'bearer':
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            headers={'WWW-Authenticate': 'Bearer'},
        )

    token: OAuth2TokenIntrospection = hydra_admin_api.introspect_token(
        access_token, [required_scope.value],
    )
    if not token.active:
        raise HTTPException(HTTP_403_FORBIDDEN)

    # if sub == client_id it's an API call from a client,
    # using a client credentials grant
    if token.sub == token.client_id:
        client_permissions = get_client_permissions(token.client_id)
        if required_scope not in client_permissions:
            raise HTTPException(HTTP_403_FORBIDDEN)

        return Authorized(
            client_id=token.client_id,
            user_id=None,
            scope=required_scope,
            object_ids=client_permissions[required_scope],
        )

    # user-initiated API call
    user_permissions = get_user_permissions(token.sub, token.client_id)
    if required_scope not in user_permissions:
        raise HTTPException(HTTP_403_FORBIDDEN)

    return Authorized(
        client_id=token.client_id,
        user_id=token.sub,
        scope=required_scope,
        object_ids=user_permissions[required_scope],
    )


class BaseAuthorize(SecurityBase):

    def __init__(self):
        # OpenAPI docs / Swagger auth
        self.scheme_name = 'ODP API Authorization'
        self.model = OAuth2(flows=OAuthFlows(clientCredentials=OAuthFlowClientCredentials(
            tokenUrl=f'{hydra_public_url}/oauth2/token',
            scopes={s.value: s.value for s in SADCOScope},
        )))

    def __repr__(self):
        return f'{self.__class__.__name__}()'


class Authorize(BaseAuthorize):
    def __init__(self, scope: SADCOScope):
        super().__init__()
        self.scope = scope

    def __repr__(self):
        return f'{self.__class__.__name__}(scope={self.scope.value!r})'

    async def __call__(self, request: Request) -> Authorized:
        return _authorize_request(request, self.scope)

