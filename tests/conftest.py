"""
Fixtures
--------
"""

import pytest

from wikirepo import utils
from wikirepo.data import data_utils
from wikirepo.data import lctn_utils
from wikirepo.data import query
from wikirepo.data import time_utils
from wikirepo.data import wd_utils

from wikirepo.data.demographic import ethnic_div
from wikirepo.data.demographic import life_expectancy
from wikirepo.data.demographic import literacy
from wikirepo.data.demographic import out_of_school_children
from wikirepo.data.demographic import population

from wikirepo.data.economic import gdp_ppp
from wikirepo.data.economic import gini
from wikirepo.data.economic import inflation_rate
from wikirepo.data.economic import median_income
from wikirepo.data.economic import nom_gdp_per_cap
from wikirepo.data.economic import nom_gdp
from wikirepo.data.economic import ppp_gdp_per_cap
from wikirepo.data.economic import total_reserves
from wikirepo.data.economic import unemployment

from wikirepo.data.geographic import area
from wikirepo.data.geographic import continent
from wikirepo.data.geographic import country

from wikirepo.data.institutional import bti_gov_idx
from wikirepo.data.institutional import bti_status_idx
from wikirepo.data.institutional import capital
from wikirepo.data.institutional import fh_category
from wikirepo.data.institutional import human_dev_idx
from wikirepo.data.institutional import org_membership

from wikirepo.data.misc import country_abbr
from wikirepo.data.misc import sub_country_abbr

from wikirepo.data.political import executive


@pytest.fixture(params=[[]])
def fixture_name(request):
    return request.param
