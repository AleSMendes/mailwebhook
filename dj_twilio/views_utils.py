# -*- coding: utf-8 -*-


def WebhookMessageDetailToDictionary(data):
    if data == None:
        return None

    dictionary = {}
    dictionary["email_to"]       = data.usemail_toername
    dictionary["election_uuid"]  = data.election_uuid
    dictionary["event_name"]     = data.event_name
    dictionary["timestamp"]      = data.timestamp
    return dictionary

def get_json_list(query_set):
    list_objects = []
    for obj in query_set:
        dict_obj = {}
        for field in obj._meta.get_fields():
            try:
                if field.many_to_many:
                    dict_obj[field.name] = get_json_list(getattr(obj, field.name).all())
                    continue
                dict_obj[field.name] = getattr(obj, field.name)
            except AttributeError:
                continue
        list_objects.append(dict_obj)
    return list_objects
        