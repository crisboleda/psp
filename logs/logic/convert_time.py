

# Utils
from datetime import datetime


class ConvertTime:

    @staticmethod
    def seconds_to_time(time_log):
        total_time = 0
        total_time += time_log.delta_time

        if not time_log.is_paused:
            last_restart = time_log.last_restart_time.replace(tzinfo=None)

            diff = (datetime.now() - last_restart).total_seconds()
            total_time += diff
        
        return total_time

