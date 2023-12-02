# Manual Setup

If you do not run windows, do not have ArcGIS Pro, or the install scripts are not working, use this document to manually install and set up `geodata-utils`.

## Virtual Environment

You'll need to create a virtual environment to ensure compatibility with dependencies. To do this, open the "Python Command Prompt" that comes with ArcGIS Pro:

```bash
conda create --name geodata-utils python=3.11.5 --yes
activate geodata-utils
```

## Install

Install `geodatautils` using Pip directly from the GitHub repository using:

```bash
python -m pip install --upgrade https://github.com/WIStCart/geodata-utils/archive/main.tar.gz
```

## Configure Settings

Run the following to open and set `config.yml`:

```bash
for /f "delims=" %i in ('python -c "from distutils.sysconfig import get_python_lib; from os.path import join; print(join(get_python_lib(),'geodatautils','config'))"') do set configpath=%i
ren %configpath%\config-template.yml config.yml
notepad %configpath%\config.yml
```

When notepad opens, edit the 'solr instances' to fit your needs and save.