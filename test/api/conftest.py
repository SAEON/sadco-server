import sadco.api
from random import randint, choice
from collections import namedtuple

from odp.lib.hydra import HydraAdminAPI
from test.factories import (Watchem1Factory, Watchem2Factory, Watpol1Factory, Watpol2Factory, WatcurrentsFactory,
                            WatnutFactory, WatphyFactory, StationFactory, SurveyFactory, InventoryFactory,
                            SedphyFactory, Sedchem2Factory,
                            Sedchem1Factory, Sedpol2Factory, Sedpol1Factory, PlanamFactory, InstitutesFactory,
                            WeatherFactory, CurrentsFactory, CurrentMooringFactory, CurrentDepthFactory,
                            CurrentDataFactory)
from test.api import all_scopes_excluding

from sadco.const import SADCOScope, DataType

from starlette.testclient import TestClient
import pytest

MockToken = namedtuple('MockToken', ('active', 'client_id', 'sub'))


@pytest.fixture(params=['client_credentials', 'authorization_code'])
def api(request, monkeypatch):
    """Fixture returning an API test client constructor. Example usages::

        r = api(scopes).get('/catalog/')

        r = api(scopes, user_collections=authorized_collections).post('/record/', json=dict(
            doi=record.doi,
            metadata=record.metadata_,
            ...,
        ))

    Each parameterization of the calling test is invoked twice: first
    to simulate a machine client with a client_credentials grant; second
    to simulate a UI client with an authorization_code grant.

    :param scopes: iterable of ODPScope granted to the test client/user
    """
    def api_test_client(
            scopes: list[SADCOScope],
            *,
            client_id: str = 'sadco.test.client',
            role_id: str = 'sadco.test.role',
            user_id: str = 'sadco.test.user'
    ):
        monkeypatch.setattr(HydraAdminAPI, 'introspect_token', lambda _, access_token, required_scopes: MockToken(
            active=required_scopes[0] in scopes,
            client_id=client_id,
            sub=user_id if request.param == 'authorization_code' else client_id,
        ))

        return TestClient(
            app=sadco.api.app,
            headers={
                'Accept': 'application/json',
                'Authorization': 'Bearer t0k3n',
            }
        )

    api_test_client.grant_type = request.param
    return api_test_client


@pytest.fixture(params=[True, False])
def planam(request):
    if request.param:
        return PlanamFactory()

    return None


@pytest.fixture(params=[True, False])
def institute(request):
    if request.param:
        return InstitutesFactory()

    return None


@pytest.fixture
def inventories(planam, institute):
    return InventoryFactory.create_batch(randint(1, 5), survey=None, planam=planam, institute=institute,
                                         cur_moorings=None)


@pytest.fixture
def inventory():
    return InventoryFactory.create(survey=None, cur_moorings=None)


@pytest.fixture
def survey(inventory):
    survey = SurveyFactory.create(survey_id=inventory.survey_id, stations=None, inventory=inventory)
    set_station_batch(survey)
    return survey


@pytest.fixture
def current_mooring(inventory):
    current_mooring = CurrentMooringFactory.create(inventory=inventory)
    set_current_depth_batch(current_mooring)
    return current_mooring


def set_station_batch(survey):
    for _ in range(randint(2, 5)):
        station = StationFactory.create(watphy_list=None, survey=survey)
        set_watphy_batch(station)
        set_sedphy_batch(station)
        WeatherFactory(station=station)
        CurrentsFactory(station=station)


def set_watphy_batch(station):
    for _ in range(randint(1, 10)):
        watphy = WatphyFactory.create(watchem1=None, watchem2=None, watpol1=None, watpol2=None, watcurrents=None,
                                      watnut=None, station=station)

        Watchem1Factory(watphy=watphy) if choice([True, False]) else None
        Watchem2Factory(watphy=watphy) if choice([True, False]) else None
        Watpol1Factory(watphy=watphy) if choice([True, False]) else None
        Watpol2Factory(watphy=watphy) if choice([True, False]) else None
        WatcurrentsFactory(watphy=watphy) if choice([True, False]) else None
        WatnutFactory(watphy=watphy) if choice([True, False]) else None


def set_sedphy_batch(station):
    for _ in range(randint(1, 10)):
        sedphy = SedphyFactory.create(sedchem1=None, sedchem2=None, sedpol1=None, sedpol2=None, station=station)

        Sedpol1Factory(sedphy=sedphy) if choice([True, False]) else None
        Sedpol2Factory(sedphy=sedphy) if choice([True, False]) else None
        Sedchem1Factory(sedphy=sedphy) if choice([True, False]) else None
        Sedchem2Factory(sedphy=sedphy) if choice([True, False]) else None


def set_current_depth_batch(current_mooring):
    for _ in range(randint(1, 5)):
        current_depth = CurrentDepthFactory.create(cur_mooring=current_mooring)
        set_current_data_batch(current_depth)


def set_current_data_batch(current_depth):
    for _ in range(randint(1, 10)):
        CurrentDataFactory.create(cur_depth=current_depth)


@pytest.fixture(params=[
        DataType.WATER.value,
        DataType.WATERNUTRIENTS.value,
        DataType.WATERCHEMISTRY.value,
        DataType.WATERPOLLUTION.value,
        DataType.WATERNUTRIENTSANDCHEMISTRY.value,
        DataType.CURRENTS.value,
        DataType.WEATHER.value,
        DataType.SEDIMENT.value,
        DataType.SEDIMENTCHEMISTRY.value,
        DataType.SEDIMENTPOLLUTION.value
    ])
def hydro_data_type(request):
    return request.param


@pytest.fixture(params=['scope_match', 'scope_mismatch'])
def scopes(request):
    """Fixture for parameterizing the set of auth scopes
    to be associated with the API test client.

    The test function must be decorated to indicate the scope
    required by the API route::

        @pytest.mark.require_scope(ODPScope.CATALOG_READ)

    This has the same effect as parameterizing the test function
    as follows::

        @pytest.mark.parametrize('scopes', [
            [ODPScope.CATALOG_READ],
            all_scopes_excluding(ODPScope.CATALOG_READ),
        ])

    """
    scope = request.node.get_closest_marker('require_scope').args[0]

    if request.param == 'scope_match':
        return [scope]
    elif request.param == 'scope_mismatch':
        return all_scopes_excluding(scope)
