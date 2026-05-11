# AVISPA CLP Instance Generator

## Requirements

```bash
pip install pyinstaller
```

## Create Executable

### Windows

```bash
pyinstaller --onefile --windowed --name "AVISPA_Generator" --icon=icon.ico generator.py
```

### Linux/Mac

```bash
pyinstaller --onefile --windowed --name "AVISPA_Generator" generator.py
```

The executable will be created in the `dist/` folder.

## Run from source

```bash
python generator.py
```
