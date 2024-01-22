# Manage Geodata Utilities Installation

## Installation

If you are on Windows and have ArcGIS Pro installed you can follow the directions below. For all other cases, follow the directions for a [manual setup](docs/manual-setup.md).

Open the "Python Command Prompt" that comes with ArcGIS Pro and run the following:

```bash
cd /d %USERPROFILE%/Desktop && curl -LJO https://github.com/WIStCart/geodata-utils/archive/main.tar.gz && tar -xf geodata-utils-main.tar.gz --strip=1 "geodata-utils-main/install scripts" && cd "install scripts" && install.bat && cd .. && del /s /q "geodata-utils-main.tar.gz" && rd /s /q "install scripts"
```

When notepad opens, edit the 'solr instances' to fit your needs and save. You can then close notepad.

## Update `geodatautils` Library

```bash
python -m pip install --upgrade https://github.com/WIStCart/geodata-utils/archive/main.tar.gz
```

## Uninstall

To uninstall environment:

```bash
conda env remove --name geodata-utils
```

You can check what environments are installed with:

```bash
conda env list
```

If you just want to uninstall the `geodatautils` python library run:

```bash
python -m pip uninstall geodatautils
```