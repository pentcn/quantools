from setuptools import setup, find_packages

setup(
    name = 'quantools',  # How you named your package folder (foo)
    packages=find_packages(),  # Chose the same as "name"
    version = '0.0.1', # Start with a small number and increase it with every change you make
    license='MIT', # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'quant development toolboxs',  # Give a short description about your library
    author = 'pentcn',  # Type in your name
    author_email = '7534199@qq.com', # Type in your E-Mail
    url = 'https://github.com/pentcn/quantools/',  # Provide either the link to your github or to your website
    download_url = 'https://github.com/pentcn/quantools/archive/master.zip',
    keywords = ['quant', 'tools'],  # Keywords that define your package best
    install_requires=['loguru','pandas'],
    
    classifiers = [
        'Development Status::3-Alpha', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience::Developers', # Define that your audience are developers
        'Topic::Software Development::Build Tools',
        'License::OSI Approved::MIT License', # Again, pick a license
        'Programming Language::Python::3', #Specify which pyhton versions that you want to support
        'Programming Language::Python::3.4',
        'Programming Language::Python::3.5',
        'Programming Language::Python::3.6',
    ],
)