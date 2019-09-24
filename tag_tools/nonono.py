import json

tags = []
tag_groups = []

n = 0  # tag_groups id count
m = 0  # tags id count


def par(data, prefix="/", parent_id=0):
    global n, m
    if type(data) == type({}):
        for k, v in data.items():
            n += 1
            k_id = n
            tag_groups.append({"id": k_id, "name": k, "parent_id":parent_id, "prefix":prefix})
            par(v, prefix=prefix+"%d/" % k_id, parent_id= k_id)

    if type(data) == type([]):
        for item in data:
            if type(item) == type(""):
                m += 1
                item_id = m
                tags.append({"name": item, "tag_id": item_id, "tag_group_id": parent_id})
            if type(item) == type({}):
                par(item, prefix=prefix, parent_id=parent_id)


if __name__ == '__main__':
    with open("TagDataV3.json") as rf:
        origin_data = json.load(rf)
    par(origin_data)
    tag_sql = """insert into tags(`id`, `name`, `tag_group_id`) values"""
    for i in range(len(tags)):
        if i == len(tags) - 1:
            tag_sql += """({0},\"{1}\",{2});""".format(tags[i]["tag_id"],tags[i]["name"],tags[i]["tag_group_id"])
            break
        tag_sql += """({0},\"{1}\",{2}),\n""".format(tags[i]["tag_id"], tags[i]["name"], tags[i]["tag_group_id"])

    tag_group_sql = """insert into tag_groups(`id`,`name`,`parent_id`,`prefix`) values"""
    for i in range(len(tag_groups)):
        if i == len(tag_groups) - 1:
            tag_group_sql += """({0},\"{1}\",{2},\"{3}\");""".format(
                tag_groups[i]['id'],
                tag_groups[i]['name'],
                tag_groups[i]['parent_id'],
                tag_groups[i]['prefix'])
            break
        tag_group_sql += """({0},\"{1}\",{2},\"{3}\"),\n""".format(tag_groups[i]['id'],
                                                                   tag_groups[i]['name'],
                                                                   tag_groups[i]['parent_id'],
                                                                   tag_groups[i]['prefix'])
    print(tag_sql)
    print(tag_group_sql)
