def aslist(arg):
    if isinstance(arg, list):
        return arg
    if isinstance(arg, dict):
        return [arg]
    return list(arg)
