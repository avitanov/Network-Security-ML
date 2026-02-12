from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path:str)->List[str]:
    requirements=[]
    try:
        with open(file_path) as file_obj:
            requirements=file_obj.readlines()
            requirements = [req.replace("\n", "") for req in requirements]
            if '-e .' in requirements:
                requirements.remove('-e .')
        return requirements
    except FileNotFoundError:
        print(f"{file_path} - file not found")


setup(
    name='cyber-security-ml',
    version='0.0.1',
    author='Atanas Vitanov',
    author_email='atanas_vitanov@yahoo.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)