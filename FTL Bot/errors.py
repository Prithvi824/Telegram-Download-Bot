class VideoTooLongException(Exception):
    def __init__(self, video_duration, limit):
        self.video_duration = video_duration
        self.limit = limit
        super().__init__(f"Video duration of {video_duration} seconds exceeds the allowed limit of {limit} seconds.")
