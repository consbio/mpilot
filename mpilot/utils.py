def flatten(li):
    """ Flattens a list of lists of any depth to a 1D list and returns a generator """

    for item in li:
        if isinstance(item, (list, tuple)):
            for list_item in flatten(item):
                yield list_item
        else:
            yield item
