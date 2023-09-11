# $src-template1 
A template for the src-layout of a Python project. 

There is a lot of content in the template for reminder or examples purposes.

## Usage
`clean.py` will remove the excess template content, and replace project-name place holders.

1. Set the name of your project
```py
# clean.py
...
# content ommitted
# Set the name of your project here
DEFAULT_PACKAGE_NAME = 'my_package'
...
```

2. Run `clean.py` 
```sh
python -m clean.py
```

3. Run `init_venv.bat` to create a virtual environment and install the project in editable mode.
```sh
init_venv.bat
```

## Github Settings 
### Pre-receive hooks 
- Reject ipynb output cells 

## src-layout 
The containg folder of this readme is a template for the 'src-layout', a popular layout for python projects and can be detected by *setuptools* for automatic package discovery.  

Read about package discovery in the setuptools docs [here](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#), including the advantages and disadvantages of [src-layout](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout). 

### Quick Description  
From the setuptools docs: 
> The project should contain a src directory under the project root and all modules and packages meant for distribution are placed inside this directory: 
``` 
project_root_directory 
├── pyproject.toml  # AND/OR setup.cfg, setup.py 
├── ... 
└── src/ 
    └── mypkg/ 
        ├── __init__.py 
        ├── ... 
        ├── module.py 
        ├── subpkg1/ 
        │   ├── __init__.py 
        │   ├── ... 
        │   └── module1.py 
        └── subpkg2/ 
            ├── __init__.py 
            ├── ... 
            └── module2.py 
``` 

> This layout is very handy when you wish to use automatic discovery, since you don’t have to worry about other Python files or folders in your project root being distributed by mistake. In some circumstances it can be also less error-prone for testing or when using [**PEP 420**](https://peps.python.org/pep-0420/)-style packages. On the other hand you cannot rely on the implicit `PYTHONPATH=`. to fire up the Python REPL and play with your package (you will need an [editable install](https://pip.pypa.io/en/stable/cli/pip_install/#editable-installs) to be able to do that) 
