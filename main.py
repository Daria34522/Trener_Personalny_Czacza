from __future__ import annotations

import sys

from coach.interface.MainMenu import MainMenu
from PySide6.QtWidgets import QApplication


def main() -> int:
    app = QApplication(sys.argv)

    window = MainMenu()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
