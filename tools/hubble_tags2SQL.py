# encoding:utf-8

import json
def pre_handler(wf):
    with open("data.json", "r") as rf:
        data = json.load(rf)
    print(data.keys())

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
if __name__ == '__main__':
    with open('format_data.txt', 'w') as wf:
        pre_handler(wf)
