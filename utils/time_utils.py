import re
from datetime import time
from typing import Optional

def parse_time_input(text: str, context: Optional[str] = None) -> Optional[time]:
    s = text.strip().lower()

    nums = re.findall(r'\d+', s)
    if not nums:
        return None

    if len(nums) >= 2:
        h = int(nums[0])
        m = int(nums[1])
    else:
        only = nums[0]
        # компактный формат HHMM
        if 3 <= len(only) <= 4:
            hhmm = only.zfill(4)      # '930' -> '0930'
            h = int(hhmm[:2])
            m = int(hhmm[2:])
        else:
            h, m = int(only), 0

    if context == 'sleep' and 8 <= h <= 12:
        h = (h + 12) % 24

    if h == 24:
        h = 0

    if 0 <= h <= 23 and 0 <= m <= 59:
        return time(hour=h, minute=m)
    return None
