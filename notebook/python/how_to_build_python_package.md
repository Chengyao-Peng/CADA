# Setting Up the Package
* Structure:
  * Project folder (booty)
    * src
      * package folder (booty)
* No dashes (-) in the name of the package
* Use [Semantic Versioning](https://semver.org/) for deciding the version in the setup.cfg
* Can pip install locally (pip install .)
* description should be one sentence
* long_description can refer to README
* Pick your [license](https://choosealicense.com/)
  * Usually use "MIT License"
    * Allows anyone to use your code as long as they give you credit

# Tests
* Create new folder ("Python Package") named tests in the project folder
* All python test files should be named "test_" followed by name of
* When creating test classes, should be named "Test<ModuleName>"
* Use TOX file to run tests to make sure it is done the right way
  * commands are commands run in the terminal (works both Windows and Unix)
  * The "py" in envlist refers to "testenv" section
  * TOX creates a sudo venv and redownloads packages to test everything from scratch
* PyRoma
  * Checks to make sure all of your metadata is there (e.g. version #s)

# CLI
* Use "Click" package to wrap functions and make CLI

# Requirements
* using "install_requires" in the setup.cfg to automatically install all necessary packages
  * Better than having a requirements.yml(txt) and doing it manually

# Uploading to PyPi
* Need to install twine to upload
* Inside your tox, should have "build" and "release" envs
  * When you make a "release", remove the "-dev" from the version number

# Documentation
* Put docstrings in every function and top of each module
* Make a "docs" folder in the repo
* Use ```sphinx-quickstart``` to create a template (make sure files are in docs folder)
  * In the "source" folder, make a .rst file for each module that you are documenting
* In "conf.py", Uncomment the "Path setup" code lines and put in the path to src folder ("../../src")
* Use ```make html``` to build the documentation
* In build/html folder, you can view the 'index.html'
