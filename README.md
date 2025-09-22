# Overview
Useful scripts in various languages: for example, [extracting notes from a PowerPoint presentation](/microsoft/powerpoint/py/extract_notes.py) or [saving multiple version of an After Effects composition with different text](/adobe/aftereffects/extendscript/render_multiple.jsx).

# Running Scripts
## Python

Scripts without external dependencies can be run with your default version of Python:

```sh
python my_script.py
# or
python3 my_script.py
```

But scripts requiring specific Python versions or external libraries become more complicated.

[uv](https://github.com/astral-sh/uv) is a useful tool for running scripts that have [PEP 723](https://peps.python.org/pep-0723/) metadata. `uv` will automatically download the version of Python and remote dependencies specified in the metadata.

```sh
uv run my_script.py
```

## PowerShell

You may need to run `Set-ExecutionPolicy` to allow unsigned scripts to run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted
```

then:

```sh
./My-Script.ps1
```


## ExtendScript

Scripts can be run from most Adobe CC applications via `File -> Scripts -> Run Script...`

## OfficeScript
OfficeScript files must be run from the "Automate" tab of an open Excel spreadsheet.

# Writing Scripts
## Python

Python scripts should follow [PEP 723](https://peps.python.org/pep-0723/) standard for inline metadata and dependencies. 

[uv](https://github.com/astral-sh/uv) is a useful tool for creating scripts. 

To create a script:
```sh
uv init --script my_script.py
```

Add dependencies in the metadata at the top of the script source code:
```py
# /// script
# requires-python = ">=3.11.0"
# dependencies = [ 
#   ...Add dependencies here, e.g:
#   "chardet>=5.0.0",
#   ...
# ]
# ///

def main()->None:
    ...
```

### Resources
- [Python 3 latest version docs](https://docs.python.org/3/)
- [PEP 723](https://peps.python.org/pep-0723/)
- [UV](https://docs.astral.sh/uv/)

## PowerShell

Powershell scripts must maintain backwards compatibility with PowerShell 5.1, since it is the version pre-installed on Windows 10/11. 

### Resources

- [Getting started with PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/01-getting-started?view=powershell-7.5)

## ExtendScript

ExtendScript can be written in your IDE of choice and saved with a `.jsx` extension.

### Resources

- [Adobe CC Extensibility Directory](https://docsforadobe.dev/)
- [ExtendScript Documentation](https://extendscript.docsforadobe.dev/)
- [After Effects Scripting Documentation](https://ae-scripting.docsforadobe.dev/)


## OfficeScript

Excel has a built-in IDE for Office Script in the Automate tab.

### Resources
- [Microsoft Office Script Docs](https://learn.microsoft.com/en-us/office/dev/scripts/)
