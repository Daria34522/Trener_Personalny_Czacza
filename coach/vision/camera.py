import cv2


class Camera:
    def __init__(
        self, name: str, camera_source: str | int, camera_resolution: tuple[int, int]
    ):
        self.__name = name
        self.__camera_source = camera_source
        self.__camera_resolution = camera_resolution
        self.capture = cv2.VideoCapture(self.__camera_source)

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.__camera_resolution[0])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__camera_resolution[1])

    def __str__(self) -> str:
        return self.__name

    def is_opened(self) -> bool:
        return self.capture.isOpened()

    def read_frame(self) -> tuple[bool, cv2.typing.MatLike]:
        return self.capture.read()

    def release(self) -> None:
        self.capture.release()
