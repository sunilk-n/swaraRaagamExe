from dataclasses import dataclass, asdict
from typing import Optional, Tuple

from PySide6.QtCore import QSettings


@dataclass
class AppSettings:
    window_size: Tuple[int, int] = (1000, 600)
    last_used_folder: str = ""
    # settings: Optional[QSettings] = None
    extra_attr: Optional[dict] = None

    def __post_init__(self) -> None:
        self.extra_attr = {}
        self.settings = QSettings("swaraRaagam", "SwaraRaagamApp")
        if not self.settings.allKeys():
            self.save()
        self.load()

    def save(self) -> None:
        for key, value in asdict(self).items():
            if key not in ["extra_attr", "settings"]:
                self.settings.setValue(key, value)

        for key, value in self.extra_attr.items():
            self.settings.setValue(key, value)

    def load(self) -> None:
        for key, default_value in asdict(self).items():
            if key not in ["extra_attr", "settings"]:
                setattr(self, key, self.settings.value(key, default_value))

        for key in self.settings.allKeys():
            if key not in asdict(self):
                self.extra_attr[key] = self.settings.value(key)

    def __getattr__(self, item):
        if item in self.extra_attr.keys():
            return self.extra_attr[item]
        else:
            print(f"'AppSettings' object has no attribute '{item}'")
            return

    def __setattr__(self, key, value):
        if key == "settings" or key in asdict(self).keys():
            super().__setattr__(key, value)
        else:
            self.extra_attr[key] = value
            self.save()


if __name__ == '__main__':
    settings = AppSettings()
    settings.settings.clear()
    # settings.songs_path = "I:\\pythonFlask\\swaraRaagamExe\\assets"
    # print(settings.songs_path)
