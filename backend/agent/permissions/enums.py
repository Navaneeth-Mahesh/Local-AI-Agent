from enum import Enum


class PermissionType(str, Enum):
    FILE_SYSTEM = "file_system"
    TERMINAL = "terminal"
    BROWSER = "browser"
    NETWORK = "network"