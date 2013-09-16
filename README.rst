tkReadOnly
==========

A set of Tkinter widgets for displaying readonly text and code.

Getting Started
---------------

tkReadOnly can be installed from PyPI::

    pip install tkreadonly

ReadOnlyText
------------

An extension of the ``ttk.Text`` widget that disables all user editing.

The builtin ttk.Text widget doesn't have a "readonly" mode. You can
disable the widget, but this also disables selection and other mouse
events, and it changes the color scheme of the text.

This widget captures and discards all insertion and deletion events on the
Text widget. This allows the widget to look and behave like a normal
``ttk.Text`` widget in all other regards.

Arguments
~~~~~~~~~

``ReadOnlyText`` takes the same arguments as the base ``ttk.Text`` widget.

Usage
~~~~~

Usage of ``ReadOnlyText`` is the same as usage for the base ``ttk.Text``
widget.

Example::

    from Tkinter import *

    from tkreadonly import ReadOnlyText

    # Create the main Tk window
    root = Tk()

    # Create a main frame
    main_frame = Frame(root)
    main_frame.grid(column=0, row=0, sticky=(N, S, E, W))

    # Put a ReadOnlyText widget in the main frame
    read_only = ReadOnlyText(main_frame)
    read_only.grid(column=0, row=0, sticky=(N, S, E, W))

    # Add text to the end of the widget.
    read_only.insert(END, 'Hello world')

    # Run the main loop
    root.mainloop()

ReadOnlyCode
------------

A composite widget that lets you display line number-annotated code,
with a vertical scrollbar. The syntax highlighting will be automatically
guessed from the filename and/or file contents.

Arguments
~~~~~~~~~

``style``

    The Pygments style sheet to use. Default is ``monokai``.


Attributes
~~~~~~~~~~

``filename``

    The filename currently being displayed. If you set this attribute,
    the path you provide will be loaded into the code window.

``line``

    The current line of the file. The current line will be highlighted.
    If you set this attribute, any existing current line will be cleared
    and the new line highlighted.

Methods
~~~~~~~

``refresh()``

    Force a reload of the current file.

``line_bind(sequence, func)``

    Bind the ``func`` event handler to the given event sequence on a line
    number. If an binding for the given sequence already exists, it will be
    overwritten.

    Supports ``<Button-1>``-``<Button-5>``, and ``<Double-1>``-``<Double-5>``
    sequences, with the ``Shift``, ``Alt``, and ``Control`` modifiers.

    When an event occurs, the handler will be invoked with a single argument -
    the event that occurred. This event object will have a ``line`` attribute
    that describes the line that generated the event.

``name_bind(sequence, func)``

    Bind ``func`` event handler to the given event sequence on a token in
    the code. If an binding for the given sequence already exists, it will
    be overwritten.

    Supports ``<Button-1>``-``<Button-5>``, and ``<Double-1>``-``<Double-5>``
    sequences, with the ``Shift``, ``Alt``, and ``Control`` modifiers.

    When an event occurs, the handler will be invoked with a single argument -
    the event that occurred. This event object will have a ``name`` attribute
    that describes the token that generated the event.

Usage
~~~~~

Example::

    from Tkinter import *
    import tkMessageBox

    from tkreadonly import ReadOnlyCode

    # Create the main Tk window
    root = Tk()

    # Create the main frame
    main_frame = Frame(root)
    main_frame.grid(column=0, row=0, sticky=(N, S, E, W))

    # Create a ReadOnlyCode widget in the main frame
    read_only = ReadOnlyCode(main_frame)
    read_only.grid(column=0, row=0, sticky=(N, S, E, W))

    # Show a particular file
    read_only.filename = '/path/to/file.py'

    # Highlight a particular line in the file
    read_only.line = 5

    # Set up a handler for a double click on a line number
    def line_handler(event):
        tkMessageBox.showinfo(message='Click on line %s' % event.line)

    read_only.line_bind('<Double-1>', line_handler)

    # Set up a handler for a single click on a code variable
    def name_handler(event):
        tkMessageBox.showinfo(message='Click on token %s' % event.name)

    read_only.name_bind('<Button-1>', name_handler)

    # Run the main event loop
    root.mainloop()


Known problems under Ubuntu
---------------------------

Ubuntu's packaging of Python omits the ``idlelib`` library from it's base
packge. If you're using Python 2.7 on Ubuntu 13.04, you can install
``idlelib`` by running::

    $ sudo apt-get install idle-python2.7

For other versions of Python and Ubuntu, you'll need to adjust this as
appropriate.

Problems under Windows
----------------------

If you're running Cricket in a virtualenv, you'll need to set an
environment variable so that Cricket can find the TCL graphics library::

    $ set TCL_LIBRARY=c:\Python27\tcl\tcl8.5

You'll need to adjust the exact path to reflect your local Python install.
You may find it helpful to put this line in the ``activate.bat`` script
for your virtual environment so that it is automatically set whenever the
virtualenv is activated.
