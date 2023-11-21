from setuptools import find_packages,setup
from typing import List

#Requirements.txt contains the names of all the packages present
REMOVE_PACKAGES="-e ."

def get_requirements(file_name)->List[str]:
    '''
    This function takes the filename which contains the modules and
    return the list of modules
    
    '''
    with open(file_name) as requirement_file:
        requirement_list=requirement_file.readlines()

    #removing the '\n' present in each line
    requirement_list=[req.replace("\n" ,"") for req in requirement_list]

    #removing the -e . present in the requirements.txt which is used to build the package
    if REMOVE_PACKAGES in requirement_list:
        requirement_list.remove(REMOVE_PACKAGES)
    
    return requirement_list


setup(name='Insurance',
       version="0.0.1",
       description='Insurance end to end project',
       author='Pritam kumar',
       author_email='singhpritam983@gmail.com',
       packages=find_packages(),
       install_requires=get_requirements('requirements.txt')
       )
