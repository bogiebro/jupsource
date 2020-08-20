## Jupsource

This is a content manager for Jupyter notebooks that stores notebooks as normal scripts. 
Currently, only Python and Julia scripts are supported. 
When you use this extension, all scripts will become readable notebook files. Saving your notebook
will save right into the script. Markdown will be preserved as comments, as will any cell with a
semicolon at the end of a line.
Output and cell metadata will not be saved. 

To enable this content manager, you'll need to install [`jq`](https://stedolan.github.io/jq/),
install the package (`pip install jupsource`),
and add the following line to the file `.jupyter/jupyter_notebook_config.py`:

```python
c.NotebookApp.contents_manager_class = 'jupsource.TextFileManager
```

Now you easily put notebooks into version control systems, typecheck them with `mypy`,
search them for unit test definitions with `pytest`, and import them into other notebooks and scripts. 

## Creating a file

This library does not add menu items to create scripts to the Jupyter file browser. If you want
to edit a new script, just `touch` the file, and open the empty script in Jupyter.

If you want to convert an existing notebook into a script, run

```
python -m jupsource [notebook_name.ipynb] [script_name.py]
```

### Comparison with Jupytext

This project is similar to [Jupytext](jupytext.readthedocs.io/), but has important differences:

1. In Jupsource, notebooks ARE source files. In Jupytext, notebooks and source files get
synced automatically as you edit. Jupsource's approach avoids keeping two copies of every
file. 

2. Jupsource will comment out cells with lines that end in semicolons. This allows you to keep
your exploratory visualizations and tinkering in the same notebooks you use as libraries for
larger projects, as long as you remember to put a semicolon somewhere in your exploratory cells.

3. Jupytext is a full featured python library of hundreds of lines of code. Jupsource is hacked
together in a couple dozen lines of jq. This simplicity makes jupsource extremely easy to extend.
