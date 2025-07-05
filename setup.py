from setuptools import setup,find_packages

def get_requirements()->list[str]:
    " This function will return list of requirements"
    req:list[str] = []
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip() ## Remove Empty Spaces
                if requirement and requirement != '-e .': # ignore empty lines and -e .
                    req.append(requirement)
    except FileNotFoundError:
        print('Requiremenst file not found')
        
    return req 

setup(
    name = 'NetworkSecurity',
    version='0.0.1',
    author='Prince Gabecha',
    packages=find_packages(),
    install_requires=get_requirements()
)