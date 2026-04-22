def to_percent_used(total: int | None, free: int | None) -> float | None:
    if free is None or total is None or total <= 0:
        return
    return (1 - free / total) * 100
