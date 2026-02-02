## Student Name: Harnaindeep Kaur
## Student ID: 217621137

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict
#from datetime import datetime, timedelta

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.

    Args:
        events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
        meeting_duration: Desired meeting length in minutes
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """
    
    def to_minutes(t: str) -> int:
        h, m = map(int, t.split(":"))
        return h * 60 + m

    def to_time_str(minutes: int) -> str:
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    # working hours
    WORK_START = to_minutes("09:00")
    WORK_END = to_minutes("17:00")
    LUNCH_START = to_minutes("12:00")
    LUNCH_END = to_minutes("13:00")
    STEP = 15 

    #convert events to datetime objects
    busy = []
    for e in events:
        start = to_minutes(e["start"])
        end = to_minutes(e["end"])
        if end <= WORK_START or start >= WORK_END:
            continue
        busy.append((max(start, WORK_START), min(end, WORK_END)))

    busy.sort()

    # find free times
    free_times = []
    current_time = WORK_START
    
    for start, end in busy:
        if start > current_time:
            free_times.append((current_time, start))
        current_time = max(current_time, end)

    # add remaining time after last event
    if current_time < WORK_END:
        free_times.append((current_time, WORK_END))
    
    # generate valid slots
    valid_slots = []
    duration_delta = timedelta(minutes=meeting_duration)
    
    for start, end in free_intervals:
        t = start
        while t + meeting_duration <= end:
            slots.append(to_time_str(t))
            t += STEP

    return valid_slots

    # TODO: Implement this function
    raise NotImplementedError("suggest_slots function has not been implemented yet")