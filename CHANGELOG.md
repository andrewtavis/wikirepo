### wikirepo 0.1.1.5 (March 28, 2021)

Changes include:

- An src structure has been adopted for easier testing and to fix wheel distribution issues
- Code quality is now checked with Codacy
- Extensive code formatting to improve quality and style
- Fixes to vulnerabilities through exception use

### wikirepo 0.1.0 (Feb 23, 2021)

First stable release of wikirepo

Additions include:

- Full documentation of the package
- Virtual environment files
- Bug fixes
- Extensive testing of all modules with GH Actions and Codecov
- Code of conduct and contribution guidelines

### wikirepo 0.0.2 (Dec 8, 2020)

The minimum viable product of wikirepo:

- Users are able to query data from [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) given locations, depth, time_lvl, and timespan arguments
- String arguments are accepted for Earth, continents, countries and disputed territories
- Data for greater depths can be retrieved by creating a dictionary given initial starting locations and going to greater depths using the [contains administrative territorial entity property](https://www.wikidata.org/wiki/Property:P150)
- Data is formatted and loaded into a pandas dataframe for further manipulation
- All available social science properties on Wikidata have had modules created for them
- Estimated load times and progress are given
- The project's scope and general roadmap have been defined and detailed in the README
