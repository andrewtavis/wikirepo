"""
Fixtures
--------
"""

from datetime import date
import pytest

import wikirepo

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


entities_dict = wd_utils.EntitiesDict()
countries = ["Germany"]
depth = 0
timespan = (date(2009, 1, 1), date(2010, 1, 1))
interval = "yearly"

# Test of values for a given timespan
df = wikirepo.data.query(
    ents_dict=entities_dict,
    locations=countries,
    depth=depth,
    timespan=timespan,
    interval=interval,
    demographic_props=[
        "ethnic_div",
        "life_expectancy",
        "literacy",
        "out_of_school_children",
        "population",
    ],
    economic_props=[
        "gdp_ppp",
        "gini",
        "inflation_rate",
        "median_income",
        "nom_gdp_per_cap",
        "nom_gdp",
        "ppp_gdp_per_cap",
        "total_reserves",
        "unemployment",
    ],
    electoral_poll_props=False,
    electoral_result_props=False,
    geographic_props=["area", "continent", "country",],
    institutional_props=[
        "bti_gov_idx",
        "bti_status_idx",
        "capital",
        "fh_category",
        "human_dev_idx",
        "org_membership",
    ],
    political_props="executive",
    misc_props="country_abbr",
    verbose=True,
)

# Test of most recent values
df = wikirepo.data.query(
    ents_dict=entities_dict,
    locations=countries,
    depth=depth,
    timespan=None,
    interval=None,
    demographic_props=[
        "ethnic_div",
        "life_expectancy",
        "literacy",
        "out_of_school_children",
        "population",
    ],
    economic_props=[
        "gdp_ppp",
        "gini",
        "inflation_rate",
        "median_income",
        "nom_gdp_per_cap",
        "nom_gdp",
        "ppp_gdp_per_cap",
        "total_reserves",
        "unemployment",
    ],
    electoral_poll_props=False,
    electoral_result_props=False,
    geographic_props=["area", "continent", "country",],
    institutional_props=[
        "bti_gov_idx",
        "bti_status_idx",
        "capital",
        "fh_category",
        "human_dev_idx",
        "org_membership",
    ],
    political_props="executive",
    misc_props="country_abbr",
    verbose=True,
)
df = data_utils.split_col_val_dates(df, col="population")

entities_dict_bundeslands = wd_utils.EntitiesDict()
depth = 1
sub_lctns = True
bundeslands_dict = lctn_utils.gen_lctns_dict(
    ents_dict=entities_dict_bundeslands,
    depth=depth,
    locations=countries,
    sub_lctns=sub_lctns,
    timespan=timespan,
    interval=interval,
    verbose=True,
)
df_bundeslands = wikirepo.data.query(
    ents_dict=entities_dict_bundeslands,
    locations=bundeslands_dict,
    depth=depth,
    timespan=timespan,
    interval=interval,
    demographic_props="population",
    economic_props=False,
    electoral_poll_props=False,
    electoral_result_props=False,
    geographic_props=False,
    institutional_props="capital",
    political_props=False,
    misc_props="sub_country_abbr",
    verbose=True,
)


@pytest.fixture(params=[entities_dict])
def ents_dict(request):
    return request.param


@pytest.fixture(params=[bundeslands_dict])
def lctns_dict(request):
    return request.param


@pytest.fixture(params=[df_bundeslands])
def df(request):
    return request.param


@pytest.fixture(params=["Q183"])
def qid(request):
    return request.param


@pytest.fixture(params=["P1082"])
def pop_pid(request):
    return request.param


@pytest.fixture(params=["P6"])
def exec_pid(request):
    return request.param
