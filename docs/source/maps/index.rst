maps (WIP)
==========

`wikirepo/maps <https://github.com/andrewtavis/wikirepo/tree/main/wikirepo/maps>`_ is a further goal of the project, as it combines wikirepo's focus on easy to access open source data and quick high level analytics.

**Query Maps**

As in `wikirepo.data.query <https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/query.py>`_, passing the :py:mod:`locations`, :py:mod:`depth`, :py:mod:`timespan` and :py:mod:`interval` arguments could access GeoJSON files stored on Wikidata, thus providing mapping files in parallel to the user's data. These files could then be leveraged using existing Python plotting libraries to provide detailed presentations of geographic analysis.

**Upload Maps**

Similar to the potential of adding statistics through `wikirepo.data.upload <https://github.com/andrewtavis/wikirepo/blob/main/wikirepo/data/upload.py>`_, GeoJSON map files could also be uploaded to Wikidata using appropriate arguments. The potential exists for a myriad of variable maps given :py:mod:`locations`, :py:mod:`depth`, :py:mod:`timespan` and :py:mod:`interval` information that would allow all wikirepo users to get the exact mapping file that they need for their given task.
