from sadco.const import SADCOScope

all_scopes = [s for s in SADCOScope]


def all_scopes_excluding(scope):
    return [s for s in SADCOScope if s != scope]


def assert_forbidden(response):
    assert response.status_code == 403
    assert response.json() == {'detail': 'Forbidden'}

