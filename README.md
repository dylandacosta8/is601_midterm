### <h1 align=center>Homework 6</h1>
---
<p align=center>This repository contains the dependencies and code for Homework 6 along with custom tests and newly added calculator functions</p>

<p align=center><b> On cloning the repository, please use</b></p>
<div align=center>

`pip install -r requirements.txt` or `pip3 install -r requirements.txt`

</div>

---

### The Homework meets the following goals:

<ol>
<li><b>Add, Subtract, Multiply, and Divide</b></li>
<li>Throw exception for <b>divide by zero</b> and test that the exception is thrown.</li>
<li>Use at least one class, at least one <b>static method</b>, at least one <b>class method</b>.</li>
<li>It needs to store a <b>history of calculations</b>, so that you can retrieve the last calculation, add a calculation.</li>
<li><b>Near 100% test coverage, pass pylint</b></li>
<li>Type hints for input parameter types and return types.</li>
<li>Implements a <b>pytest fixture</b> to the tests.</li>
<li>Implements a new command to pytest to generate N number of records, so that you can run the following command: <b>pytest --num_records=100</b> to generate 100 records.</li>
<li>Added a main.py file to serve as an entry point to your program and provide <b>command line utilities</b>.</li>
<li>Covers <b>REPL and command patterns</b> with four basic commands add, subtract, multiply and divide.</li>
<li>Implements a <b>menu command</b> that prints the command dictionary and gives and example of command usage</li>
<li>Implements a menu command to list available command and usage example.</li>
<li>Uses <b>Plugin architecture</b> to dynamically load new plugins.</li>
<li>Uses <b>multiprocessing</b> capabilities to enable commands to run on separate cores.</li>
<li>Uses a <b>.env</b> file to set environment variables that are used for logging verbosity.</li>
<li>Uses <b>logging</b> statements to trace the flow of the program and track application usage and security. This is the log file that is generated when the program is run <a href="https://github.com/dylandacosta8/is601_6/blob/main/calc.log"><b>Log File</b></a></li>
<li>Uses <b>Github Action Workflows</b> to run pytests.</li>
</ol>

---

### Packages Used:

<ol>
<li><b>pytest:</b> The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.</li>
<li><b>pytest-pylint:</b> Pylint analyses your code without actually running it. It checks for errors, enforces a coding standard, looks for code smells, and can make suggestions about how the code could be refactored.</li>
<li><b>pytest-cov: </b>Coverage.py is a tool for measuring code coverage of Python programs. It monitors your program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not.</li>
<li><b>Faker: </b>Faker is a Python package that generates fake data for you.</li>
<li><b><a href='https://docs.python.org/3/library/concurrent.futures.html'>concurrent.futures:</a></b> a high-level interface for asynchronously executing callables.</li>
<li><b>abc:</b> This module provides the infrastructure for defining abstract base classes (ABCs).</li>
<li><b>setuptools:</b> collection of enhancements to the Python distutils that allow developers to more easily build and distribute Python packages.</li>
<li><b>python-dotenv:</b> Used to load the environment variables from the .env file into the program.</li>
</ol>

---

### Calculator Functions:

<ol>
<li><b>Addition:</b> Adds two numbers</li>
<li><b>Subtraction:</b> Subtracts two numbers</li>
<li><b>Multiplication:</b> Multiplies two numbers</li>
<li><b>Division:</b> Divides two numbers and also catches the divide by zero exception</li>
<li><b>History:</b> Stores and clears history of the calculator
</ol>

---
### Usage
<ol>
<li>To run tests with fake data generated using Faker, use</li>

`pytest --num_records=100 --cov --pylint` <b>OR ---> </b> view at <a href="https://github.com/dylandacosta8/is601_6/actions"><b>GitHub Actions</b></a>.

<li>To run the command line utility use one of the following command:</li>

`python main.py`

You can then use the various command line commands like add, subtract, multiply and divide as such:

`add 2 3` or `divide 5 0`

<li>You can also use a menu command to list the available commands and see a usage guide.</li>


</ol>

---

<b>Note:</b> Test Cases have 100% coverage for all the above Calculator Functions using pytest. Use the following commands to execute the tests.

`pytest`
`pytest --pylint`
`pytest --pylint --cov`

---