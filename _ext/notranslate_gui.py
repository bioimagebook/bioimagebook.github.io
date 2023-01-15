"""
Minimal extension that adds 'notranslate' class to guilabel and menuselection tags.

The point of this is to tell Google Translate (and possibly other translators) not 
to translate button and menu text.

This should make automatic translations more usable, since they don't impact 
user interface elements in the software.

Important! This implementation is very simple, and overrides the 'default' guilabel 
and menuselection handling.
In particular, it doesn't bother with supporting accelerators (flagged by &).
"""

from docutils import nodes

_BULLET_CHARACTER = '\N{TRIANGULAR BULLET}'

def guilabel_notranslate(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = nodes.inline(rawtext=rawtext, text=text, classes=[name, 'notranslate'])
    return [node], []


def menuselection_notranslate(name, rawtext, text, lineno, inliner, options={}, content=[]):
    text = text.replace('-->', _BULLET_CHARACTER)
    node = nodes.inline(rawtext=rawtext, text=text, classes=[name, 'notranslate'])
    return [node], []


def span_notranslate(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = nodes.inline(rawtext=rawtext, text=text, classes=['notranslate'])
    return [node], []


def setup(app):
    app.add_role("guilabel", guilabel_notranslate, override=True)
    app.add_role("menuselection", menuselection_notranslate, override=True)
    app.add_role("notranslate", span_notranslate)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }