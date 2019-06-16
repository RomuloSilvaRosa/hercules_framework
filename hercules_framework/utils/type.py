
def check_type(needed_type_, **kwargs):
    var_name, item = kwargs.popitem()
    if not isinstance(needed_type_, list):
        needed_type_ = [needed_type_]
    for needed_type in needed_type_:
        if isinstance(item, needed_type):
            return
    raise TypeError("The {} object must be {}, not {}".
                    format(var_name, ', '.join([x.__name__
                                                for x in needed_type]), item.__class__.__name__))
