tkReadOnly
==========

A set of Tkinter widgets for displaying readonly text and code.

Getting Started
---------------

tkReadOnly can be installed from PyPI::

    pip install tkreadonly

ReadOnlyText
------------

An extension of the ``ttk.Text`` widget that disables all user input.

The builtin ttk.Text widget doesn't have a "readonly" mode - you can
disable the widget, but this also disables selection and other mouse
events, and it changes the color scheme of the text.

This widget captures the insertion and deletion events, and redirects
them to the bitbucket. This allows the rest of the widget to look and
behave like a normal ``ttk.Text`` widget

Arguments
~~~~~~~~~

``ReadOnlyText`` takes the same arguments as the base ``ttk.Text`` widget.

Usage
~~~~~

Usage of ``ReadOnlyText`` is the same as usage for the base ``ttk.Text``
widget.

Example::

    from Tkinter import *
    from ttk import *

    from tkreadonly import ReadOnlyText

    root = Tk()

    main_frame = Frame()
    main_frame.grid(column=0, row=0, sticky=(N, S, E, W))

    read_only = ReadOnlyText(main_frame)
    read_only.grid(column=0, row=0, sticky=(N, S, E, W))
    read_only.insert(END, 'Hello world')

    root.mainloop()

ReadOnlyCode
------------

A composite widget that lets you display line number-annotated code,
with a vertical scrollbar.

Arguments
~~~~~~~~~

style:

    The Pygments style sheet to use. Default is ``monokai``.

lexer:

    The Pygments lexer to use. Default is ``PythonLexer``.


Methods
~~~~~~~

show(filename, line=None, refresh=False):

    Show the given filename, highlighting the specific line number.
    If line is None, no line will be highlighted, and the window will
    be scrolled to line 1.

    The widget remembers the file that is currently loaded;
    if you present the same file again, it won't be reopened and reloaded.

    However, if you pass in refresh=False, it will be.

Usage
~~~~~


Example::

    from Tkinter import *
    from ttk import *

    from tkreadonly import ReadOnlyCode

    root = Tk()

    main_frame = Frame()
    main_frame.grid(column=0, row=0, sticky=(N, S, E, W))

    read_only = ReadOnlyCode(main_frame)
    read_only.grid(column=0, row=0, sticky=(N, S, E, W))
    read_only.show('/path/to/file.py', line=5)

    root.mainloop()

