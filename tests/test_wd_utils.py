"""
Wikidata Utilities Tests
------------------------
"""

from wikirepo.data import wd_utils


entities_dict = wd_utils.EntitiesDict()


def test_load_ent(qid):
    wd_utils.load_ent(ents_dict=entities_dict, pq_id=qid)


def test_check_in_ents_dict(ents_dict, qid):
    wd_utils.check_in_ents_dict(ents_dict=ents_dict, qid=qid)


def test_is_wd_id(qid, pop_pid):
    assert wd_utils.is_wd_id(qid) == True

    assert wd_utils.is_wd_id(pop_pid) == True

    assert wd_utils.is_wd_id("Not") == False


def test_prop_has_many_entries():
    assert wd_utils.prop_has_many_entries(["No"]) == False
    assert wd_utils.prop_has_many_entries(["It", "does"]) == True


def test_get_lbl(ents_dict, pop_pid):
    assert wd_utils.get_lbl(ents_dict=None, pq_id=None) == None
    assert type(wd_utils.get_lbl(ents_dict=ents_dict, pq_id=pop_pid)) == str


def test_get_prop(ents_dict, qid, pop_pid):
    assert type(wd_utils.get_prop(ents_dict=ents_dict, qid=qid, pid=pop_pid)[0]) == dict


def test_get_prop_id(ents_dict, qid, exec_pid):
    assert wd_utils.is_wd_id(
        wd_utils.get_prop_id(ents_dict=ents_dict, qid=qid, pid=exec_pid, i=0)
    )


def test_get_prop_val(ents_dict, qid, pop_pid, exec_pid):
    assert (
        type(
            wd_utils.get_prop_val(
                ents_dict=entities_dict, qid=qid, pid=pop_pid, i=0, ignore_char=""
            )
        )
        == int
    )

    assert (
        type(
            wd_utils.get_prop_val(
                ents_dict=entities_dict, qid=qid, pid=exec_pid, i=0, ignore_char=""
            )
        )
        == str
    )
