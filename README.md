<div align="center">
  <a href="https://github.com/andrewtavis/wikirepo"><img src="https://raw.githubusercontent.com/andrewtavis/wikirepo/master/resources/wikirepo_logo.png" width="568" height="342"></a>
</div>

--------------------------------------

[![PyPI Version](https://badge.fury.io/py/wikirepo.svg)](https://pypi.org/project/wikirepo/)
[![Python Version](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)](https://pypi.org/project/wikirepo/)
[![GitHub](https://img.shields.io/github/license/andrewtavis/wikirepo.svg)](https://github.com/andrewtavis/wikirepo/blob/master/LICENSE)

### Python based ETL and ELT framework for Wikidata

**Jump to:** 
[Data](#data) • [Maps](#maps) • [To-Do](#to-do)

**wikirepo** is a Python package that provides an ETL framework to easily source and leverage standardized [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) information. The current focus is to create an intuitive interface so that Wikidata can function as a common repository for public social science statistics. 

# Installation via PyPi
```bash
pip install wikirepo
```

```python
import wikirepo
```

# Data

wikirepo's data structure is built around [Wikidata.org](https://www.wikidata.org/wiki/Wikidata:Main_Page). Human-readable access to Wikidata statistics is achieved through converting requests into Wikidata's Query IDs (QIDs) and Property IDs (PIDs), with the Python package [wikidata](https://github.com/dahlia/wikidata) serving as a basis for data loading and indexing. The wikirepo community aims to work with Wikidata to derive and add needed statistics, thus playing an integral role in growing the premier free and open sourced online knowledge base.

### Query Data

wikirepo's main ETL access function, [wikirepo.data.query](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/query.py), returns a `pandas.DataFrame` of locations and property data across time. Property access is through `data.data_utils.query_repo_dir`, with desired statistics coming from [wikirepo/data](https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/data) directory modules, and results then being merged across modules and directories. 

The query structure streamlines not just data extraction, but also the process of adding access to Wikidata properties for all to use. Adding a new property is as simple as adding a module to an appropriate [wikirepo/data](https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/data) directory, with most data modules being as simple as six defined variables and a single function call. wikirepo is self indexing, so any property module added is accessible by [wikirepo.data.query](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/query.py). See [data.demographic.population](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/demographic/population.py) for the general structure of data modules, and [examples/add_property](https://github.com/andrewtavis/wikirepo/blob/main/examples/add_property.ipynb) for a quick demo on adding new properties to wikirepo.

Each query needs the following inputs:

- **locations**: the locations that data should be queried for
    - Strings are accepted for `Earth`, continents, and countries
    - The user can also pass Wikidata QIDs directly
- **depth**: the geographic level of the given locations to query
    - A depth of 0 is the locations themselves
    - Greater depths correspond to lower geographic levels (states of countries, etc.)
    - A dictionary of locations is generated for lower depths (see second example below)
- **time_lvl**: `yearly`, `monthly`, `weekly`, or `daily` as strings
    - If not provided, then the most recent data will be retrieved with annotation for when it's from
- **timespan**: start and end `datetime.date` objects to be subsetted based on `time_lvl`
- **Further arguments**: the names of modules in [wikirepo/data](https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/data) directories
    - These are passed to arguments corresponding to their directories
    - Data will be queried for these properties for the given `locations`, `depth`, `time_lvl` and `timespan`, with results being merged as dataframe columns

Queries are also able to access information in Wikidata sub-pages for locations. For example: if inflation rate is not found on the location's main page, then wikirepo checks the location's economic topic page as [inflation_rate.py](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/economic/inflation_rate.py) is found in [wikirepo/data/economic](https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/data/economic) (see [Germany](https://www.wikidata.org/wiki/Q183) and [economy of Germany](https://www.wikidata.org/wiki/Q8046)).

wikirepo further provides a unique dictionary class, `EntitiesDict`, that stores all loaded Wikidata entities during a query. This speeds up data retrieval, as entities are loaded once and then accessed in the `EntitiesDict` object for any other needed properties.

Examples of [wikirepo.data.query](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/query.py) follow:

#### Querying Information for Given Countries

```python
import wikirepo
from wikirepo.data import wd_utils
from datetime import date

ents_dict = wd_utils.EntitiesDict()
# Strings must match their Wikidata English page names
countries = ["Germany", "United States of America", "People's Republic of China"]
# countries = ["Q183", "Q30", "Q148"] # we could also pass QIDs
depth = 0
time_lvl = 'yearly'
timespan = (date(2009,1,1), date(2010,1,1))

df = wikirepo.data.query(ents_dict=ents_dict, 
                         locations=countries, depth=depth,
                         time_lvl=time_lvl, timespan=timespan,
                         demographic_props=['population', 'life_expectancy'], 
                         economic_props='median_income', 
                         electoral_poll_props=False, 
                         electoral_result_props=False,
                         geographic_props=False, 
                         institutional_props='human_dev_idx',
                         political_props='executive',
                         misc_props=False,
                         verbose=True)

col_order = ['location', 'qid', 'year', 'executive', 'population', 
             'life_exp', 'human_dev_idx', 'median_income']
df = df[col_order]

df.head(6)
```

| location                   | qid   |   year | executive      |    population |   life_exp |   human_dev_idx |   median_income |
|:---------------------------|:------|-------:|:---------------|--------------:|-----------:|----------------:|----------------:|
| Germany                    | Q183  |   2010 | Angela Merkel  |   8.1752e+07  |    79.9878 |           0.921 |           33333 |
| Germany                    | Q183  |   2009 | Angela Merkel  | nan           |    79.8366 |           0.917 |             nan |
| United States of America   | Q30   |   2010 | Barack Obama   |   3.08746e+08 |    78.5415 |           0.914 |           43585 |
| United States of America   | Q30   |   2009 | George W. Bush | nan           |    78.3902 |           0.91  |             nan |
| People's Republic of China | Q148  |   2010 | Wen Jiabao     |   1.35976e+09 |    75.236  |           0.706 |             nan |
| People's Republic of China | Q148  |   2009 | Wen Jiabao     | nan           |    75.032  |           0.694 |             nan |



#### Querying Information for all US Counties

```python
# Note: >3000 regions, expect an hour runtime
import wikirepo
from wikirepo.data import lctn_utils, wd_utils
from datetime import date

ents_dict = wd_utils.EntitiesDict()
depth = 2 # 2 for counties, 1 for states and territories
country = "United States of America"
# country = "Q30" # we could also pass its QID
sub_lctns = True # for all
time_lvl = 'yearly'
# Only valid sub-locations given the timespan will be queried
timespan = (date(2016,1,1), date(2018,1,1))

us_counties_dict = lctn_utils.gen_lctns_dict(ents_dict=ents_dict,
                                             depth=depth,
                                             locations=country, 
                                             sub_lctns=sub_lctns,
                                             time_lvl=time_lvl, 
                                             timespan=timespan,
                                             verbose=True)

df = wikirepo.data.query(ents_dict=ents_dict, 
                         locations=us_counties_dict, depth=depth,
                         time_lvl=time_lvl, timespan=timespan,
                         demographic_props='population', 
                         economic_props=False, 
                         electoral_poll_props=False, 
                         electoral_result_props=False,
                         geographic_props='area', 
                         institutional_props='capital',
                         political_props=False,
                         misc_props=False,
                         verbose=True)

df[df['population'].notnull()].head(6)
```

| location                 | sub_lctn   | sub_sub_lctn        | qid     |   year |       population |   area_km2 | capital      |
|:-------------------------|:-----------|:--------------------|:--------|-------:|-----------------:|-----------:|:-------------|
| United States of America | California | Alameda County      | Q107146 |   2018 |      1.6602e+06  |       2127 | Oakland      |
| United States of America | California | Contra Costa County | Q108058 |   2018 |      1.14936e+06 |       2078 | Martinez     |
| United States of America | California | Marin County        | Q108117 |   2018 | 263886           |       2145 | San Rafael   |
| United States of America | California | Napa County         | Q108137 |   2018 | 141294           |       2042 | Napa         |
| United States of America | California | San Mateo County    | Q108101 |   2018 | 774155           |       1919 | Redwood City |
| United States of America | California | Santa Clara County  | Q110739 |   2018 |      1.9566e+06  |       3377 | San Jose     |



### Upload Data

[wikirepo.data.upload](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/upload.py) will be the core of the eventual wikirepo ELT process. The goal is to reocrd edits that a user makes to a prveviously queried dataframe such that these changes can then be pushed back to Wikidata. This process could be as simple as making changes to a `df.copy()` of a queried dataframe, and then using [pandas](https://github.com/pandas-dev/pandas) to compare the new and original dataframes after the user has added information that they have access to. The unique information in the edited dataframe could then be loaded into Wikidata for all to use.

The same process used to query information from Wikidata could be reversed for the upload process. Dataframe columns could be linked to their corresponding Wikidata properties, whether the time qualifiers are a [points in time](https://www.wikidata.org/wiki/Property:P585) or spans using [start time](https://www.wikidata.org/wiki/Property:P580) and [end time](https://www.wikidata.org/wiki/Property:P582) could be derived through the defined variables, and other necessary qualifiers for proper data indexing could also be included. Source information could also be added in corresponding columns to the given property edits.

Put simply: a full featured [wikirepo.data.upload](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/upload.py) function would realize the potential of a single open-source repository for all public social science information.

# Maps

[wikirepo/maps](https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/maps) is a further goal of the project, as it combines wikirepo's focus on easy to access open source data and quick high level analytics.

### Query Maps

As in [wikirepo.data.query](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/query.py), passing the `depth`, `locations`, `time_lvl` and `timespan` arguments could access GeoJSON files stored on [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page), thus providing mapping files in parallel to the user's data. These files could then be leveraged using existing Python plotting libraries to provide detailed presentations of geographic analysis.

### Upload Maps

Similar to the potential of adding statistics through [wikirepo.data.upload](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/upload.py), GeoJSON map files could also be uploaded to Wikidata using appropriate arguments. The potential exists for a myriad of variable maps given `depth`, `locations`, `time_lvl` and `timespan` information that would allow all wikirepo users to get the exact mapping file that they need for their given task.

# To-Do

### Expanding Wikidata

The growth of wikirepo's database relies on that of [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page). Beyond simply adding entries to already existing properties, the following are examples of property types that could be included:

- Those for electoral [polling](https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/data/electoral_polls) and [results](https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/data/electoral_results) for locations
    - This would allow direct access to all needed election information in a single function call
    - Data could be added to Wikidata sub-pages for locations and linked to via `data.wd_utils.dir_to_topic_page`
- A property that links political parties and their regions in [data/political](https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/data/political)
    - For easy professional presentation of electoral results (ex: loading in party hex colors, abbreviations, and alignments)
- [data/demographic](https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/data/demographic) properties such as:
    - age, education, religious, and linguistic diversities across time
- [data/economic](https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/data/economic) properties such as:
    - female workforce participation, workforce industry diversity, wealth diversity, and total working age population across time
- Distinct properties for Freedom House and Press Freedom indexes, as well as other descriptive metrics
    - These could be added to [data/institutional](https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/data/institutional)

### Further Ways to Help

- Integrating current Python tools with wikirepo ETL structures for ELT uploads to Wikidata
- Adding multiprocessing support to the [wikirepo.data.query](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/query.py) process and `data.lctn_utils.gen_lctns_dict`
- Optimizing [wikirepo.data.query](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/query.py):
    - Potentially converting `EntitiesDict` and `LocationsDict` to slotted object classes for memory savings
    - Deriving and optimizing other slow parts of the query process
- Adding access to GeoJSON files for mapping via [wikirepo.maps.query](https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/maps/query.py)
- Designing and adding GeoJSON files indexed by time properties to Wikidata
- Creating and improving [examples](https://github.com/andrewtavis/wikirepo/tree/main/examples), as well as sharing them around the web
- Testing for wikirepo
- A read the docs page

# Similar Packages
<details><summary><strong>Python<strong></summary>
<p>

- https://github.com/dahlia/wikidata
- https://github.com/SuLab/WikidataIntegrator
- https://github.com/siznax/wptools

</p>
</details>

<details><summary><strong>JavaScript<strong></summary>
<p>

- https://github.com/maxlath/wikibase-cli
- https://github.com/maxlath/wikibase-edit
- https://github.com/maxlath/wikibase-dump-filter
- https://github.com/maxlath/wikibase-sdk

</p>
</details>

<details><summary><strong>Java<strong></summary>
<p>

- https://github.com/Wikidata/Wikidata-Toolkit

</p>
</details>

# Powered By

<div align="center">
  <br>
  <a href="https://wikiba.se/"><img height="150" src="https://raw.githubusercontent.com/andrewtavis/wikirepo/master/resources/gh_images/wikibase_logo.png" alt="wikibase"></a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.wikidata.org/wiki/Wikidata:Main_Page"><img height="150" src="https://raw.githubusercontent.com/andrewtavis/wikirepo/master/resources/gh_images/wikidata_logo.png" alt="wikidata"></a>
  <br>
  <br>
</div>