def is_comment(item):
    return isinstance(item, str) and item.startswith("#")

def execute(program):
    while program:
        p = program.pop()
        if not is_comment(p):
            program.append(p)
            break
    else:  # nobreak
        print("program is empty")
        return

    pending = []
    while program:
        item = program.pop()
        if callable(item):
            try:
                result = item(*pending)
            except Exception as e:
                print("Error: ", e)
                break
            program.append(result)
            pending.clear()
        else:
            pending.append(item)
    else:  # nobreak
        print("Program successful")
        print("result: ", pending)


if __name__ == '__main__':
    import operator
    program = list(reversed((
        "# A short stack program to add",
        "# and multiply some constans",
        5,
        2,
        operator.add,
        3,
        operator.mul)))

    execute(program)