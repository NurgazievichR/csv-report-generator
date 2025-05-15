COLUMNS_ORIGINALS = (
    "id",
    "email",
    "name",
    "department",
    "hours_worked",
    "hourly_rate",
)

COLUMNS_AND_ALIASES = (
    ("id", "pk"),
    ("email",),
    ("name",),
    ("department",),
    ("hours_worked",),
    (
        "hourly_rate",
        "rate",
        "salary",
    ),
)
