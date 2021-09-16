from flask_paginate import Pagination, get_page_args

# Pagination settings for routes below
# Adapted from:
# https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9
PER_PAGE = 8


def convert_to_pagination(
        games,
        PER_PAGE,
        page_param,
        per_page_param):
    """
    Prepares the list of games given to be paginated,
    and gives the page and per-page values for flask-paginate.
    """
    page, _, _, = get_page_args(
        page_parameter=page_param, per_page_parameter=per_page_param)

    offset = page * PER_PAGE - PER_PAGE
    total = len(games)

    pagination_args = Pagination(page=page,
                                 per_page=PER_PAGE,
                                 total=total,
                                 page_parameter=page_param,
                                 per_page_parameter=per_page_param)

    objs_to_display = games[offset: offset + PER_PAGE]

    return pagination_args, objs_to_display


# Convert list of ratings to average,
# and get number of ratings
def avg_ratings(ratings):
    num_ratings = len(ratings)
    avg = sum(ratings)/num_ratings
    return round(avg), num_ratings
