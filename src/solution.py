from typing import List, Dict

def suggest_slots(events, meeting_duration, day):

    if meeting_duration <= 0:
        return []

    def to_minutes(t):
        h, m = map(int, t.split(":"))
        return h * 60 + m

    def to_time_str(minutes):
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    WORK_START = to_minutes("09:00")
    WORK_END = to_minutes("17:00")
    LUNCH_START = to_minutes("12:00")
    LUNCH_END = to_minutes("13:00")
    FRIDAY_CUTOFF = to_minutes("15:00")
    STEP = 15

    is_friday = str(day).lower().startswith("fri") or str(day).endswith("-5")

    # Build busy intervals
    busy = []
    for e in events:
        start = to_minutes(e["start"])
        end = to_minutes(e["end"])
        if end <= WORK_START or start >= WORK_END:
            continue
        busy.append((max(start, WORK_START), min(end, WORK_END)))

    busy.sort()

    # Merge overlapping busy intervals
    merged_busy = []
    for start, end in busy:
        if not merged_busy:
            merged_busy.append((start, end))
        else:
            last_start, last_end = merged_busy[-1]
            if start <= last_end:
                merged_busy[-1] = (last_start, max(last_end, end))
            else:
                merged_busy.append((start, end))

    # Build free intervals
    free_times = []
    current_time = WORK_START
    for start, end in merged_busy:
        if start > current_time:
            free_times.append((current_time, start))
        current_time = max(current_time, end)
    if current_time < WORK_END:
        free_times.append((current_time, WORK_END))

    # Generate valid slots
    valid_slots = []
    for free_start, free_end in free_times:
        # Align to global STEP grid starting at WORK_START
        t = WORK_START + ((free_start - WORK_START + STEP - 1) // STEP) * STEP

        while t + meeting_duration <= free_end and t < WORK_END:
            if is_friday and t > FRIDAY_CUTOFF:
                break

            meeting_end = t + meeting_duration
            overlaps_lunch = not (meeting_end <= LUNCH_START or t >= LUNCH_END)

            if not overlaps_lunch:
                valid_slots.append(to_time_str(t))

            t += STEP

    return valid_slots