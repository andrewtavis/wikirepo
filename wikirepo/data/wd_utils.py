"""
Utility functions for accessing and storing Wikidata information

Contents
--------
  0. No Class
      check_in_ents_dict
      load_ent
      is_wd_id
      prop_has_many_entries

      get_lbl
      get_prop
      get_prop_id
      get_prop_lbl
      get_prop_val
      prop_has_qualifiers
      get_qualifiers
      get_prop_qualifier_val
      get_val

      get_prop_t
      get_prop_start_t
      get_prop_end_t
      format_t
      get_formatted_prop_t
      get_formatted_prop_start_t
      get_formatted_prop_end_t
      get_prop_timespan_intersection
      get_formatted_prop_start_end_t
      prop_start_end_to_timespan
      get_prop_timespan

      dir_to_topic_page
      check_for_pid_sub_page
      t_to_prop_val_dict
      t_to_prop_val_dict_dict

  1. EntitiesDict
      __init__
      __repr__
      __str__
      key_lbls
      _print
"""

import numpy as np
from datetime import datetime
from datetime import date

from wikidata.client import Client

from wikirepo import utils
from wikirepo.data import time_utils

client = Client()


def check_in_ents_dict(ents_dict, qid):
    """
    Checks an the provided entity dictionary and adds to it if not present
    """
    if ents_dict is not None and qid not in ents_dict.keys():
        ents_dict[qid] = client.get(qid, load=True).data


def load_ent(ents_dict, pq_id):
    """
    Loads an entity
    """
    if pq_id[0] == "Q":
        if pq_id not in ents_dict.keys():
            check_in_ents_dict(ents_dict, pq_id)
        return ents_dict[pq_id]

    else:
        return client.get(pq_id, load=True).data


def is_wd_id(var):
    """
    Checks whether a variable is a Wikidata id
    """
    if var[0] == "Q" and var.split("Q")[1].isnumeric():  # check if it's a QID
        return True

    if var[0] == "P" and var.split("P")[1].isnumeric():  # check if it's a PID
        return True

    return False


def prop_has_many_entries(prop_ent):
    """
    Check if a Wikidata entry has multiple values for a given property
    """
    try:
        prop_ent[1]
        return True
    except:
        return False


def print_not_available(ents_dict=None, qid=None, pid=None, exrta_msg=""):
    """
    Notify the user that a given property is not available for a given subject
    """
    print(
        f"{get_lbl(ents_dict, qid)} '{qid}' currently does not have the '{get_lbl(ents_dict, pid)}' property '{pid}'{exrta_msg}."
    )


def get_lbl(ents_dict=None, pq_id=None):
    """
    Gets an English label of a Wikidata entity
    """
    if ents_dict == None and pq_id == None:
        return

    try:
        return load_ent(ents_dict, pq_id)["labels"]["en"]["value"]
    except:
        return load_ent(ents_dict, pq_id)["labels"]["de"]["value"]


def get_prop(ents_dict, qid, pid):
    """
    Gets property information from a Wikidata entity
    """
    check_in_ents_dict(ents_dict=ents_dict, qid=qid)  # checks for all further functions
    return ents_dict[qid]["claims"][pid]


def get_prop_id(ents_dict, qid, pid, i):
    """
    Gets the qid of an indexed property label of a Wikidata entity
    """
    return get_prop(ents_dict=ents_dict, qid=qid, pid=pid)[i]["mainsnak"]["datavalue"][
        "value"
    ]["id"]


def get_prop_lbl(ents_dict, qid, pid, i):
    """
    Gets a label of an indexed property label of a Wikidata entity
    """
    return get_lbl(
        ents_dict=ents_dict,
        pq_id=get_prop_id(ents_dict=ents_dict, qid=qid, pid=pid, i=i),
    )


def get_prop_val(ents_dict, qid, pid, i, ignore_char=""):
    """
    Gets a values of an indexed property label of a Wikidata entity
    """
    try:
        # Check to see if the value is a QID
        val = get_lbl(
            ents_dict=ents_dict,
            pq_id=get_prop(ents_dict=ents_dict, qid=qid, pid=pid)[i]["mainsnak"][
                "datavalue"
            ]["value"]["id"],
        ).replace(ignore_char, "")
        return val

    except:
        pass

    try:
        val = get_prop(ents_dict=ents_dict, qid=qid, pid=pid)[i]["mainsnak"][
            "datavalue"
        ]["value"]["amount"].replace(ignore_char, "")
        try:
            return int(val)
        except:
            pass
        try:
            return float(val)
        except:
            return val
    except:
        pass

    try:
        val = get_prop(ents_dict=ents_dict, qid=qid, pid=pid)[i]["mainsnak"][
            "datavalue"
        ]["value"].replace(ignore_char, "")
        try:
            return int(val)
        except:
            pass
        try:
            return float(val)
        except:
            return val
    except:
        # Property has no datavalue at the given index
        return np.nan


def prop_has_qualifiers(ents_dict, qid, pid, i):
    """
    Checks if the property has qualifiers
    """
    return "qualifiers" in get_prop(ents_dict=ents_dict, qid=qid, pid=pid)[i].keys()


def get_qualifiers(ents_dict, qid, pid, i):
    """
    Gets the qualifiers of a property of a Wikidata entity
    """
    return get_prop(ents_dict=ents_dict, qid=qid, pid=pid)[i]["qualifiers"]


def get_prop_qualifier_val(ents_dict, qid, pid, sub_pid, i, ignore_char=""):
    """
    Gets a values of an indexed qualifier property label of a Wikidata entity
    """
    try:
        # Check to see if the value is a QID
        val = get_lbl(
            ents_dict=ents_dict,
            pq_id=get_prop(ents_dict=ents_dict, qid=qid, pid=pid)[i]["qualifiers"][
                sub_pid
            ][0]["datavalue"]["value"]["id"],
        ).replace(ignore_char, "")
        return val

    except:
        pass

    try:
        val = get_prop(ents_dict=ents_dict, qid=qid, pid=pid)[i]["qualifiers"][sub_pid][
            0
        ]["datavalue"]["value"]["amount"].replace(ignore_char, "")
        try:
            return int(val)
        except:
            pass
        try:
            return float(val)
        except:
            return val
    except:
        pass

    try:
        val = get_prop(ents_dict=ents_dict, qid=qid, pid=pid)[i]["qualifiers"][sub_pid][
            0
        ]["datavalue"]["value"].replace(ignore_char, "")
        try:
            return int(val)
        except:
            pass
        try:
            return float(val)
        except:
            return val
    except:
        # Property has no datavalue at the given index
        return np.nan


def get_val(ents_dict, qid, pid, sub_pid, i, ignore_char=""):
    """
    Combines get_prop_val, get_prop_qualifier_val, and boolean assignment
    """
    if sub_pid == bool:
        return True

    elif type(sub_pid) == str:
        return get_prop_qualifier_val(ents_dict, qid, pid, sub_pid, i, ignore_char)

    else:
        return get_prop_val(ents_dict, qid, pid, i, ignore_char)


def get_prop_t(pid, i):
    """
    Gets a value of 'P585' (point in time) from a Wikidata property
    """
    return pid[i]["qualifiers"]["P585"][0]["datavalue"]["value"]["time"]


def get_prop_start_t(pid, i):
    """
    Gets a value of 'P580' (start time) from a Wikidata property
    """
    try:
        return pid[i]["qualifiers"]["P580"][0]["datavalue"]["value"]["time"]
    except:
        return


def get_prop_end_t(pid, i):
    """
    Gets a value of 'P582' (end time) from a Wikidata property
    """
    try:
        return pid[i]["qualifiers"]["P582"][0]["datavalue"]["value"]["time"]
    except:
        return


def format_t(t):
    """
    Formats the date strings of a Wikidata entry
    """
    if t != None:
        return datetime.strptime(t[1:11].replace("-00", "-01"), "%Y-%m-%d").date()
    else:
        return t


def get_formatted_prop_t(ents_dict, qid, pid, i):
    """
    Gets the formatted 'P585' (point in time) from a Wikidata property
    """
    return format_t(get_prop_t(get_prop(ents_dict=ents_dict, qid=qid, pid=pid), i))


def get_formatted_prop_start_t(ents_dict, qid, pid, i):
    """
    Gets the formatted 'P580' (start time) from a Wikidata property
    """
    return format_t(
        get_prop_start_t(get_prop(ents_dict=ents_dict, qid=qid, pid=pid), i)
    )


def get_formatted_prop_end_t(ents_dict, qid, pid, i):
    """
    Gets the formatted 'P582' (end time) from a Wikidata property
    """
    return format_t(get_prop_end_t(get_prop(ents_dict=ents_dict, qid=qid, pid=pid), i))


def get_prop_timespan_intersection(ents_dict, qid, pid, i, timespan, interval):
    """
    Combines get_formatted_prop_start_end_t and prop_start_end_to_timespan
    """
    included_times = time_utils.make_timespan(timespan=timespan, interval=interval)

    start_t = get_formatted_prop_start_t(ents_dict, qid, pid, i)
    end_t = get_formatted_prop_end_t(ents_dict, qid, pid, i)

    if interval == None and timespan == None:
        # We want the most recent data, so return the end date if it exists, or today's date
        if start_t == None and end_t != None:
            return

        elif start_t != None and end_t != None:
            return

        elif start_t == None and end_t == None:
            prop_t_intersection = [
                time_utils.truncate_date(date.today(), interval="daily")
            ]

        else:
            prop_t_intersection = [
                time_utils.truncate_date(date.today(), interval="daily")
            ]

    else:
        if start_t != None and end_t != None:
            if all(start_t > t for t in included_times) or all(
                end_t < t for t in included_times
            ):
                return

            else:
                prop_t_intersection = [
                    t for t in included_times if t >= start_t and t <= end_t
                ]

        elif start_t != None and end_t == None:
            if all(start_t > t for t in included_times):
                return

            else:
                prop_t_intersection = [t for t in included_times if t >= start_t]

        elif start_t == None and end_t != None:
            if all(end_t < t for t in included_times):
                return

        else:
            prop_t_intersection = included_times

    try:
        prop_t_intersection = [
            time_utils.truncate_date(t, interval=interval) for t in prop_t_intersection
        ]
    except:
        return

    return prop_t_intersection


def dir_to_topic_page(dir_name=None, ents_dict=None, qid=None):
    """
    Allows for the checking of subject entities for a given QID

    Parameters
    ----------
        dir_name : str (default=None)
            The name of the directory within wikirepo.data

        ents_dict : wd_utils.EntitiesDict (default=None)
            A dictionary with keys being Wikidata QIDs and values being their entities

        qid : str (default=None)
            Wikidata QID for a location

    Returns
    -------
        topic_qid or None : str or None
            The qid for an existing topic for the location or None to cancel later steps
    """
    # Needs sub-topics for other wikirepo directories
    name_to_topic_pid_dict = {"economic": "P8744", "geographic": "P2633"}

    if dir_name in name_to_topic_pid_dict.keys():
        topic_pid = name_to_topic_pid_dict[dir_name]

        if topic_pid in load_ent(ents_dict, qid)["claims"].keys():
            topic_qid = get_prop_id(ents_dict, qid, topic_pid, i=0)

            return topic_qid

        else:
            return

    else:
        return


def check_for_pid_topic_page(
    dir_name=None,
    ents_dict=None,
    qid=None,
    orig_qid=None,
    pid=None,
    interval=None,
    timespan=None,
    vd_or_vdd="vd",
):
    """
    Tries to find a topic-page for the topic of the current directory and return the needed variables

    Parameters
    ----------
        dir_name : str (default=None)
            The name of the directory within wikirepo.data

        ents_dict : wd_utils.EntitiesDict (default=None)
            A dictionary with keys being Wikidata QIDs and values being their entities

        qid : str (default=None)
            Wikidata QID for a location

        orig_qid : str (default=None)
            Maintains the original QID for assignment if qid is changed to that of the topic-page

        pid : str (default=None)
            The Wikidata property that is being queried

        timespan : two element tuple or list : contains datetime.date or tuple (default=None: (date.today(), date.today()))
            A tuple or list that defines the start and end dates to be queried
            Note 1: if True, then the full timespan from 1-1-1 to the current day will be queried
            Note 2: passing a single entry will query for that date only

        interval : str (default=None)
            The time interval over which queries will be made
            Note 1: see data.time_utils for options
            Note 2: if None, then only the most recent data will be queried

        vd_or_vdd : str (default=vd)
            Whether the function is being called in val_dict or val_dict_dict
            Note: this controls the depth of the returned placeholders

    Returns
    -------
        qid, orig_qid, t_p_d, skip_assignment : str, str, dict, bool
            Arguments necessary to derive if and how assignment should occur
    """
    topic_qid = dir_to_topic_page(dir_name, ents_dict, qid)

    t_p_d = {}
    skip_assignment = False
    if topic_qid != None and pid in load_ent(ents_dict, topic_qid)["claims"].keys():
        # A sub-page for the location that has the property exists
        # Save the original QID for assignment and replace with the topic page for access
        orig_qid = qid
        qid = topic_qid

    else:
        print_not_available(ents_dict=ents_dict, qid=qid, pid=pid, exrta_msg="")
        # Assign no date for on interval or the most recent time in the timespan with np.nan as a placeholder
        if interval == None and timespan == None:
            if vd_or_vdd == "vd":
                t_p_d = {"no date": np.nan}
            else:
                t_p_d = {"no date": {"no date": np.nan}}
        else:
            if vd_or_vdd == "vd":
                t_p_d = {
                    time_utils.truncated_latest_date(
                        timespan=timespan, interval=interval
                    ): np.nan
                }
            else:
                t_p_d = {
                    time_utils.truncated_latest_date(
                        timespan=timespan, interval=interval
                    ): {get_prop_val(ents_dict, qid, pid, i=0, ignore_char=""): np.nan}
                }

        skip_assignment = True

    return qid, orig_qid, t_p_d, skip_assignment


def t_to_prop_val_dict(
    dir_name=None,
    ents_dict=None,
    qids=None,
    pid=None,
    sub_pid=None,
    interval=None,
    timespan=None,
    ignore_char="",
    span=False,
):
    """
    Gets a dictionary of property value(s) indexed by time(s) from a locational entity

    Note: used to assign property values to a single column (values cannot have the same time value)

    Parameters
    ----------
        dir_name : str (default=None)
            The name of the directory within wikirepo.data

        ents_dict : wd_utils.EntitiesDict (default=None)
            A dictionary with keys being Wikidata QIDs and values being their entities

        qids : str or list (contains strs) (default=None)
            Wikidata QIDs for locations

        pid : str (default=None)
            The Wikidata property that is being queried

        sub_pid : str (default=None)
            The Wikidata property that subsets time values

        timespan : two element tuple or list : contains datetime.date or tuple (default=None: (date.today(), date.today()))
            A tuple or list that defines the start and end dates to be queried
            Note 1: if True, then the full timespan from 1-1-1 to the current day will be queried
            Note 2: passing a single entry will query for that date only

        interval : str (default=None)
            The time interval over which queries will be made
            Note 1: see data.time_utils for options
            Note 2: if None, then only the most recent data will be queried

        ignore_char : str (default='', no character to ignore)
            Characters in the output that should be ignored

        span : bool (default=False)
            Whether to check for P580 'start time' and P582 'end time' to create spans

    Returns
    -------
        t_prop_dict : dict
            A dictionary of Wikidata properties indexed by their time
    """
    qids = utils._make_var_list(qids)[0]

    if interval != None:
        included_times = [
            time_utils.truncate_date(t, interval=interval)
            for t in time_utils.make_timespan(timespan=timespan, interval=interval)
        ]
    else:
        # Triggers acceptance of a all values so that the most recent can be selected
        included_times = None

    t_prop_dict = {}
    for q in qids:
        t_p_d = {}
        orig_qid = None
        skip_assignment = False
        if pid not in load_ent(ents_dict, q)["claims"].keys():
            q, orig_qid, t_p_d, skip_assignment = check_for_pid_topic_page(
                dir_name=dir_name,
                ents_dict=ents_dict,
                qid=q,
                orig_qid=orig_qid,
                pid=pid,
                timespan=timespan,
                interval=interval,
                vd_or_vdd="vd",
            )

        if skip_assignment == False:
            if span:
                for i in range(len(get_prop(ents_dict, q, pid))):
                    prop_t_intersection = get_prop_timespan_intersection(
                        ents_dict, q, pid, i, timespan, interval
                    )
                    if prop_t_intersection != None:
                        for t in prop_t_intersection:
                            if t in t_p_d.keys():
                                t_p_d[t] = str(t_p_d[t])
                                t_p_d[t] += ", " + str(
                                    get_val(ents_dict, q, pid, sub_pid, i, ignore_char)
                                )

                            else:
                                t_p_d[t] = get_val(
                                    ents_dict, q, pid, sub_pid, i, ignore_char
                                )

            else:
                for i in range(len(get_prop(ents_dict, q, pid))):
                    try:
                        t = time_utils.truncate_date(
                            get_formatted_prop_t(ents_dict, q, pid, i),
                            interval=interval,
                        )
                    except:
                        if interval == None and timespan == None:
                            t = "no date"

                        else:
                            # Assign the most recent time in the timespan
                            t = time_utils.truncated_latest_date(
                                timespan=timespan, interval=interval
                            )

                    if (included_times != None and t in included_times) or (
                        included_times == None
                    ):
                        t_p_d[t] = get_val(ents_dict, q, pid, sub_pid, i, ignore_char)

        if orig_qid == None:
            t_prop_dict[q] = t_p_d
        else:
            t_prop_dict[orig_qid] = t_p_d

    return t_prop_dict


def t_to_prop_val_dict_dict(
    dir_name=None,
    ents_dict=None,
    qids=None,
    pid=None,
    sub_pid=None,
    interval=None,
    timespan=None,
    ignore_char="",
    span=False,
):
    """
    Gets a dictionary of dictionaries of multiple property values that are indexed by time(s) from a locational entity

    Note: used to assign property values to separate columns (values can have the same time value)

    Parameters
    ----------
        dir_name : str (default=None)
            The name of the directory within wikirepo.data

        ents_dict : wd_utils.EntitiesDict (default=None)
            A dictionary with keys being Wikidata QIDs and values being their entities

        qids : str or list (contains strs) (default=None)
            Wikidata QIDs for locations

        pid : str (default=None)
            The Wikidata property that is being queried

        sub_pid : str (default=None)
            The Wikidata property that subsets time values

        timespan : two element tuple or list : contains datetime.date or tuple (default=None: (date.today(), date.today()))
            A tuple or list that defines the start and end dates to be queried
            Note 1: if True, then the full timespan from 1-1-1 to the current day will be queried
            Note 2: passing a single entry will query for that date only

        interval : str (default=None)
            The time interval over which queries will be made
            Note 1: see data.time_utils for options
            Note 2: if None, then only the most recent data will be queried

        ignore_char : str (default='', no character to ignore)
            Characters in the output that should be ignored

        span : bool (default=False)
            Whether to check for P580 'start time' and P582 'end time' to create spans

    Returns
    -------
        t_prop_dict : dict
            A dictionary of Wikidata properties indexed by their time
    """
    qids = utils._make_var_list(qids)[0]

    if interval != None:
        included_times = [
            time_utils.truncate_date(t, interval=interval)
            for t in time_utils.make_timespan(timespan=timespan, interval=interval)
        ]
    else:
        # Triggers acceptance of a all values so that the most recent can be selected
        included_times = None

    t_prop_dict = {}
    for q in qids:
        t_p_d = {}
        orig_qid = None
        skip_assignment = False
        if pid not in load_ent(ents_dict, q)["claims"].keys():
            q, orig_qid, t_p_d, skip_assignment = check_for_pid_topic_page(
                dir_name=dir_name,
                ents_dict=ents_dict,
                qid=q,
                orig_qid=orig_qid,
                pid=pid,
                timespan=timespan,
                interval=interval,
                vd_or_vdd="vdd",
            )

        if skip_assignment == False:
            if span:
                for i in range(len(get_prop(ents_dict, q, pid))):
                    if "qualifiers" not in get_prop(ents_dict, q, pid)[i].keys():
                        prop_t_intersection = included_times

                    else:
                        prop_t_intersection = get_prop_timespan_intersection(
                            ents_dict, q, pid, i, timespan, interval
                        )

                    if prop_t_intersection != None:
                        for t in prop_t_intersection:
                            if t not in t_p_d.keys():
                                t_p_d[t] = {}
                                t_p_d[t][
                                    get_prop_val(ents_dict, q, pid, i, ignore_char)
                                ] = get_val(ents_dict, q, pid, sub_pid, i, ignore_char)

                            else:
                                t_p_d[t][
                                    get_prop_val(ents_dict, q, pid, i, ignore_char)
                                ] = get_val(ents_dict, q, pid, sub_pid, i, ignore_char)

            else:
                for i in range(len(get_prop(ents_dict, q, pid))):
                    try:
                        t = time_utils.truncate_date(
                            get_formatted_prop_t(ents_dict, q, pid, i),
                            interval=interval,
                        )
                    except:
                        if interval == None and timespan == None:
                            t = "no date"

                        else:
                            # Assign the most recent time in the timespan
                            t = time_utils.truncated_latest_date(
                                timespan=timespan, interval=interval
                            )

                    if (included_times != None and t in included_times) or (
                        included_times == None
                    ):
                        if t not in t_p_d.keys():
                            t_p_d[t] = {}
                            t_p_d[t][
                                get_prop_val(ents_dict, q, pid, i, ignore_char)
                            ] = get_val(ents_dict, q, pid, sub_pid, i, ignore_char)
                        else:
                            t_p_d[t][
                                get_prop_val(ents_dict, q, pid, i, ignore_char)
                            ] = get_val(ents_dict, q, pid, sub_pid, i, ignore_char)

        if orig_qid == None:
            t_prop_dict[q] = t_p_d
        else:
            t_prop_dict[orig_qid] = t_p_d

    return t_prop_dict


class EntitiesDict(dict):
    """
    A dictionary for storing WikiData entities

    Keywords are QIDs, and values are QID entities
    """

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super(EntitiesDict, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "%s" % self.__class__

    def __str__(self):
        return """
    The EntitiesDict class is meant to store WikiData entities.
        - Keys are QIDs
        - Values are QID entities

    Because of the potential size, print() has been disabled.

    All other dictionary methods are included, as well as:
        key_lbls - a list of labels of the QID keys
        _print - prints the full dictionary
    """

    def key_lbls(self):
        """
        Provides a list of the labels of all entities within the dictionary
        """
        return [get_lbl(ents_dict=self, pq_id=q) for q in self.keys()]

    def _print(self):
        """
        Prints the full entities dictionary (not advisable)
        """
        return {k: v for k, v in self.items()}
