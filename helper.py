import datetime as dt


def normalize_time_value(seconds):
    if seconds >= 3600:
        return f"{int(seconds // 3600)} год. {int((seconds % 3600) // 60)} хв. {int((seconds % 60))} с."
    elif seconds >= 60:
        return f"{int(seconds // 60)} хв. {int(seconds % 60)} с."
    else:
        return f"{int(seconds)} с."


def desc_seconds(start_time, seconds):
    return (
            dt.datetime.combine(dt.date.today(), start_time) + dt.timedelta(seconds=seconds)
    ).strftime("%H:%M:%S")


def desc_seconds_value(start_time, seconds):
    return (
            dt.datetime.combine(dt.date.today(), start_time) + dt.timedelta(seconds=seconds)
    )
