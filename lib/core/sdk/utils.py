import os
from pathlib import Path
from types import ModuleType
from typing import List


def get_all_modules(package: ModuleType, relative_package_dir: Path) -> List[str]:
    package_dir = str(relative_package_dir)
    modules = []
    for filename in os.listdir(package_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # Remove the '.py' extension
            full_module_name = f"{package.__name__}.{module_name}"
            modules.append(full_module_name)
    return modules
