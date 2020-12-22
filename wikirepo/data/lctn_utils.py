"""
Utility functions for querying locations

Contents
--------
  0. No Class
      lctn_to_qid_dict
      qid_to_lctn_dict

      incl_lctn_lbls
      incl_lctn_ids
      lctn_lbl_to_qid
      qid_tp_lctn_lbl

      depth_to_col_name
      depth_to_cols
      depth_to_qid_col_name
      depth_to_qid_cols

      find_qid_get_depth
      get_qids_at_depth
      iter_set_dict
      gen_lctns_dict
          assign_first_iteration
              get_first_iter_dict
          assign_another_iteration
              get_most_frequent_dict
              get_valid_timespan_dict

      derive_depth
      merge_lctn_dicts
      find_key_items

  1. LocationsDict
      __init__
      __repr__
      __str__
      key_lbls_list
      get_depth
      iter_key_items
      iter_set
      get_qids_at_depth
      _print
"""

from pandas.core.common import flatten
from tqdm.auto import tqdm

from wikirepo import utils
from wikirepo.data import data_utils, wd_utils


def lctn_to_qid_dict():
    """
    Queries a dictionary that links a location's name to its WikiData QID
    """
    lctn_to_qid_dict = {
        "Earth": "Q2",
        "Africa": "Q15",
        "Antarctica": "Q51",
        "Asia": "Q48",
        "Europe": "Q46",
        "North America": "Q49",
        "South America": "Q18",
        "Oceania": "Q538",
        "Abkhazia": "Q23334",
        "Afghanistan": "Q889",
        "Albania": "Q222",
        "Algeria": "Q262",
        "American Samoa": "Q16641",
        "Andorra": "Q228",
        "Angola": "Q916",
        "Anguilla": "Q25228",
        "Antigua and Barbuda": "Q781",
        "Argentina": "Q414",
        "Armenia": "Q399",
        "Aruba": "Q21203",
        "Australia": "Q408",
        "Austria": "Q40",
        "Azerbaijan": "Q227",
        "Åland Islands": "Q5689",
        "Azores": "Q25263",
        "Bahrain": "Q398",
        "Bangladesh": "Q902",
        "Barbados": "Q244",
        "Belarus": "Q184",
        "Belgium": "Q31",
        "Belize": "Q242",
        "Benin": "Q962",
        "Bermuda": "Q23635",
        "Bhutan": "Q917",
        "Bolivia": "Q750",
        "Bonaire": "Q25396",
        "Bosnia and Herzegovina": "Q225",
        "Botswana": "Q963",
        "Brazil": "Q155",
        "British Virgin Islands": "Q25305",
        "Brunei": "Q921",
        "Bulgaria": "Q219",
        "Burkina Faso": "Q965",
        "Burundi": "Q967",
        "Cambodia": "Q424",
        "Cameroon": "Q1009",
        "Canada": "Q16",
        "Cape Verde": "Q1011",
        "Cayman Islands": "Q5785",
        "Central African Republic": "Q929",
        "Chad": "Q657",
        "Chile": "Q298",
        "Christmas Island": "Q31063",
        "Cocos (Keeling) Islands": "Q36004",
        "Colombia": "Q739",
        "Comoros": "Q970",
        "Cook Islands": "Q26988",
        "Costa Rica": "Q800",
        "Croatia": "Q224",
        "Cuba": "Q241",
        "Curaçao": "Q25279",
        "Cyprus": "Q229",
        "Czech Republic": "Q213",
        "Democratic Republic of the Congo": "Q974",
        "Denmark": "Q35",
        "Djibouti": "Q977",
        "Dominica": "Q784",
        "Dominican Republic": "Q786",
        "East Timor": "Q574",
        "East Turkestan": "Q840601",
        "Ecuador": "Q736",
        "Egypt": "Q79",
        "El Salvador": "Q792",
        "Equatorial Guinea": "Q983",
        "Eritrea": "Q986",
        "Estonia": "Q191",
        "Eswatini": "Q1050",
        "Ethiopia": "Q115",
        "Falkland Islands": "Q9648",
        "Faroe Islands": "Q4628",
        "Federated States of Micronesia": "Q702",
        "Fiji": "Q712",
        "Finland": "Q33",
        "France": "Q142",
        "French Polynesia": "Q30971",
        "Gabon": "Q1000",
        "Georgia": "Q230",
        "Germany": "Q183",
        "Ghana": "Q117",
        "Gibraltar": "Q1410",
        "Greece": "Q41",
        "Greenland": "Q223",
        "Grenada": "Q769",
        "Guadeloupe": "Q3118683",
        "Guam": "Q16635",
        "Guatemala": "Q774",
        "Guernsey": "Q25230",
        "Guinea": "Q1006",
        "Guinea-Bissau": "Q1007",
        "Guyana": "Q734",
        "Haiti": "Q790",
        "Honduras": "Q783",
        "Hong Kong": "Q8646",
        "Hungary": "Q28",
        "Iceland": "Q189",
        "India": "Q668",
        "Indonesia": "Q252",
        "Iran": "Q794",
        "Iraq": "Q796",
        "Ireland": "Q27",
        "Isle of Man": "Q9676",
        "Israel": "Q801",
        "Italy": "Q38",
        "Ivory Coast": "Q1008",
        "Jamaica": "Q766",
        "Japan": "Q17",
        "Jersey": "Q785",
        "Jordan": "Q810",
        "Kazakhstan": "Q232",
        "Kenya": "Q114",
        "Kiribati": "Q710",
        "Kosovo": "Q1246",
        "Kuwait": "Q817",
        "Kyrgyzstan": "Q813",
        "Laos": "Q819",
        "Latvia": "Q211",
        "Lebanon": "Q822",
        "Lesotho": "Q1013",
        "Liberia": "Q1014",
        "Libya": "Q1016",
        "Liechtenstein": "Q347",
        "Lithuania": "Q37",
        "Luxembourg": "Q32",
        "Madagascar": "Q1019",
        "Madeira": "Q26253",
        "Malawi": "Q1020",
        "Malaysia": "Q833",
        "Maldives": "Q826",
        "Mali": "Q912",
        "Malta": "Q233",
        "Marshall Islands": "Q709",
        "Martinique": "Q17054",
        "Mauritania": "Q1025",
        "Mauritius": "Q1027",
        "Mayotte": "Q17063",
        "Mexico": "Q96",
        "Moldova": "Q217",
        "Monaco": "Q235",
        "Mongolia": "Q711",
        "Montenegro": "Q236",
        "Montserrat": "Q13353",
        "Morocco": "Q1028",
        "Mozambique": "Q1029",
        "Myanmar": "Q836",
        "Namibia": "Q1030",
        "Nauru": "Q697",
        "Navassa Island": "Q25359",
        "Nepal": "Q837",
        "Netherlands": "Q55",
        "New Caledonia": "Q33788",
        "New Zealand": "Q664",
        "Nicaragua": "Q811",
        "Niger": "Q1032",
        "Nigeria": "Q1033",
        "Niue": "Q34020",
        "Norfolk Island": "Q31057",
        "North Korea": "Q423",
        "North Macedonia": "Q221",
        "Turkish Republic of Northern Cyprus": "Q23681",
        "Northern Mariana Islands": "Q16644",
        "Norway": "Q20",
        "Oman": "Q842",
        "Pakistan": "Q843",
        "Palau": "Q695",
        "State of Palestine": "Q219060",
        "Panama": "Q804",
        "Papua New Guinea": "Q691",
        "Paraguay": "Q733",
        "People's Republic of China": "Q148",
        "Peru": "Q419",
        "Philippines": "Q928",
        "Pitcairn Islands": "Q35672",
        "Poland": "Q36",
        "Portugal": "Q45",
        "Puerto Rico": "Q1183",
        "Qatar": "Q846",
        "Republic of Artsakh": "Q244165",
        "Republic of the Congo": "Q971",
        "Romania": "Q218",
        "Russia": "Q159",
        "Rwanda": "Q1037",
        "Saba": "Q25528",
        "Saint Barthélemy": "Q25362",
        "Saint Helena, Ascension and Tristan da Cunha": "Q192184",
        "Saint Kitts and Nevis": "Q763",
        "Saint Lucia": "Q760",
        "Saint Martin": "Q25596",
        "Saint Pierre and Miquelon": "Q34617",
        "Saint Vincent and the Grenadines": "Q757",
        "Samoa": "Q683",
        "San Marino": "Q238",
        "Saudi Arabia": "Q851",
        "Senegal": "Q1041",
        "Serbia": "Q403",
        "Seychelles": "Q1042",
        "Sierra Leone": "Q1044",
        "Singapore": "Q334",
        "Sint Eustatius": "Q26180",
        "Sint Maarten": "Q26273",
        "Slovakia": "Q214",
        "Slovenia": "Q215",
        "Solomon Islands": "Q685",
        "Somalia": "Q1045",
        "South Africa": "Q258",
        "South Georgia and the South Sandwich Islands": "Q35086",
        "South Korea": "Q884",
        "South Ossetia": "Q23427",
        "South Sudan": "Q958",
        "Spain": "Q29",
        "Sri Lanka": "Q854",
        "Sudan": "Q1049",
        "Suriname": "Q730",
        "Sweden": "Q34",
        "Switzerland": "Q39",
        "Syria": "Q858",
        "São Tomé and Príncipe": "Q1039",
        "Taiwan": "Q865",
        "Tajikistan": "Q863",
        "Tanzania": "Q924",
        "Thailand": "Q869",
        "The Bahamas": "Q778",
        "The Gambia": "Q1005",
        "Tibet": "Q17252",
        "Togo": "Q945",
        "Tokelau": "Q36823",
        "Tonga": "Q678",
        "Transnistria": "Q907112",
        "Trinidad and Tobago": "Q754",
        "Tunisia": "Q948",
        "Turkey": "Q43",
        "Turkmenistan": "Q874",
        "Turks and Caicos Islands": "Q18221",
        "Tuvalu": "Q672",
        "United States Virgin Islands": "Q11703",
        "Uganda": "Q1036",
        "Ukraine": "Q212",
        "United Arab Emirates": "Q878",
        "United Kingdom": "Q145",
        "United States of America": "Q30",
        "Uruguay": "Q77",
        "Uzbekistan": "Q265",
        "Vanuatu": "Q686",
        "Vatican City": "Q237",
        "Venezuela": "Q717",
        "Vietnam": "Q881",
        "Wallis and Futuna": "Q35555",
        "Western Sahara": "Q6250",
        "Yemen": "Q805",
        "Zambia": "Q953",
        "Zimbabwe": "Q954",
    }

    return lctn_to_qid_dict


def qid_to_lctn_dict():
    """
    Queries a dictionary that links a location's name to its WikiData QID

    Keys are QIDs, and values are dictionaries of QID labels and their locational level
    """
    qid_to_lctn_dict = {
        "Q2": {"lbl": "Earth", "lctn_lvl": "world"},
        "Q15": {"lbl": "Africa", "lctn_lvl": "continent"},
        "Q51": {"lbl": "Antarctica", "lctn_lvl": "continent"},
        "Q48": {"lbl": "Asia", "lctn_lvl": "continent"},
        "Q46": {"lbl": "Europe", "lctn_lvl": "continent"},
        "Q49": {"lbl": "North America", "lctn_lvl": "continent"},
        "Q18": {"lbl": "South America", "lctn_lvl": "continent"},
        "Q538": {"lbl": "Oceania", "lctn_lvl": "continent"},
        "Q23334": {"lbl": "Abkhazia", "lctn_lvl": "region"},
        "Q889": {"lbl": "Afghanistan", "lctn_lvl": "country"},
        "Q222": {"lbl": "Albania", "lctn_lvl": "country"},
        "Q262": {"lbl": "Algeria", "lctn_lvl": "country"},
        "Q16641": {"lbl": "American Samoa", "lctn_lvl": "region"},
        "Q228": {"lbl": "Andorra", "lctn_lvl": "country"},
        "Q916": {"lbl": "Angola", "lctn_lvl": "country"},
        "Q25228": {"lbl": "Anguilla", "lctn_lvl": "region"},
        "Q781": {"lbl": "Antigua and Barbuda", "lctn_lvl": "country"},
        "Q414": {"lbl": "Argentina", "lctn_lvl": "country"},
        "Q399": {"lbl": "Armenia", "lctn_lvl": "country"},
        "Q21203": {"lbl": "Aruba", "lctn_lvl": "region"},
        "Q408": {"lbl": "Australia", "lctn_lvl": "country"},
        "Q40": {"lbl": "Austria", "lctn_lvl": "country"},
        "Q227": {"lbl": "Azerbaijan", "lctn_lvl": "country"},
        "Q5689": {"lbl": "Åland Islands", "lctn_lvl": "region"},
        "Q25263": {"lbl": "Azores", "lctn_lvl": "region"},
        "Q398": {"lbl": "Bahrain", "lctn_lvl": "country"},
        "Q902": {"lbl": "Bangladesh", "lctn_lvl": "country"},
        "Q244": {"lbl": "Barbados", "lctn_lvl": "country"},
        "Q184": {"lbl": "Belarus", "lctn_lvl": "country"},
        "Q31": {"lbl": "Belgium", "lctn_lvl": "country"},
        "Q242": {"lbl": "Belize", "lctn_lvl": "country"},
        "Q962": {"lbl": "Benin", "lctn_lvl": "country"},
        "Q23635": {"lbl": "Bermuda", "lctn_lvl": "region"},
        "Q917": {"lbl": "Bhutan", "lctn_lvl": "country"},
        "Q750": {"lbl": "Bolivia", "lctn_lvl": "country"},
        "Q25396": {"lbl": "Bonaire", "lctn_lvl": "region"},
        "Q225": {"lbl": "Bosnia and Herzegovina", "lctn_lvl": "country"},
        "Q963": {"lbl": "Botswana", "lctn_lvl": "country"},
        "Q155": {"lbl": "Brazil", "lctn_lvl": "country"},
        "Q25305": {"lbl": "British Virgin Islands", "lctn_lvl": "region"},
        "Q921": {"lbl": "Brunei", "lctn_lvl": "country"},
        "Q219": {"lbl": "Bulgaria", "lctn_lvl": "country"},
        "Q965": {"lbl": "Burkina Faso", "lctn_lvl": "country"},
        "Q967": {"lbl": "Burundi", "lctn_lvl": "country"},
        "Q424": {"lbl": "Cambodia", "lctn_lvl": "country"},
        "Q1009": {"lbl": "Cameroon", "lctn_lvl": "country"},
        "Q16": {"lbl": "Canada", "lctn_lvl": "country"},
        "Q1011": {"lbl": "Cape Verde", "lctn_lvl": "country"},
        "Q5785": {"lbl": "Cayman Islands", "lctn_lvl": "region"},
        "Q929": {"lbl": "Central African Republic", "lctn_lvl": "country"},
        "Q657": {"lbl": "Chad", "lctn_lvl": "country"},
        "Q298": {"lbl": "Chile", "lctn_lvl": "country"},
        "Q148": {"lbl": "People's Republic of China", "lctn_lvl": "country"},
        "Q31063": {"lbl": "Christmas Island", "lctn_lvl": "region"},
        "Q36004": {"lbl": "Cocos (Keeling) Islands", "lctn_lvl": "region"},
        "Q739": {"lbl": "Colombia", "lctn_lvl": "country"},
        "Q970": {"lbl": "Comoros", "lctn_lvl": "country"},
        "Q26988": {"lbl": "Cook Islands", "lctn_lvl": "region"},
        "Q800": {"lbl": "Costa Rica", "lctn_lvl": "country"},
        "Q224": {"lbl": "Croatia", "lctn_lvl": "country"},
        "Q241": {"lbl": "Cuba", "lctn_lvl": "country"},
        "Q25279": {"lbl": "Curaçao", "lctn_lvl": "region"},
        "Q229": {"lbl": "Cyprus", "lctn_lvl": "country"},
        "Q213": {"lbl": "Czech Republic", "lctn_lvl": "country"},
        "Q974": {"lbl": "Democratic Republic of the Congo", "lctn_lvl": "country"},
        "Q35": {"lbl": "Denmark", "lctn_lvl": "country"},
        "Q977": {"lbl": "Djibouti", "lctn_lvl": "country"},
        "Q784": {"lbl": "Dominica", "lctn_lvl": "country"},
        "Q786": {"lbl": "Dominican Republic", "lctn_lvl": "country"},
        "Q574": {"lbl": "East Timor", "lctn_lvl": "country"},
        "Q840601": {"lbl": "East Turkestan", "lctn_lvl": "region"},
        "Q736": {"lbl": "Ecuador", "lctn_lvl": "country"},
        "Q79": {"lbl": "Egypt", "lctn_lvl": "country"},
        "Q792": {"lbl": "El Salvador", "lctn_lvl": "country"},
        "Q983": {"lbl": "Equatorial Guinea", "lctn_lvl": "country"},
        "Q986": {"lbl": "Eritrea", "lctn_lvl": "country"},
        "Q191": {"lbl": "Estonia", "lctn_lvl": "country"},
        "Q1050": {"lbl": "Eswatini", "lctn_lvl": "country"},
        "Q115": {"lbl": "Ethiopia", "lctn_lvl": "country"},
        "Q9648": {"lbl": "Falkland Islands", "lctn_lvl": "region"},
        "Q4628": {"lbl": "Faroe Islands", "lctn_lvl": "region"},
        "Q702": {"lbl": "Federated States of Micronesia", "lctn_lvl": "country"},
        "Q712": {"lbl": "Fiji", "lctn_lvl": "country"},
        "Q33": {"lbl": "Finland", "lctn_lvl": "country"},
        "Q142": {"lbl": "France", "lctn_lvl": "country"},
        "Q30971": {"lbl": "French Polynesia", "lctn_lvl": "region"},
        "Q1000": {"lbl": "Gabon", "lctn_lvl": "country"},
        "Q230": {"lbl": "Georgia", "lctn_lvl": "country"},
        "Q183": {"lbl": "Germany", "lctn_lvl": "country"},
        "Q117": {"lbl": "Ghana", "lctn_lvl": "country"},
        "Q1410": {"lbl": "Gibraltar", "lctn_lvl": "region"},
        "Q41": {"lbl": "Greece", "lctn_lvl": "country"},
        "Q223": {"lbl": "Greenland", "lctn_lvl": "region"},
        "Q769": {"lbl": "Grenada", "lctn_lvl": "country"},
        "Q3118683": {"lbl": "Guadeloupe", "lctn_lvl": "region"},
        "Q16635": {"lbl": "Guam", "lctn_lvl": "region"},
        "Q774": {"lbl": "Guatemala", "lctn_lvl": "country"},
        "Q25230": {"lbl": "Guernsey", "lctn_lvl": "region"},
        "Q1006": {"lbl": "Guinea", "lctn_lvl": "country"},
        "Q1007": {"lbl": "Guinea-Bissau", "lctn_lvl": "country"},
        "Q734": {"lbl": "Guyana", "lctn_lvl": "country"},
        "Q790": {"lbl": "Haiti", "lctn_lvl": "country"},
        "Q783": {"lbl": "Honduras", "lctn_lvl": "country"},
        "Q8646": {"lbl": "Hong Kong", "lctn_lvl": "region"},
        "Q28": {"lbl": "Hungary", "lctn_lvl": "country"},
        "Q189": {"lbl": "Iceland", "lctn_lvl": "country"},
        "Q668": {"lbl": "India", "lctn_lvl": "country"},
        "Q252": {"lbl": "Indonesia", "lctn_lvl": "country"},
        "Q794": {"lbl": "Iran", "lctn_lvl": "country"},
        "Q796": {"lbl": "Iraq", "lctn_lvl": "country"},
        "Q27": {"lbl": "Ireland", "lctn_lvl": "country"},
        "Q9676": {"lbl": "Isle of Man", "lctn_lvl": "region"},
        "Q801": {"lbl": "Israel", "lctn_lvl": "country"},
        "Q38": {"lbl": "Italy", "lctn_lvl": "country"},
        "Q1008": {"lbl": "Ivory Coast", "lctn_lvl": "country"},
        "Q766": {"lbl": "Jamaica", "lctn_lvl": "country"},
        "Q17": {"lbl": "Japan", "lctn_lvl": "country"},
        "Q785": {"lbl": "Jersey", "lctn_lvl": "region"},
        "Q810": {"lbl": "Jordan", "lctn_lvl": "country"},
        "Q232": {"lbl": "Kazakhstan", "lctn_lvl": "country"},
        "Q114": {"lbl": "Kenya", "lctn_lvl": "country"},
        "Q710": {"lbl": "Kiribati", "lctn_lvl": "country"},
        "Q1246": {"lbl": "Kosovo", "lctn_lvl": "country"},
        "Q817": {"lbl": "Kuwait", "lctn_lvl": "country"},
        "Q813": {"lbl": "Kyrgyzstan", "lctn_lvl": "country"},
        "Q819": {"lbl": "Laos", "lctn_lvl": "country"},
        "Q211": {"lbl": "Latvia", "lctn_lvl": "country"},
        "Q822": {"lbl": "Lebanon", "lctn_lvl": "country"},
        "Q1013": {"lbl": "Lesotho", "lctn_lvl": "country"},
        "Q1014": {"lbl": "Liberia", "lctn_lvl": "country"},
        "Q1016": {"lbl": "Libya", "lctn_lvl": "country"},
        "Q347": {"lbl": "Liechtenstein", "lctn_lvl": "country"},
        "Q37": {"lbl": "Lithuania", "lctn_lvl": "country"},
        "Q32": {"lbl": "Luxembourg", "lctn_lvl": "country"},
        "Q1019": {"lbl": "Madagascar", "lctn_lvl": "country"},
        "Q26253": {"lbl": "Madeira", "lctn_lvl": "region"},
        "Q1020": {"lbl": "Malawi", "lctn_lvl": "country"},
        "Q833": {"lbl": "Malaysia", "lctn_lvl": "country"},
        "Q826": {"lbl": "Maldives", "lctn_lvl": "country"},
        "Q912": {"lbl": "Mali", "lctn_lvl": "country"},
        "Q233": {"lbl": "Malta", "lctn_lvl": "country"},
        "Q709": {"lbl": "Marshall Islands", "lctn_lvl": "country"},
        "Q17054": {"lbl": "Martinique", "lctn_lvl": "region"},
        "Q1025": {"lbl": "Mauritania", "lctn_lvl": "country"},
        "Q1027": {"lbl": "Mauritius", "lctn_lvl": "country"},
        "Q17063": {"lbl": "Mayotte", "lctn_lvl": "region"},
        "Q96": {"lbl": "Mexico", "lctn_lvl": "country"},
        "Q217": {"lbl": "Moldova", "lctn_lvl": "country"},
        "Q235": {"lbl": "Monaco", "lctn_lvl": "country"},
        "Q711": {"lbl": "Mongolia", "lctn_lvl": "country"},
        "Q236": {"lbl": "Montenegro", "lctn_lvl": "country"},
        "Q13353": {"lbl": "Montserrat", "lctn_lvl": "region"},
        "Q1028": {"lbl": "Morocco", "lctn_lvl": "country"},
        "Q1029": {"lbl": "Mozambique", "lctn_lvl": "country"},
        "Q836": {"lbl": "Myanmar", "lctn_lvl": "country"},
        "Q1030": {"lbl": "Namibia", "lctn_lvl": "country"},
        "Q697": {"lbl": "Nauru", "lctn_lvl": "country"},
        "Q25359": {"lbl": "Navassa Island", "lctn_lvl": "region"},
        "Q837": {"lbl": "Nepal", "lctn_lvl": "country"},
        "Q55": {"lbl": "Netherlands", "lctn_lvl": "country"},
        "Q33788": {"lbl": "New Caledonia", "lctn_lvl": "region"},
        "Q664": {"lbl": "New Zealand", "lctn_lvl": "country"},
        "Q811": {"lbl": "Nicaragua", "lctn_lvl": "country"},
        "Q1032": {"lbl": "Niger", "lctn_lvl": "country"},
        "Q1033": {"lbl": "Nigeria", "lctn_lvl": "country"},
        "Q34020": {"lbl": "Niue", "lctn_lvl": "country"},
        "Q31057": {"lbl": "Norfolk Island", "lctn_lvl": "region"},
        "Q423": {"lbl": "North Korea", "lctn_lvl": "country"},
        "Q221": {"lbl": "North Macedonia", "lctn_lvl": "country"},
        "Q16644": {"lbl": "Northern Mariana Islands", "lctn_lvl": "region"},
        "Q20": {"lbl": "Norway", "lctn_lvl": "country"},
        "Q842": {"lbl": "Oman", "lctn_lvl": "country"},
        "Q843": {"lbl": "Pakistan", "lctn_lvl": "country"},
        "Q695": {"lbl": "Palau", "lctn_lvl": "country"},
        "Q219060": {"lbl": "State of Palestine", "lctn_lvl": "country"},
        "Q804": {"lbl": "Panama", "lctn_lvl": "country"},
        "Q691": {"lbl": "Papua New Guinea", "lctn_lvl": "country"},
        "Q733": {"lbl": "Paraguay", "lctn_lvl": "country"},
        "Q419": {"lbl": "Peru", "lctn_lvl": "country"},
        "Q928": {"lbl": "Philippines", "lctn_lvl": "country"},
        "Q35672": {"lbl": "Pitcairn Islands", "lctn_lvl": "region"},
        "Q36": {"lbl": "Poland", "lctn_lvl": "country"},
        "Q45": {"lbl": "Portugal", "lctn_lvl": "country"},
        "Q1183": {"lbl": "Puerto Rico", "lctn_lvl": "region"},
        "Q846": {"lbl": "Qatar", "lctn_lvl": "country"},
        "Q244165": {"lbl": "Republic of Artsakh", "lctn_lvl": "region"},
        "Q971": {"lbl": "Republic of the Congo", "lctn_lvl": "country"},
        "Q218": {"lbl": "Romania", "lctn_lvl": "country"},
        "Q159": {"lbl": "Russia", "lctn_lvl": "country"},
        "Q1037": {"lbl": "Rwanda", "lctn_lvl": "country"},
        "Q25528": {"lbl": "Saba", "lctn_lvl": "region"},
        "Q25362": {"lbl": "Saint Barthélemy", "lctn_lvl": "region"},
        "Q192184": {
            "lbl": "Saint Helena, Ascension and Tristan da Cunha",
            "lctn_lvl": "region",
        },
        "Q763": {"lbl": "Saint Kitts and Nevis", "lctn_lvl": "country"},
        "Q760": {"lbl": "Saint Lucia", "lctn_lvl": "country"},
        "Q25596": {"lbl": "Saint Martin", "lctn_lvl": "region"},
        "Q34617": {"lbl": "Saint Pierre and Miquelon", "lctn_lvl": "region"},
        "Q757": {"lbl": "Saint Vincent and the Grenadines", "lctn_lvl": "country"},
        "Q683": {"lbl": "Samoa", "lctn_lvl": "country"},
        "Q238": {"lbl": "San Marino", "lctn_lvl": "country"},
        "Q851": {"lbl": "Saudi Arabia", "lctn_lvl": "country"},
        "Q1041": {"lbl": "Senegal", "lctn_lvl": "country"},
        "Q403": {"lbl": "Serbia", "lctn_lvl": "country"},
        "Q1042": {"lbl": "Seychelles", "lctn_lvl": "country"},
        "Q1044": {"lbl": "Sierra Leone", "lctn_lvl": "country"},
        "Q334": {"lbl": "Singapore", "lctn_lvl": "country"},
        "Q26180": {"lbl": "Sint Eustatius", "lctn_lvl": "region"},
        "Q26273": {"lbl": "Sint Maarten", "lctn_lvl": "region"},
        "Q214": {"lbl": "Slovakia", "lctn_lvl": "country"},
        "Q215": {"lbl": "Slovenia", "lctn_lvl": "country"},
        "Q685": {"lbl": "Solomon Islands", "lctn_lvl": "country"},
        "Q1045": {"lbl": "Somalia", "lctn_lvl": "country"},
        "Q258": {"lbl": "South Africa", "lctn_lvl": "country"},
        "Q35086": {
            "lbl": "South Georgia and the South Sandwich Islands",
            "lctn_lvl": "region",
        },
        "Q884": {"lbl": "South Korea", "lctn_lvl": "country"},
        "Q23427": {"lbl": "South Ossetia", "lctn_lvl": "region"},
        "Q958": {"lbl": "South Sudan", "lctn_lvl": "country"},
        "Q29": {"lbl": "Spain", "lctn_lvl": "country"},
        "Q854": {"lbl": "Sri Lanka", "lctn_lvl": "country"},
        "Q1049": {"lbl": "Sudan", "lctn_lvl": "country"},
        "Q730": {"lbl": "Suriname", "lctn_lvl": "country"},
        "Q34": {"lbl": "Sweden", "lctn_lvl": "country"},
        "Q39": {"lbl": "Switzerland", "lctn_lvl": "country"},
        "Q858": {"lbl": "Syria", "lctn_lvl": "country"},
        "Q1039": {"lbl": "São Tomé and Príncipe", "lctn_lvl": "country"},
        "Q865": {"lbl": "Taiwan", "lctn_lvl": "country"},
        "Q863": {"lbl": "Tajikistan", "lctn_lvl": "country"},
        "Q924": {"lbl": "Tanzania", "lctn_lvl": "country"},
        "Q869": {"lbl": "Thailand", "lctn_lvl": "country"},
        "Q778": {"lbl": "The Bahamas", "lctn_lvl": "country"},
        "Q1005": {"lbl": "The Gambia", "lctn_lvl": "country"},
        "Q17252": {"lbl": "Tibet", "lctn_lvl": "region"},
        "Q945": {"lbl": "Togo", "lctn_lvl": "country"},
        "Q36823": {"lbl": "Tokelau", "lctn_lvl": "region"},
        "Q678": {"lbl": "Tonga", "lctn_lvl": "country"},
        "Q907112": {"lbl": "Transnistria", "lctn_lvl": "region"},
        "Q754": {"lbl": "Trinidad and Tobago", "lctn_lvl": "country"},
        "Q948": {"lbl": "Tunisia", "lctn_lvl": "country"},
        "Q43": {"lbl": "Turkey", "lctn_lvl": "country"},
        "Q23681": {"lbl": "Turkish Republic of Northern Cyprus", "lctn_lvl": "region"},
        "Q874": {"lbl": "Turkmenistan", "lctn_lvl": "country"},
        "Q18221": {"lbl": "Turks and Caicos Islands", "lctn_lvl": "region"},
        "Q672": {"lbl": "Tuvalu", "lctn_lvl": "country"},
        "Q1036": {"lbl": "Uganda", "lctn_lvl": "country"},
        "Q212": {"lbl": "Ukraine", "lctn_lvl": "country"},
        "Q878": {"lbl": "United Arab Emirates", "lctn_lvl": "country"},
        "Q145": {"lbl": "United Kingdom", "lctn_lvl": "country"},
        "Q30": {"lbl": "United States", "lctn_lvl": "country"},
        "Q11703": {"lbl": "United States Virgin Islands", "lctn_lvl": "region"},
        "Q77": {"lbl": "Uruguay", "lctn_lvl": "country"},
        "Q265": {"lbl": "Uzbekistan", "lctn_lvl": "country"},
        "Q686": {"lbl": "Vanuatu", "lctn_lvl": "country"},
        "Q237": {"lbl": "Vatican City", "lctn_lvl": "country"},
        "Q717": {"lbl": "Venezuela", "lctn_lvl": "country"},
        "Q881": {"lbl": "Vietnam", "lctn_lvl": "country"},
        "Q35555": {"lbl": "Wallis and Futuna", "lctn_lvl": "region"},
        "Q6250": {"lbl": "Western Sahara", "lctn_lvl": "region"},
        "Q805": {"lbl": "Yemen", "lctn_lvl": "country"},
        "Q953": {"lbl": "Zambia", "lctn_lvl": "country"},
        "Q954": {"lbl": "Zimbabwe", "lctn_lvl": "country"},
    }

    return qid_to_lctn_dict


def incl_lctn_lbls(lctn_lvls=False):
    """
    Queries the included location labels

    Parameters
    ----------
        lctn_lvls : str or list (contains strs)
            The level(s) of location to be queried

    Returns
    -------
        incl_lctns : list (contains strs)
            The Wikidata labels corresponding to the provided location level(s)
    """
    lctn_lvls = utils._make_var_list(lctn_lvls)[0]

    valid_args = ["world", "continent", "country", "region"]

    assert sorted(list(set(valid_args) | set(lctn_lvls))) == sorted(valid_args), (
        "Invalid levels were provided to the 'lctn_lvls' argument. Valid options are: "
        + ", ".join(valid_args)
        + "."
    )

    incl_lctns = []

    if "world" in lctn_lvls:
        incl_lctns.append(
            [
                lctn
                for lctn in lctn_to_qid_dict().keys()
                if qid_to_lctn_dict()[lctn_to_qid_dict()[lctn]]["lctn_lvl"] == "world"
            ]
        )

    if "continent" in lctn_lvls:
        incl_lctns.append(
            [
                lctn
                for lctn in lctn_to_qid_dict().keys()
                if qid_to_lctn_dict()[lctn_to_qid_dict()[lctn]]["lctn_lvl"]
                == "continent"
            ]
        )

    if "country" in lctn_lvls:
        incl_lctns.append(
            [
                lctn
                for lctn in lctn_to_qid_dict().keys()
                if qid_to_lctn_dict()[lctn_to_qid_dict()[lctn]]["lctn_lvl"] == "country"
            ]
        )

    if "region" in lctn_lvls:
        incl_lctns.append(
            [
                lctn
                for lctn in lctn_to_qid_dict().keys()
                if qid_to_lctn_dict()[lctn_to_qid_dict()[lctn]]["lctn_lvl"] == "region"
            ]
        )

    return list(flatten(incl_lctns))


def incl_lctn_ids():
    """
    Queries the included location ids
    """
    return list(lctn_to_qid_dict().values())


def lctn_lbl_to_qid(locations):
    """
    Returns the Wikidata QID for given location(s)

    Parameters
    ----------
        locations : str or list (contains strs)
            The label(s) of location(s) to be converted

    Returns
    -------
        wd_qids : list (contains strs)
            The Wikidata QIDs corresponding to the provided location label(s)
    """
    locations, was_str_bool = utils._make_var_list(locations)

    locations = utils.check_str_args(
        arguments=locations, valid_args=lctn_to_qid_dict().keys()
    )

    wd_qids = [lctn_to_qid_dict()[lctn] for lctn in locations]

    return utils._return_given_type(var=wd_qids, var_was_str=was_str_bool)


def qid_to_lctn_lbl(qids):
    """
    Returns the Wikidata label for given QID(s)

    Parameters
    ----------
        qids : str or list (contains strs)
            The QID(s) of location(s) to be converted

    Returns
    -------
        wd_lbls : list (contains strs)
            The Wikidata labels corresponding to the provided location qid(s)

    """
    qids, was_str_bool = utils._make_var_list(qids)

    for q in qids:
        if q not in qid_to_lctn_dict().keys():
            print(f"{q} is not a QID that a label can be direcrtly queried for.")
            print("Use wd_utils.get_lbl() to load the entity and get its label.")
            qids.pop(q)

    wd_lbls = [qid_to_lctn_dict()[q]["lbl"] for q in qids]

    return utils._return_given_type(var=wd_lbls, var_was_str=was_str_bool)


def depth_to_col_name(depth):
    """
    Derives the proper name of the column for locations given a depth
    """
    if depth == 0:
        return "location"

    else:
        return "sub_" * depth + "lctn"


def depth_to_qid_col_name(depth):
    """
    Derives the proper name of the column for qids for depth based assignment
    """
    return "sub_" * depth + "qid"


def depth_to_qid_cols(depth):
    """
    Derives the proper name of the column for qids for depth based assignment
    """
    return ["sub_" * d + "qid" for d in range(depth + 1)]


def depth_to_cols(depth):
    """
    Derives a list of locational columns for data_utils.gen_base_df given a depth
    """
    return list(
        flatten(
            ["location"] + [["sub_" * d + "lctn"] for d in range(depth + 1) if d > 0]
        )
    )


def find_qid_get_depth(lctns_dict, c=0):
    """
    Finds all QIDs and gets their depths
    """
    if isinstance(lctns_dict, dict):
        for k, v in lctns_dict.items():
            if wd_utils.is_wd_id(k):
                yield (k, int(c / 2))
            if isinstance(v, dict):
                for result in find_qid_get_depth(v, c + 1):
                    yield result


def get_qids_at_depth(lctns_dict, depth=None):
    """
    Finds all QIDs at a given depth of a LocationsDict
    """
    all_qid_depths = list(find_qid_get_depth(lctns_dict=lctns_dict, c=0))

    qids_at_depth = [q[0] for q in all_qid_depths if q[1] == depth]

    return qids_at_depth


def iter_set_dict(dictionary, key, sub_key, value):
    """
    Iterates until a key is found, and then sets the value (potentially given a sub_key)
    """
    for k, v in dictionary.items():  # pylint: disable=unused-variable
        if k == key:
            if sub_key == None:
                dictionary[k] = value

            else:
                dictionary[k][sub_key] = value

        elif type(dictionary[k]) == dict:
            iter_set_dict(dictionary[k], key, sub_key, value)

        elif type(dictionary[k]) == str:
            pass


def gen_lctns_dict(
    ents_dict=None,
    locations=None,
    depth=0,
    sub_lctns=True,
    timespan=None,
    interval=None,
    #    multicore=True,
    verbose=True,
):
    """
    Generates a dictionary of locations indexed by QIDs

    Note: 'P150' (contains administrative territorial entity) is used to subset

    Parameters
    ----------
        ents_dict : wd_utils.EntitiesDict : optional (default=None)
            A dictionary with keys being Wikidata QIDs and values being their entities

        locations : str or list (contains strs) : optional (default=None)
            The name of a location or list of location names

        depth : int (default=0, no sub_locations)
            The depth from the given lbls or qids that data should go
            Note: this uses 'P150' (contains administrative territorial entity)

        sub_lctns : str or list (contains strs) : optional (default=None)
            sub_locations to subset by or not subset by adding '~' as the first character

        timespan : two element tuple or list : contains datetime.date or tuple (default=None: (date.today(), date.today()))
            A tuple or list that defines the start and end dates to be queried
            Note 1: if True, then the full timespan from 1-1-1 to the current day will be queried
            Note 2: passing a single entry will query for that date only

        interval : str
            The time interval over which queries will be made
            Note 1: see data.time_utils for options
            Note 2: if None, then only the most recent data will be queried

        verbose : bool (default=True)
            Whether to show a tqdm progress bar for the creation of the dictionary

        Potential later arguments:
            multicore : bool or int (default=False)
                Whether to make use of multiple processes and threads, and how many to use
                Note: True uses all available

    Returns
    -------
        subs_dict : dict
            A dictionary of the given qids as keys and dictionaries of their subsidiaries by 'P150' as items
    """
    pid = "P150"
    lctns_dict = LocationsDict()
    current_depth = 0

    def assign_first_iteration(
        ents_dict=None,
        lctns_dict=None,
        qids=None,
        #    multicore=True,
        verbose=True,
    ):
        """
        Assigns the first level of a LocationsDict
        """

        def get_first_iter_dict(ents_dict, lctns_dict, qid):
            lctns_dict[qid] = {"lbl": wd_utils.get_lbl(ents_dict, qid)}

        disable = not verbose
        for q in tqdm(qids, desc="Depth 0 derived", total=len(qids), disable=disable):
            get_first_iter_dict(ents_dict, lctns_dict, q)

    def assign_another_iteration(
        ents_dict=ents_dict,
        lctns_dict=lctns_dict,
        pid=None,
        depth=depth,
        current_depth=current_depth,
        sub_lctns=sub_lctns,
        timespan=timespan,
        interval=interval,
        #  multicore=multicore,
        verbose=verbose,
    ):
        """
        Assigns more layers to a LocationsDict after the first
        """
        sub_lctns = utils._make_var_list(sub_lctns)[0]

        depth_keys = get_qids_at_depth(lctns_dict=lctns_dict, depth=current_depth)

        disable = not verbose
        if interval == None:
            # Assuming that the user wants the current sub-locations
            def get_most_frequent_dict(ents_dict, lctns_dict, qid, pid):
                """
                Returns sub-locations that don't have 'P582' (end time) or don't have qualifiers at all
                """
                if pid in wd_utils.load_ent(ents_dict, qid)["claims"].keys():
                    subs_info = {
                        sub[0]: {"lbl": sub[1]}
                        for sub in [
                            [
                                wd_utils.get_prop_id(ents_dict, qid, pid, i),
                                wd_utils.get_prop_lbl(ents_dict, qid, pid, i),
                            ]
                            for i in range(len(wd_utils.get_prop(ents_dict, qid, pid)))
                            if (
                                wd_utils.prop_has_qualifiers(ents_dict, qid, pid, i)
                                and "P582"
                                not in wd_utils.get_qualifiers(
                                    ents_dict, qid, pid, i
                                ).keys()
                            )
                            or not wd_utils.prop_has_qualifiers(ents_dict, qid, pid, i)
                        ]
                        if (
                            sub_lctns == True
                            or (sub_lctns != True and sub[1] in sub_lctns)
                            or (
                                sub_lctns != True
                                and sub[1]
                                not in [
                                    lctn[1:] for lctn in sub_lctns if lctn[0] == "~"
                                ]
                            )
                        )
                    }

                else:
                    wd_utils.print_not_available(
                        ents_dict=ents_dict,
                        qid=qid,
                        pid=pid,
                        exrta_msg=" to derive sub_lctns",
                    )
                    subs_info = {}

                iter_set_dict(
                    dictionary=lctns_dict, key=qid, sub_key="sub_lctns", value=subs_info
                )

            for q in tqdm(
                depth_keys,
                desc=f"Depth {current_depth + 1} derived",
                total=len(depth_keys),
                disable=disable,
            ):
                get_most_frequent_dict(ents_dict, lctns_dict, q, pid)

        else:
            # Find the included times and the timespan for each sub-location element
            def get_valid_timespan_dict(ents_dict, lctns_dict, qid, pid):
                """
                Returns the sub-location's id, lbl, and the valid timespan so it can be used in subsetting
                """
                if pid in wd_utils.load_ent(ents_dict, qid)["claims"].keys():
                    subs_info = {
                        sub[0]: {"lbl": sub[1], "valid_timespan": sub[2]}
                        for sub in [
                            [
                                wd_utils.get_prop_id(ents_dict, qid, pid, i),
                                wd_utils.get_prop_lbl(ents_dict, qid, pid, i),
                                wd_utils.get_prop_timespan_intersection(
                                    ents_dict, qid, pid, i, timespan, interval
                                ),
                            ]
                            for i in range(len(wd_utils.get_prop(ents_dict, qid, pid)))
                        ]
                        if (
                            sub_lctns == True
                            or (sub_lctns != True and sub[1] in sub_lctns)
                            or (
                                sub_lctns != True
                                and sub[1]
                                not in [
                                    lctn[1:] for lctn in sub_lctns if lctn[0] == "~"
                                ]
                            )
                        )
                        and sub[2] != None
                    }

                else:
                    wd_utils.print_not_available(
                        ents_dict=ents_dict,
                        qid=qid,
                        pid=pid,
                        exrta_msg=" to derive sub_lctns",
                    )
                    subs_info = {}

                iter_set_dict(
                    dictionary=lctns_dict, key=qid, sub_key="sub_lctns", value=subs_info
                )

            for q in tqdm(
                depth_keys,
                desc=f"Depth {current_depth + 1} derived",
                total=len(depth_keys),
                disable=disable,
            ):
                get_valid_timespan_dict(ents_dict, lctns_dict, q, pid)

        depth -= 1
        current_depth += 1

        return depth, current_depth

    locations = utils._make_var_list(locations)[0]

    qids = [
        lctn_lbl_to_qid(lctn) if not wd_utils.is_wd_id(lctn) else lctn
        for lctn in locations
    ]

    if ents_dict == None:
        ents_dict = wd_utils.EntitiesDict()

    assign_first_iteration(
        ents_dict=ents_dict,
        lctns_dict=lctns_dict,
        qids=qids,
        #    multicore=multicore,
        verbose=verbose,
    )

    while depth > 0:
        depth, current_depth = assign_another_iteration(
            ents_dict=ents_dict,
            lctns_dict=lctns_dict,
            pid=pid,
            depth=depth,
            current_depth=current_depth,
            sub_lctns=sub_lctns,
            timespan=timespan,
            interval=interval,
            # multicore=multicore,
            verbose=verbose,
        )

    return lctns_dict


def derive_depth(a_dict, depth=0):
    """
    Derives the depth of a LocationsDict
    """
    if a_dict != {}:  # an empty sub_lctn
        if "sub_lctns" in a_dict[list(a_dict.keys())[0]].keys():
            depth += 1
            return derive_depth(
                a_dict[list(a_dict.keys())[0]]["sub_lctns"], depth=depth
            )

        else:

            return depth

    else:
        return depth


def merge_lctn_dicts(ld1, ld2):
    """
    Merges two location dictionaries conditionally on them having the same depth
    """
    assert (
        type(ld1) == LocationsDict and type(ld2) == LocationsDict
    ), "This merge is valid only for LocationsDict objects."
    depth_1 = derive_depth(ld1)
    depth_2 = derive_depth(ld2)

    if depth_1 == depth_2:
        for k in ld2.keys():
            ld1[k] = ld2[k]

        return ld1

    else:
        ValueError("Two LocationsDict objects of different depth have been passed.")


def iter_key_items(node, kv):
    """
    Finds the items of a nested dictionary key
    """
    if isinstance(node, list):
        for i in node:
            for x in iter_key_items(i, kv):
                yield x

    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in iter_key_items(j, kv):
                yield x


class LocationsDict(dict):
    """
    A dictionary for storing WikiData locations

    Keywords are QIDs, and values are dictionaries of depth, interval, and timespan specific information
    """

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super(LocationsDict, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "%s" % self.__class__

    def __str__(self):
        return """
    The LocationsDict class is meant to store information needed to query locations
        - Keys are QIDs
        - Values are dictionaries containing:
            - lbl: the location's label
            - valid_timespan: the timespan that the location is valid for given a interval and timespan
            - sub_lctns: equivalent dictionary objects for sub-locations given a depth

            Note: the last two are optional

    Because of the potential size, print() has been disabled.

    All other dictionary methods are included, as well as:
        key_lbls_list - a list of all location labels
        get_depth - the depth
        iter_key_items - the items within a key
        iter_set - finds and sets a key
        get_qids_at_depth - finds all QIDs at a given depth
        key_lbls_at_depth - the key labels at a given depth
        _print - prints the full LocationsDict
    """

    def key_lbls_list(self):
        """
        Provides a list of all location labels in the LocationsDict
        """
        return list(iter_key_items(self, "lbl"))

    # def key_lbls_dict(self):
    #     """
    #     Provides a dict of location labels in the LocationsDict
    #     """
    #     return # a dictionary created by a recursive lookup of those elements that have the key 'lbl'

    def get_depth(self):
        """
        The depth of the LocationsDict
        """
        return derive_depth(self, depth=0)

    # def get_interval(self):
    #     """
    #     The interval of the LocationsDict
    #     """
    #     return self['interval']

    # def get_timespan(self):
    #     """
    #     The timespan of the LocationsDict
    #     """
    #     return self['timespan']

    # def get_lctn_dict_specs(self, depth, timespan, interval):
    #     """
    #     Combines get_depth, get_interval, and get_timespan of a LocationsDict
    #     """
    #     if depth == None:
    #         depth = self.get_depth()
    #     if interval == None:
    #         interval = self.get_interval()
    #     if timespan == None:
    #         timespan = self.get_timespan()

    #     return depth, timespan, interval

    def iter_key_items(self, kv):
        """
        The items within a key in LocationsDict
        """
        return iter_key_items(self, kv)

    def iter_set(self, key, sub_key, value):
        """
        Finds and sets a key in LocationsDict
        """
        return iter_set_dict(self, key, sub_key, value)

    def get_qids_at_depth(self, depth=None):
        """
        Finds all QIDs at a given depth of a LocationsDict
        """
        qids_at_depth = get_qids_at_depth(self, depth=depth)

        return qids_at_depth

    def key_lbls_at_depth(self, ents_dict, depth):
        """
        Provides a list of key labels at a given depth
        """
        qids_at_depth = get_qids_at_depth(self, depth=depth)

        return [wd_utils.get_lbl(ents_dict=ents_dict, pq_id=q) for q in qids_at_depth]

    def _print(self):
        """
        Prints the full LocationsDict
        """
        return {k: v for k, v in self.items()}
