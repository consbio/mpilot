def flatten(li):
    """ Flattens a list of lists of any depth to a 1D list and returns a generator """

    for item in li:
        if isinstance(item, (list, tuple)):
            for list_item in flatten(item):
                yield list_item
        else:
            yield item


def insure_fuzzy(arr, fuzzy_min, fuzzy_max):
    """ Limits all array values in-place to fuzzy_min and fuzzy_max and returns the array """

    arr[arr > fuzzy_max] = fuzzy_max
    arr[arr < fuzzy_min] = fuzzy_min

    if arr.mask:
        arr.data[arr.mask] = arr.fill_value

    return arr
