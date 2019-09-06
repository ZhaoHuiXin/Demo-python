# encoding:utf-8
import json

ORIGIN_FILE = "data.json"
PRE_HANDLE_RES = "format_data.txt"
TAG_CHAIN_HANDLE_RES = "barData.txt"
leaf_latest_group_name_map = dict()
group_name_level_map = dict()

level_map = {
    '通用': {"id": 1, "parent_id": 0, "prefix": "/"},
    'Det、video': {"id": 2, 'parent_id': 0, "prefix": "/"},
    'Det': {"id": 3, "parent_id": 0, "prefix": "/"},
    'video': {"id": 4, "parent_id": 0, "prefix": "/"},
    'FR': {"id": 5, "parent_id": 0, "prefix": "/"}
}




def pre_handler(wf):
    with open(ORIGIN_FILE, "r") as rf:
        data = json.load(rf)
    # print(data.keys())

    def se(item):
        if type(item) is dict:
            for k, v in item.items():
                if k in ['通用', 'Det、video', 'Det', 'video', 'FR']:
                    wf.write("top_title %s\n" % k)
                # print(0,k)
                if type(v) is dict:
                    # print(k)
                    se(v)
                # print(k)
                if type(v) is list:
                    for inner in v:
                        if type(inner) is dict:
                            wf.write("1 %s\n" % k)
                            se(inner)
                        if type(inner) is str:
                            wf.write(k + ' ' + inner + '\n')
                    wf.write("end\n")

    se(data)


def handle_foo():
    with open(PRE_HANDLE_RES, "r") as rf:
        data = rf.readlines()
    data = [l.strip('\n') for l in data]

    top_level = ''
    second_level = ''

    with open(TAG_CHAIN_HANDLE_RES, "w") as wf:
        for line in data:
            if line.startswith("top_title"):
                top_level = line.split(" ")[1] + '/'
                continue
            if line.startswith("1"):
                second_level += line.split(' ')[1] + '/'
                continue
            if line.startswith("end"):
                res = second_level.split('/')
                if len(res) > 2:
                    res = res[:-2]
                    res.append('')
                    second_level = '/'.join(res)
                else:
                    second_level = ''
                continue
            wf.write(top_level + second_level + line + '\n')


def handle_bar():
    tag_group_sql = """insert into tag_group(`id`,`group_name`,`parent_id`,`prefix`) values"""
    tag_sql = """insert into tag(`name`, `group_id`) values"""
    n = 5
    tree_set = set()
    with open(TAG_CHAIN_HANDLE_RES, 'r') as rf:
        data = rf.readlines()
    data = [l.strip() for l in data]
    for line in data:
        chain_list = line.split(' ')
        tree_set.add(chain_list[0])
        leaf_latest_group_name_map[chain_list[1]] = chain_list[0].split('/')[-1]

    res = sorted(list(tree_set), key=lambda x: (x, len(x)))
    for l in res:
        items = l.split("/")
        if items[1] not in level_map:
            n += 1
            level_map[items[1]] = {
                "id": n,
                "parent_id": level_map[items[0]].get('id'),
                "prefix": "".join(["/", str(level_map[items[0]].get('id')), "/"])
            }
        if len(items) > 2:
            n += 1
            id_list = "/".join([str(level_map[item].get('id')) for item in items[:-1]])
            level_map[items[-1]] = {
                "id": n,
                "parent_id": level_map[items[-2]].get('id'),
                "prefix": "".join(["/", id_list, "/"])
            }
    for k, v in level_map.items():
        tag_group_sql += """({0},\"{1}\",{2},\"{3}\"),\n""".format(v['id'],
                                                      k,
                                                      v['parent_id'],
                                                      v['prefix'])

    res1 = tag_group_sql

    for k, v in leaf_latest_group_name_map.items():
        # print(k,v)
        tag_sql += """(\"{0}\",{1}),\n""".format(k, level_map[v].get('id'))
    res2 = tag_sql
    print(res1.rstrip() + "\b;")
    print(res2.rstrip() + "\b;")

if __name__ == '__main__':
    with open(PRE_HANDLE_RES, 'w') as wf:
        pre_handler(wf)
    handle_foo()
    handle_bar()
