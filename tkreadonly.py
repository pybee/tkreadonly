try:
    from idlelib.WidgetRedirector import WidgetRedirector
except ImportError:
    import platform
    import sys
    if platform.linux_distribution()[0] == 'Ubuntu':
        raise Exception("idlelib could not be found. " +
                        "You may need to install IDLE - try running " +
                        "'sudo apt-get install idle-python%s.%s'" % (
                            sys.version_info[0:2]
                        ))
    else:
        raise Exception("idlelib could not be found. " +
                        "Check your operating system instructions " +
                        "to work out how to install IDLE and idlelib.")

try:
    from Tkinter import *
    from ttk import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *

from pygments import lex
from pygments.lexers import guess_lexer_for_filename
from pygments.styles import get_style_by_name
from pygments.token import Token


__all__ = ('ReadOnlyText', 'ReadOnlyCode')


def normalize_sequence(sequence):
    """Normalize sequence names to a common format.

    This is required so that <1>, <Button-1>, and <ButtonPress-1> all
    map to the same handler, and so that <Alt-Shift-Control-1> and
    <Shift-Alt-Control-1> map to the same event.
    """
    # Split on the dash character
    parts = sequence[1:-1].split('-')

    if len(parts) == 1:
        # If there's only one part, it's a button press number
        normalized = ['Button', parts[-1]]
    else:
        # Look at the second last part. If it's Double, handle as a
        # double click. If it's Button or ButtonPress, handle as
        # Button. Otherwise, it's a button press.

        # Any modifiers before the bit describing the button/double
        # should be sorted alphabetically.
        if parts[-2] == 'Double':
            normalized = sorted(parts[:-2]) + parts[-2:]
        elif parts[-2] in ('Button', 'ButtonPress'):
            normalized = sorted(parts[:-2]) + ['Button', parts[-1]]
        else:
            normalized = sorted(parts[:-1]) + ['Button', parts[-1]]

    return '<%s>' % '-'.join(normalized)


def tk_break(*args, **kwargs):
    "Return a Tk 'break' event result."
    return "break"


def text_set(widget):
    "Create a function for `widget` that will respond to scroll events"
    def set_fn(start, end):
        widget.yview('moveto', start)
    return set_fn


def combine(*functions):
    """Combine multiple event handlers into a single combined handler.

    The return value for the last function provided will be returned as
    the return value for the full list.
    """
    def _combined(*args, **kwargs):
        for fn in functions:
            retval = fn(*args, **kwargs)
        return retval
    return _combined


class ReadOnlyText(Text):
    """A Text widget that redirects the insert and delete
    handlers so that they are no-ops. This effectively makes
    the widget readonly with respect to keyboard input handlers.

    Adapted from http://tkinter.unpythonic.net/wiki/ReadOnlyText, which
    is itself adapting a solution described here: http://wiki.tcl.tk/1152
    """
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        self.redirector = WidgetRedirector(self)
        self.insert = self.redirector.register("insert", tk_break)
        self.delete = self.redirector.register("delete", tk_break)


class ReadOnlyCode(Frame, object):
    """A widget for displaying read-only, syntax highlighted code.

    """
    def __init__(self, *args, **kwargs):
        # Get the code style
        self.style = get_style_by_name(kwargs.pop('style', 'monokai'))
        self.lexer = kwargs.pop('lexer', None)
        # Initialize the base frame with the remaining arguments.
        super(ReadOnlyCode, self).__init__(*args, **kwargs)

        # The file and line currently being displayed
        self._filename = None
        self._line = None

        # The list of bound event handlers
        # Handlers for actions on a line number
        self._line_bindings = {}
        # Handlers for actions on a tokenized NAME
        self._name_bindings = {}

        # The Text widget holding the line numbers.
        self.lines = Text(self,
            width=5,
            padx=4,
            highlightthickness=0,
            takefocus=0,
            bd=0,
            background='lightgrey',
            foreground='black',
            cursor='arrow',
            state=DISABLED
        )
        self.lines.grid(column=0, row=0, sticky=(N, S))

        # The Main Text Widget
        self.code = ReadOnlyText(self,
            width=80,
            height=25,
            wrap=NONE,
            background=self.style.background_color,
            highlightthickness=0,
            bd=0,
            padx=4,
            cursor='arrow',
        )
        self.code.grid(column=1, row=0, sticky=(N, S, E, W))

        # Set up styles for the code window
        for token in self.style.styles:
            self.code.tag_configure(str(token), **self._tag_style(token))

        self.code.tag_configure("current_line", background=self.style.highlight_color)

        # The widgets vertical scrollbar
        self.vScrollbar = Scrollbar(self, orient=VERTICAL)
        self.vScrollbar.grid(column=2, row=0, sticky=(N, S))

        # Tie the scrollbar to the text views, and the text views
        # to each other.
        self.code.config(yscrollcommand=combine(text_set(self.lines), self.vScrollbar.set))
        self.lines.config(yscrollcommand=combine(text_set(self.code), self.vScrollbar.set))
        self.vScrollbar.config(command=combine(self.lines.yview, self.code.yview))

        # Set up internal event handlers.
        for modifier in [
                    '',
                    'Alt-', 'Alt-Control-', 'Alt-Shift-', 'Alt-Control-Shift-',
                    'Control-', 'Control-Shift-',
                    'Shift-'
                ]:
            for action in ['Button', 'Double']:
                for button in range(1, 6):
                    sequence = '<%s%s-%s>' % (modifier, action, button)
                    self.lines.bind(sequence, self._on_line_handler(sequence))

                    self.code.tag_bind(str(Token.Name), sequence, self._on_name_handler(sequence))

        # Configure the weights for the grid.
        # All the weight goes to the code view.
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)

    def _tag_style(self, token):
        "Convert a heirarchical style definition into a Tk style string"
        if token.parent is not None:
            kwargs = self._tag_style(token.parent)
        else:
            kwargs = {}
        for part in self.style.styles[token].split():
            if part.startswith('#'):
                kwargs['foreground'] = part
            # elif part == 'bold':
            #     kwargs['font'] = part
            elif part.startswith('bg:'):
                kwargs['background'] = part[3:]
        return kwargs

    @property
    def filename(self):
        "Return the current file being displayed by the view"
        return self._filename

    @filename.setter
    def filename(self, value):
        "Set the file being displayed by the view"
        if self._filename != value:
            self.code.delete('1.0', END)
            with open(value) as code:
                all_content = code.read()
                if self.lexer:
                    lexer = self.lexer
                else:
                    lexer = guess_lexer_for_filename(value, all_content, stripnl=False)
                for token, content in lex(all_content, lexer):
                    self.code.insert(END, content, str(token))

            # Now update the text for the linenumbers
            end_index = self.code.index(END)
            line_count = int(end_index.split('.')[0])
            lineNumbers = '\n'.join('%5d' % i for i in range(1, line_count))
            self.lines.config(state=NORMAL)
            self.lines.delete('1.0', END)
            self.lines.insert('1.0', lineNumbers)
            self.lines.config(state=DISABLED)

            # Store the new filename, and clear any current line
            self._filename = value
            self._line = None

    def refresh(self):
        "Force a refresh of the file currently in the view"
        # Remember the old file, set the internal tracking of the
        # filename to None, then use the property to set the filename
        # again. Since the internal representation has changed, this
        # will force a reload.
        filename = self._filename
        self._filename = None
        self.filename = filename

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        # If the line is currently displayed, clear the current_line
        # tag from the code view.
        if self._line:
            self.code.tag_remove('current_line',
                '%s.0' % self._line,
                '%s.0' % (self._line + 1)
            )

        # Save the new value for the line
        self._line = value

        # If there is a new value for the line, set the current_line
        # tag from the code view, and make that line visible; if
        # there isn't a new line, set the view to point at line 1.
        if self._line:
            self.code.see('%s.0' % self._line)
            self.code.tag_add('current_line',
                '%s.0' % self._line,
                '%s.0' % (self._line + 1)
            )
        else:
            # Reset the view
            self.code.see('1.0')

    def line_bind(self, sequence, func):
        "Bind a sequence on line numbers to the given function"
        self._line_bindings[normalize_sequence(sequence)] = func

    def name_bind(self, sequence, func):
        "Bind a sequence on tokenized names to the given function"
        self._name_bindings[normalize_sequence(sequence)] = func

    def _on_line_handler(self, sequence):
        "Create an internal handler for events on a line number."
        def line_handler(event):
            line = int(self.code.index("@%s,%s" % (event.x, event.y)).split('.')[0])
            try:
                handler = self._line_bindings[sequence]

                # Modify the event for passing on external handlers
                event.widget = self
                event.line = line
                handler(event)
            except KeyError:
                # No handler registered
                pass
        return line_handler

    def _on_name_handler(self, sequence):
        "Create an internal handler for events on a tokenized name."
        def name_handler(event):
            range = self.code.tag_nextrange(str(Token.Name), "@%s,%s wordstart" % (event.x, event.y))
            name = self.code.get(range[0], range[1])

            try:
                handler = self._name_bindings[sequence]

                # Modify the event for passing on external handlers
                event.widget = self
                event.name = name
                handler(event)
            except KeyError:
                # No handler registered
                pass
        return name_handler
