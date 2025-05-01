from typing import Optional


def to_percent_used(total: Optional[int], free: Optional[int]
                    ) -> Optional[float]:
    if free is None or total is None or total <= 0:
        return
    return (1 - free / total) * 100
