from flask_restful import abort


def get_paginated_list(results, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    obj = {'start': start, 'limit': limit, 'count': count}
    if start == 1:
        obj['has_previous'] = False
    else:
        # start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['has_previous'] = True
    if start + limit > count:
        obj['has_next'] = False
    else:
        # start_copy = start + limit
        obj['has_next'] = True
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj


