upload (WIP)
============

`wikirepo.data.upload <https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/upload.py>`_ will be the core of the eventual wikirepo upload feature. The goal is to record edits that a user makes to a previously queried or baseline dataframe such that these changes can then be pushed back to Wikidata. With the addition of Wikidata login credentials as a wikirepo feature (WIP), the unique information in the edited dataframe could then be uploaded to Wikidata for all to use.

The same process used to query information from Wikidata could be reversed for the upload process. Dataframe columns could be linked to their corresponding Wikidata properties, whether the time qualifiers are a `point in time <https://www.wikidata.org/wiki/Property:P585>`_ or spans using `start time <https://www.wikidata.org/wiki/Property:P580>`_ and `end time <https://www.wikidata.org/wiki/Property:P582>`_ could be derived through the defined variables in the module header, and other necessary qualifiers for proper data indexing could also be included. Source information could also be added in corresponding columns to the given property edits.

:py:mod:`Pseudocode` for how this process could function follows:

In the first example, changes are made to a `df.copy()` of a queried dataframe. `pandas <https://github.com/pandas-dev/pandas>`_ is then used to compare the new and original dataframes after the user has added information that they have access to.


.. code-block:: python

   import wikirepo
   from wikirepo.data import lctn_utils, wd_utils
   from datetime import date

   credentials = wd_utils.login()

   ents_dict = wd_utils.EntitiesDict()
   country = "Country Name"
   depth = 2
   sub_lctns = True
   timespan = (date(2000,1,1), date(2018,1,1))
   interval = 'yearly'

   lctns_dict = lctn_utils.gen_lctns_dict()

   df = wikirepo.data.query()
   df_copy = df.copy()

   # The user checks for NaNs and adds data

   df_edits = pd.concat([df, df_copy]).drop_duplicates(keep=False)

   wikirepo.data.upload(df_edits, credentials)

In the next example `data.data_utils.gen_base_df` is used to create a dataframe with dimensions that match a time series that the user has access to. The data is then added to the column that corresponds to the property to which it should be added. Source information could further be added via a structured dictionary generated for the user.

.. code-block:: python

   import wikirepo
   from wikirepo.data import data_utils, wd_utils
   from datetime import date

   credentials = wd_utils.login()

   locations = "Country Name"
   depth = 0
   # The user defines the time parameters based on their data
   timespan = (date(1995,1,2), date(2010,1,2)) # (first Monday, last Sunday)
   interval = 'weekly'

   base_df = data_utils.gen_base_df()
   base_df['data'] = data_for_matching_time_series

   source_data = wd_utils.gen_source_dict('Source Information')
   base_df['data_source'] = [source_data] * len(base_df)

   wikirepo.data.upload(base_df, credentials)

Put simply: a full featured `wikirepo.data.upload <https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/upload.py>`_ function would realize the potential of a single read-write repository for all public information.
