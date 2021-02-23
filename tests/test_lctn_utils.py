"""
Location Utilities Tests
------------------------
"""

from wikirepo.data import lctn_utils


def test_lctn_to_qid_dict():
    assert type(lctn_utils.lctn_to_qid_dict()) == dict


def test_qid_to_lctn_dict():
    assert type(lctn_utils.qid_to_lctn_dict()) == dict


def test_incl_lctn_lbls():
    assert len(lctn_utils.incl_lctn_lbls("world")) == 1
    assert len(lctn_utils.incl_lctn_lbls("continent")) == 7
    assert type(lctn_utils.incl_lctn_lbls("country")) == list
    assert type(lctn_utils.incl_lctn_lbls("region")) == list


def test_incl_lctn_ids():
    assert type(lctn_utils.incl_lctn_ids()) == list


def test_qid_to_lctn_lbl(qid):
    assert type(lctn_utils.qid_to_lctn_lbl(qid)) == str


def test_merge_lctn_dicts(lctns_dict):
    assert (
        type(lctn_utils.merge_lctn_dicts(ld1=lctns_dict, ld2=lctns_dict))
        == lctn_utils.LocationsDict
    )


def test_LocationsDict(ents_dict, lctns_dict):
    assert len(lctns_dict.key_lbls_list()) == 17  # Germany and all its states
    assert lctns_dict.get_depth() == 1
    assert lctns_dict.get_qids_at_depth(depth=0) == ["Q183"]
    assert type(lctns_dict.key_lbls_at_depth(ents_dict=ents_dict, depth=0)) == list
