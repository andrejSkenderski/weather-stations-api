OPERATORS = {
    "lt": lambda avg, ref: avg < ref,
    "gt": lambda avg, ref: avg > ref,
    "eq": lambda avg, ref: avg == ref,
    "lte": lambda avg, ref: avg <= ref,
    "gte": lambda avg, ref: avg >= ref,
}

CACHE_KEY_PREFIX = "city_stats:"
FILE_MTIME_KEY = "measurements:_file_mtime"
