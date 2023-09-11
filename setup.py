from setuptools import find_packages,setup
from typing import List

def get_requirements() -> List[str]:
    requirement_list: List[str] = []

    # Open the requirements.txt file and read its contents
    with open('requirements.txt', 'r') as file:
        for line in file:
            requirement_list.append(line.strip())

    return requirement_list

setup(
    name="sensor",
    version="0.0.1",
    author="Pavan Kumar Medarametla",
    author_email="pavankumarchowdary35@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements(),
)