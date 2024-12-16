def normalize_lists(*args, fill_value=None):
    value_to_use = fill_value
    lists_to_same_len = args
    langevonjederliste = [[len(xx), xx] for xx in lists_to_same_len]
    langevonjederliste.sort()
    maxlaengegroessteliste = langevonjederliste[-1][0]
    langevonjederliste = [
        xx[1] + [value_to_use] * (maxlaengegroessteliste - xx[0])
        for xx in langevonjederliste
    ]
    return langevonjederliste
