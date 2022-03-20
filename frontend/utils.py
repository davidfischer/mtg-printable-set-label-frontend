import datetime
import logging

import requests
from django.core.cache import cache
from django.utils import timezone


log = logging.getLogger(__name__)  # noqa


SCRYFALL_SETS_API_URL = "https://api.scryfall.com/sets"

# Cache the call to Scryfall to avoid hitting them that much
# Set data changes infrequently
SCRYFALL_SETS_CACHE_KEY = "scryfall-sets"
SCRYFALL_SETS_CACHE_DURATION = 60 * 60 * 8


def get_scryfall_set_data():
    cached_result = cache.get(SCRYFALL_SETS_CACHE_KEY)
    if cached_result:
        return cached_result

    log.debug("Fetching sets from Scryfall API...")
    resp = requests.get(SCRYFALL_SETS_API_URL)
    resp.raise_for_status()

    sets = resp.json()["data"]

    # Save the sets back to the cache
    cache.set(SCRYFALL_SETS_CACHE_KEY, sets, SCRYFALL_SETS_CACHE_DURATION)

    return sets


def get_grouped_sets():
    sets = {}
    for exp in get_scryfall_set_data():
        if exp["digital"]:
            # Skip digital only sets
            continue

        if exp["set_type"] in ("memorabilia", "token", "vanguard", "promo"):
            # Skip tokens and others sets that don't make sense
            continue

        # Skip sets released after today
        # This is important because sets with a failing SVG URL
        # will cause the whole process to break
        release_date = datetime.datetime.strptime(exp["released_at"], "%Y-%m-%d").date()
        if release_date > timezone.now().date():
            continue

        set_type = exp["set_type"].replace("_", " ")
        if set_type not in sets:
            sets[set_type] = []
        sets[set_type].append((exp["code"], exp))

    grouped_sets = []
    for set_type in sets:
        grouped_sets.append((set_type, sets[set_type]))

    grouped_sets.sort()

    return grouped_sets
