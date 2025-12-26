"""
Author: David Goodger
Contact: dgoodger@bigfoot.com
Revision: $Revision: 1.1.1.1 $
Date: $Date: 2001/07/21 22:14:09 $
Copyright: This module has been placed in the public domain.


"""

import sys, re, string
from dps import nodes, statemachine, utils
from dps.statemachine import StateMachineWS, StateWS

__all__ = ['RSTStateMachine']


class MarkupError: pass


class Stuff:

    """Stores a bunch of stuff for dotted-attribute access."""

    def __init__(self, **keywordargs):
        self.__dict__.update(keywordargs)


class RSTStateMachine(StateMachineWS):

    """
    reStructuredText's customized StateMachine.
    """

    def run(self, inputlines, inputoffset=0,
            warninglevel=1, errorlevel=3,
            memo=None, node=None, matchtitles=1):
        """Extend `StateMachineWS.run()`: set up document-wide data."""
        self.warninglevel=warninglevel
        self.errorlevel = errorlevel
        self.matchtitles = matchtitles
        if memo is None:
            errorist = utils.Errorist(warninglevel, errorlevel)
            docroot = nodes.document(errorist)
            self.memo = Stuff(document=docroot,
                              errorist=errorist,
                              titlestyles=[],
                              sectionlevel=0,
                              matchfirstfields=1)
            self.node = docroot
        else:
            if self.debug:
                print >>sys.stderr, ('\nRSTStateMachine (recursive): node=%r'
                                     % node)
            self.memo = memo
            self.node = node
        if not self.memo.matchfirstfields:
            for state in self.states.values:
                if state.transitions.has_key('firstfield'):
                    state.removetransition('firstfield')
        return StateMachineWS.run(self, inputlines, inputoffset)


class RSTState(StateWS):

    """reStructuredText State superclass."""

    def __init__(self, statemachine, debug=0):
        self.indentSMkwargs = {'stateclasses': stateclasses,
                               'initialstate': 'Body'}
        StateWS.__init__(self, statemachine, debug)

    def bof(self, context):
        return [], []

    def section(self, title, source, style, lineno):
        """
        When a new section is reached that isn't a subsection of the current
        section, back up the line count (use previousline(-x)), then raise
        EOFError. The current StateMachine will finish, then the calling
        StateMachine can re-examine the title. This will work its way back up
        the calling chain until the correct section level isreached.

        Alternative: Evaluate the title, store the title info & level, and
        back up the chain until that level is reached. Store in memo? Or
        return in results?
        """
        # XXX need to catch title as first element (after comments),
        # so firstfields will work
        memo = self.statemachine.memo
        titlestyles = memo.titlestyles
        try:
            mylevel = memo.sectionlevel
            level = titlestyles.index(style) + 1
            if self.debug:
                print >>sys.stderr, ('\nstates.RSTState.section: mylevel=%s, '
                                     'new level=%s (exists)' % (mylevel, level))
            if level <= mylevel:        # sibling or supersection
                memo.sectionlevel = level
                self.statemachine.previousline(2)
                raise EOFError          # return to parent section
            if level == mylevel + 1:    # subsection
                memo.sectionlevel += 1
            else:
                sw = memo.errorist.strong_system_warning(
                      'ABORT', 'Title level inconsistent at line %s:' % lineno,
                      source)
                self.statemachine.node += sw
                return
        except ValueError:              # new title style
            if len(titlestyles) == memo.sectionlevel:
                memo.sectionlevel += 1
                titlestyles.append(style)
            else:                       # not at lowest level
                sw = memo.errorist.strong_system_warning(
                      'ABORT', 'Title level inconsistent at line %s:' % lineno,
                      source)
                self.statemachine.node += sw
                return
        if self.debug:
            print >>sys.stderr, ('\nstates.RSTState.section: starting a new '
                                 'subsection (level %s)' % (mylevel + 1))
        s = nodes.section()
        textnodes, warnings = self.inline_text(title, lineno)
        titlenode = nodes.title(title, '', *textnodes)
        s += titlenode
        s.extend(warnings)
        memo.document.addimplicitlink(normname(titlenode.astext()), s)
        sm = RSTStateMachine(stateclasses=stateclasses, initialstate='Body',
                             debug=self.debug)
        offset = self.statemachine.lineoffset + 1
        absoffset = self.statemachine.abslineoffset() + 1
        sm.run(self.statemachine.inputlines[offset:], inputoffset=absoffset,
               memo=memo, node=s, matchtitles=1)
        sm.unlink()
        self.statemachine.node += s
        if self.debug:
            print >>sys.stderr, ('\nstates.RSTState.section: back from '
                                 'subsection (mylevel=%s, new level=%s)'
                                 % (mylevel,
                                    memo.sectionlevel))
            print >>sys.stderr, ('                       sm.abslineoffset=%s'
                                 % sm.abslineoffset())
        try:
            self.statemachine.gotoline(sm.abslineoffset())
        except IndexError:
            pass
        if memo.sectionlevel <= mylevel:
            raise EOFError              # pass on to supersection
        # reset sectionlevel; next pass will detect it properly
        memo.sectionlevel = mylevel

    def paragraph(self, lines, lineno):
        """
        Return a list (paragraph & warnings) and a boolean: literal_block next?
        """
        data = '\n'.join(lines).rstrip()
        if data[-2:] == '::':
            if len(data) == 2:
                return [], 1
            elif data[-3] == ' ':
                text = data[:-3].rstrip()
            else:
                text = data[:-1]
            literalnext = 1
        else:
            text = data
            literalnext = 0
        textnodes, warnings = self.inline_text(text, lineno)
        #print >>sys.stderr, ('paragraph: data=%r, textnodes=%r, warnings=%r'
        #                         % (data, textnodes, warnings))
        p = nodes.paragraph(data, '', *textnodes)
        return [p] + warnings, literalnext

    inline = Stuff()
    """Patterns and constants used for inline markup recognition."""

    inline.openers = '\'"([{<'
    inline.closers = '\'")]}>'
    inline.start_string_prefix = r'(?:^|[ \n])[%s]*' % re.escape(inline.openers)
    inline.end_string_suffix = r'[.,:;!?%s-]*(?:[ \n]|$)' % re.escape(inline.closers)
    inline.non_whitespace_before = r'(?<![ \n])'
    inline.non_whitespace_escape_before = r'(?<![ \n\x00])'
    inline.non_whitespace_after = r'(?![ \n])'
    inline.simplename = r'[a-zA-Z0-9](?:[-_.a-zA-Z0-9]*[a-zA-Z0-9])?'
    inline.uric = r"""[-_.!~*'();/:@&=+$,%a-zA-Z0-9]"""
    inline.emailc = r"""[-_!~*'{|}/#%?^`&=+$a-zA-Z0-9]"""
    inline.identity = string.maketrans('', '')
    inline.null2backslash = string.maketrans('\x00', '\\')
    inline.patterns = Stuff(
          initial=re.compile(r"""
                             %s             # start-string prefix
                             (
                               (              # start-strings only (group 2):
                                   \*\*         # strong
                                 | \*           # emphasis
                                   (?!\*)         # but not strong
                                 | ``           # literal
                                 | `            # interpreted or phrase link
                                   (?!`)          # but not literal
                               )
                               %s             # no whitespace after
                             |              # *OR*
                               (              # whole constructs (group 3):
                                   (%s)(_)      # link name, end-string (4,5)
                                 | \[(%s)(\]_)  # footnote_reference, end (6,7)
                               )
                               %s             # end-string suffix
                             )
                             """ % (inline.start_string_prefix,
                                    inline.non_whitespace_after,
                                    inline.simplename,
                                    inline.simplename,
                                    inline.end_string_suffix),
                             re.VERBOSE),
          emphasis=re.compile(inline.non_whitespace_escape_before
                              + r'(\*)' + inline.end_string_suffix),
          strong=re.compile(inline.non_whitespace_escape_before
                            + r'(\*\*)' + inline.end_string_suffix),
          interpreted_or_phrase_link=re.compile(
                inline.non_whitespace_escape_before + '(`_?)'
                + inline.end_string_suffix),
          interpreted_role=re.compile(
                r"""
                  %s          # no whitespace/escape before
                  (:[ \n]+)   # prefix role (group 1)
                |           # *OR*
                  ([ \n]+:)   # suffix role (group 2)
                  %s          # no whitespace after
                """ % (inline.non_whitespace_escape_before,
                       inline.non_whitespace_after),
                re.VERBOSE),
          literal=re.compile(inline.non_whitespace_before + '(``)'
                             + inline.end_string_suffix),
          uri=re.compile(
                r"""
                %s                          # start-string prefix
                (
                  (                           # absolute URI (group 2)
                    [a-zA-Z][a-zA-Z0-9.+-]*     # scheme (http, ftp, mailto)
                    :
                    (?:
                      (?:                         # either:
                        //                          # hierarchical URI
                        %s+?                        # URI characters
                      |                           # OR
                        %s+(?:\.%s+)*               # opaque URI
                        @%s+(?:\.%s+)*              # (email only?)
                      )
                      (?:                         # optional query
                        \?%s*?
                      )?
                      (?:                         # optional fragment
                        \#%s*?
                      )?
                    )
                  )
                |                           # *OR*
                  (                           # email address (group 3)
                    %s+(?:\.%s+)*               # name
                    @                           # at
                    %s+?(?:\.%s+?)*             # host
                  )
                )
                %s                          # end-string suffix
                """ % ((inline.start_string_prefix, inline.uric)
                       + (inline.emailc,) * 4
                       + (inline.uric, inline.uric)
                       + (inline.emailc,) * 4
                       + (inline.end_string_suffix,)),
                re.VERBOSE))
    inline.groups = Stuff(initial=Stuff(start=2, whole=3, linkname=4, linkend=5,
                                        footnotelabel=6, fnend=7),
                          interpreted_role=Stuff(prefix=1, suffix=2),
                          uri=Stuff(whole=1, absolute=2, email=3))
    #print >>sys.stderr, '`RSTState.inline.patterns.uri.pattern`=\n%r' % inline.patterns.uri.pattern
    #print >>sys.stderr, 'RSTState.inline.patterns.uri.pattern=\n%s' % inline.patterns.uri.pattern

    def quotedstart(self, match):
        """Return 1 if inline markup start-string is 'quoted', 0 if not."""
        string = match.string
        start = match.start(self.inline.groups.initial.start)
        end = match.end(self.inline.groups.initial.start)
        if start == 0:                  # start-string at beginning of text
            return 0
        prestart = string[start - 1]
        try:
            poststart = string[end]
            if self.inline.openers.index(prestart) \
                  == self.inline.closers.index(poststart):   # quoted
                return 1
        except IndexError:              # start-string at end of text
            return 1
        except ValueError:              # not quoted
            pass
        return 0

    def inlineobj(self, match, lineno, pattern, nodeclass,
                  restorebackslashes=0):
        string = match.string
        matchstart = match.start(self.inline.groups.initial.start)
        matchend = match.end(self.inline.groups.initial.start)
        if self.quotedstart(match):
            return (string[:matchend], [], string[matchend:], [])
        else:
            endmatch = pattern.search(string[matchend:])
            if endmatch and endmatch.start(1):  # 1 or more chars
                text = unescape(endmatch.string[:endmatch.start(1)],
                                restorebackslashes)
                rawsource = unescape(
                      string[matchstart:matchend+endmatch.end(1)], 1)
                inlineobj = nodeclass(rawsource, text)
                return (string[:matchstart], [inlineobj],
                        string[matchend:][endmatch.end(1):], [])
            else:
                sw = self.statemachine.memo.errorist.system_warning(
                      1, 'Inline %s start-string without end-string '
                      'at line %s.' % (nodeclass.__name__, lineno))
                return (string[:matchend], [], string[matchend:], [sw])

    def emphasis(self, match, lineno, pattern=inline.patterns.emphasis):
        return self.inlineobj(match, lineno, pattern, nodes.emphasis)

    def strong(self, match, lineno, pattern=inline.patterns.strong):
        return self.inlineobj(match, lineno, pattern, nodes.strong)

    def interpreted_or_phrase_link(
          self, match, lineno,
          pattern=inline.patterns.interpreted_or_phrase_link):
        string = match.string
        matchstart = match.start(self.inline.groups.initial.start)
        matchend = match.end(self.inline.groups.initial.start)
        if self.quotedstart(match):
            return (string[:matchend], [], string[matchend:], [])
        else:
            endmatch = pattern.search(string[matchend:])
            if endmatch and endmatch.start(1):  # 1 or more chars
                escaped = endmatch.string[:endmatch.start(1)]
                text = unescape(escaped, 0)
                rawsource = unescape(
                      string[matchstart:matchend+endmatch.end(1)], 1)
                if rawsource[-1] == '_':
                    refname = normname(text)
                    inlineobj = nodes.link(rawsource, text,
                                           refname=normname(text))
                    self.statemachine.memo.document.addrefname(refname,
                                                               inlineobj)
                    sw = []
                else:
                    inlineobj, sw = self.interpreted(lineno, escaped,
                                                     rawsource, text)
                return (string[:matchstart], [inlineobj],
                        string[matchend:][endmatch.end(1):], sw)
            else:
                sw = self.statemachine.memo.errorist.system_warning(
                      1, 'Inline %s start-string without end-string '
                      'at line %s.' % (nodeclass.__name__, lineno))
                return (string[:matchend], [], string[matchend:], [sw])

    def interpreted(self, lineno, escaped, rawsource, text,
                    pattern=inline.patterns.interpreted_role,
                    prefix=inline.groups.interpreted_role.prefix,
                    suffix=inline.groups.interpreted_role.suffix):
        #print >>sys.stderr, 'RSTState.interpreted: rawsource=%r, text=%r' % (rawsource, text)
        sw = []
        match = pattern.search(escaped)
        if not match:
            return nodes.interpreted(rawsource, text), sw
        #print >>sys.stdout, 'RSTState.interpreted: match.groups=%r' % (match.groups(),)
        if match.group(prefix):
            #print >>sys.stderr, 'RSTState.interpreted: prefix matched! match.group(prefix)=%r' % (match.group(prefix),)
            role = normname(unescape(escaped[:match.start(prefix)]))
            aftercolon = escaped[match.end(prefix):]
            text = unescape(aftercolon)
        else:
            #print >>sys.stderr, 'RSTState.interpreted: suffix matched!'
            aftercolon = escaped[match.end(suffix):]
            role = normname(unescape(aftercolon))
            text = unescape(escaped[:match.start(suffix)])
        #print >>sys.stderr, 'RSTState.interpreted: aftercolon=%r' % aftercolon
        if pattern.search(aftercolon):
            sw.append(self.statemachine.memo.errorist.system_warning(
                  1, 'Multiple role-separators in interpreted text '
                  'at line %s.' % lineno))
        return nodes.interpreted(rawsource, text, role=role), sw

    def literal(self, match, lineno, pattern=inline.patterns.literal):
        return self.inlineobj(match, lineno, pattern, nodes.literal,
                              restorebackslashes=1)

    def footnote_reference(self, match, lineno, pattern=None):
        fnname = '[%s]' % match.group(self.inline.groups.initial.footnotelabel)
        refname = normname(fnname)
        fnrefnode = nodes.footnote_reference(fnname + '_', fnname,
                                             refname=refname)
        self.statemachine.memo.document.addrefname(refname, fnrefnode)
        string = match.string
        matchstart = match.start(self.inline.groups.initial.whole)
        matchend = match.end(self.inline.groups.initial.whole)
        return (string[:matchstart], [fnrefnode], string[matchend:], [])

    def link(self, match, lineno, pattern=None):
        linkname = match.group(self.inline.groups.initial.linkname)
        refname = normname(linkname)
        linknode = nodes.link(linkname + '_', linkname, refname=refname)
        self.statemachine.memo.document.addrefname(refname, linknode)
        string = match.string
        matchstart = match.start(self.inline.groups.initial.whole)
        matchend = match.end(self.inline.groups.initial.whole)
        return (string[:matchstart], [linknode], string[matchend:], [])

    def standalone_uri(self, text, lineno, pattern=inline.patterns.uri,
                       whole=inline.groups.uri.whole,
                       email=inline.groups.uri.email):
        remainder = text
        textnodes = []
        while 1:
            #print >>sys.stderr, 'RSTState.standalone_uri: remainder=%r' % remainder
            match = pattern.search(remainder)
            if match:
                #print >>sys.stderr, 'RSTState.standalone_uri: match.groups=%r, match.span(1)=%r' % (match.groups(), match.span(1))
                if match.start(whole) > 0:
                    textnodes.append(nodes.Text(unescape(
                          remainder[:match.start(whole)])))
                if match.group(email):
                    scheme = 'mailto:'
                else:
                    scheme = ''
                text = match.group(whole)
                unescaped = unescape(text, 0)
                textnodes.append(nodes.link(unescape(text, 1),
                                            unescaped,
                                            refuri=scheme + unescaped))
                remainder = remainder[match.end(whole):]
            else:
                if remainder:
                    textnodes.append(nodes.Text(unescape(remainder)))
                break
        return textnodes

    inline.dispatch = {'*': emphasis,
                       '**': strong,
                       '`': interpreted_or_phrase_link,
                       '``': literal,
                       ']_': footnote_reference,
                       '_': link}

    def inline_text(self, text, lineno):
        """
        Return 2 lists: nodes (text and inline elements), and system_warnings.

        A pattern matching start-strings (for emphasis, strong, interpreted,
        phrase link, and literal) or complete constructs (simple link,
        footnote reference) is stored in `self.inline.patterns.initial`. First
        we search for a candidate. When one is found, we check for validity
        (e.g., not a quoted '*' character). If valid, search for the
        corresponding end string if applicable, and check for validity. If not
        found or invalid, raise a warning and ignore the start-string.
        Standalone hyperlinks are found last. Other than that, there is no
        "precedence order" to inline markup, just left-to-right.
        """
        pattern = self.inline.patterns.initial
        dispatch = self.inline.dispatch
        start = self.inline.groups.initial.start - 1
        linkend = self.inline.groups.initial.linkend - 1
        fnend = self.inline.groups.initial.fnend - 1
        remaining = escape2null(text)
        processed = []
        unprocessed = []
        warnings = []
        while remaining:
            match = pattern.search(remaining)
            if match:
                groups = match.groups()
                before, inlines, remaining, syswarnings = \
                      dispatch[groups[start] or groups[linkend]
                               or groups[fnend]](self, match, lineno)
                unprocessed.append(before)
                warnings += syswarnings
                if inlines:
                    processed += self.standalone_uri(''.join(unprocessed),
                                                     lineno)
                    processed += inlines
                    unprocessed = []
            else:
                break
        remaining = ''.join(unprocessed) + remaining
        if remaining:
            processed += self.standalone_uri(remaining, lineno)
        return processed, warnings

    def unindentwarning(self):
        return self.statemachine.memo.errorist.system_warning(
              1, ('Unindent without blank line at line %s.'
                  % (self.statemachine.abslineno() + 1)))        


class Body(RSTState):

    """Identifier of first line of a body element or section title."""

    pats = {'arabic': '[0-9]+',
            'loweralpha': '[a-z]',
            'upperalpha': '[A-Z]',
            'lowerroman': '[ivxlcdm]+',
            'upperroman': '[IVXLCDM]+',
            'nonAlphaNum7Bit': '[!-/:-@[-`{-~]'}
    pats['enum'] = ('(%(arabic)s|%(loweralpha)s|%(upperalpha)s|%(lowerroman)s'
                    '|%(upperroman)s)' % pats)
    pats['parens'] = r'(?P<parens>\(%(enum)s\))' % pats
    pats['rightparen'] = r'(?P<rightparen>%(enum)s\))' % pats
    pats['period'] = r'(?P<period>%(enum)s\.)' % pats

    patterns = {'bullet': r'[-+*] +',
                'enum': r'(%(parens)s|%(rightparen)s|%(period)s) +' % pats,
                'option': r'(-\w|--\w[\w-]*).*?  ',
                'doctest': r'>>> ',
                'table': r'\+-[-+]+-\+ *$',
                'explicit_markup': r'\.\.( +|$)',
                'overline': r'(%(nonAlphaNum7Bit)s)\1\1+ *$' % pats,
                'firstfield': r'[!-9;-~]+:( +|$)',
                'text': r''}
    initialtransitions = ['bullet',
                          'enum',
                          'option',
                          'doctest',
                          'table',
                          'explicit_markup',
                          'overline',
                          #('firstfield', 'Field'),
                          ('text', 'Text')]

    def indent(self, match, context, nextstate):
        """Block quote."""
        indented, indent, lineoffset, blankfinish = \
              self.statemachine.getindented()
        if self.debug:
            print >>sys.stderr, ('\nstates.Body.indent (block_quote): '
                                 'indented=%r' % indented)
        bq = nodes.block_quote()
        sm = self.indentSM(debug=self.debug, **self.indentSMkwargs)
        sm.run(indented, inputoffset=lineoffset,
               memo=self.statemachine.memo, node=bq, matchtitles=0)
        sm.unlink()
        self.statemachine.node += bq
        if not blankfinish:
            self.statemachine.node += self.unindentwarning()
        return context, nextstate, []

    def bullet(self, match, context, nextstate):
        """Bullet list item."""
        l = nodes.bullet_list()
        l['bullet'] = match.string[0]
        i, blankfinish = self.list_item(match.end())
        l += i
        self.statemachine.node += l
        offset = self.statemachine.lineoffset + 1   # next line
        kwargs = self.indentSMkwargs.copy()
        kwargs['initialstate'] = 'BulletList'
        sm = self.indentSM(debug=self.debug, **kwargs)
        sm.states['BulletList'].blankfinish = blankfinish
        sm.run(self.statemachine.inputlines[offset:],
               inputoffset=self.statemachine.abslineoffset() + 1,
               memo=self.statemachine.memo, node=l, matchtitles=0)
        if not sm.states['BulletList'].blankfinish:
            self.statemachine.node += self.unindentwarning()
        sm.unlink()
        try:
            self.statemachine.gotoline(sm.abslineoffset())
        except IndexError:
            pass
        return [], nextstate, []

    def enum(self, match, context, nextstate):
        """Potential Enumerated List Item"""
        return context, nextstate, []

    def option(self, match, context, nextstate):
        return context, nextstate, []

    def doctest(self, match, context, nextstate):
        data = '\n'.join(self.statemachine.gettextblock())
        self.statemachine.node += nodes.doctest_block(data, data)
        return [], nextstate, []

    def table(self, match, context, nextstate):
        return context, nextstate, []

    explicit = Stuff()
    """Patterns and constants used for explicit markup recognition."""
    
    explicit.patterns = Stuff(
          target=re.compile(r"""
                            (`?)        # optional open quote
                            (?!=[ ])    # first char. not space
                            (           # hyperlink name
                              .+?
                            )
                            %s          # not whitespace or escape
                            \1          # close quote if open quote used
                            :           # end of hyperlink name
                            (?:[ ]+|$)    # followed by whitespace
                            """ % RSTState.inline.non_whitespace_escape_before,
                            re.VERBOSE),)
    explicit.groups = Stuff(
          target=Stuff(quote=1, name=2))

    def footnote(self, match):
        indented, indent, offset, blankfinish = \
              self.statemachine.getfirstknownindented(match.end())
        label = match.group(1)
        name = normname('[' + label + ']')
        f = nodes.footnote('\n'.join(indented))
        f += nodes.label('', label)
        self.statemachine.memo.document.addexplicitlink(name, f)
        if indented:
            #rint >>sys.stdout, 'Body.footnote: indented=%r' % indented
            sm = self.indentSM(debug=self.debug, **self.indentSMkwargs)
            sm.run(indented, inputoffset=offset,
                   memo=self.statemachine.memo, node=f, matchtitles=0)
            sm.unlink()
        return [f], blankfinish

    def hyperlink_target(self, match,
                         pattern=explicit.patterns.target,
                         namegroup=explicit.groups.target.name):
        escaped = escape2null(match.string)
        targetmatch = pattern.match(escaped[match.end():])
        if not targetmatch:
            raise MarkupError('not a hyperlink target')
        name = normname(unescape(targetmatch.group(namegroup)))
        block = self.statemachine.gettextblock()
        block[0] = unescape(targetmatch.string[targetmatch.end():], 1)
        blankfinish = 1
        for i in range(1,len(block)):
            if block[i][:1] != ' ':
                blankfinish = 0
                self.statemachine.previousline(len(block) - i)
                del block[i:]
                break
        reference = ''.join([line.strip() for line in block])
        t = nodes.target('\n'.join([match.string] + block[1:]), reference)
        if reference:
            self.statemachine.memo.document.addindirectlink(
                  name, reference, t, self.statemachine.node)
        else:
            self.statemachine.memo.document.addexplicitlink(
                  name, t, self.statemachine.node)
        return [t], blankfinish

    def directive(self, match):
        # XXX need to actually *do* something with the directive
        type = match.group(1).lower()
        atts = {'type': type}
        data = match.string[match.end():].strip()
        if data:
            atts['data'] = data
        try:
            self.statemachine.nextline()
            indented, indent, offset, blankfinish = \
                  self.statemachine.getindented()
            text = '\n'.join(indented)
        except IndexError:
            text = ''
            blankfinish = 1
        children = []
        if text:
            children.append(nodes.literal_block(text, text))
        return [nodes.directive(text, *children, **atts)], blankfinish

    def comment(self, match):
        indented, indent, offset, blankfinish = \
              self.statemachine.getfirstknownindented(match.end())
        text = '\n'.join(indented)
        return [nodes.comment(text, text)], blankfinish

    explicit.constructs = [(re.compile(r'\.\. +_\[(%s)\](?: +|$)'
                                       % RSTState.inline.simplename), footnote),
                           (re.compile(r'\.\. +_'), hyperlink_target),
                           (re.compile(r'\.\. +([\w-]+)::(?: +|$)'), directive)]

    def explicit_markup(self, match, context, nextstate):
        """Footnotes, hyperlink targets, directives, comments."""
        nodelist, blankfinish = self.explicit_construct(match)
        self.statemachine.node.extend(nodelist)
        offset = self.statemachine.lineoffset + 1   # next line
        kwargs = self.indentSMkwargs.copy()
        kwargs['initialstate'] = 'Explicit'
        sm = self.indentSM(debug=self.debug, **kwargs)
        sm.states['Explicit'].blankfinish = blankfinish
        sm.run(self.statemachine.inputlines[offset:],
               inputoffset=self.statemachine.abslineoffset() + 1,
               memo=self.statemachine.memo, node=self.statemachine.node,
               matchtitles=0)
        if not sm.states['Explicit'].blankfinish:
            self.statemachine.node += self.unindentwarning()
        sm.unlink()
        try:
            self.statemachine.gotoline(sm.abslineoffset())
        except IndexError:
            pass
        return [], nextstate, []

    def explicit_construct(self, match,
                           constructs=explicit.constructs):
        """Determine which explicit construct this is, parse & return it."""
        for pattern, method in constructs:
            expmatch = pattern.match(match.string)
            if expmatch:
                try:
                    return method(self, expmatch)
                except MarkupError:
                    break
        return self.comment(match)

    def overline(self, match, context, nextstate):
        """Section title."""
        makesection = 1
        lineno = self.statemachine.abslineno()
        if not self.statemachine.matchtitles:
            sw = self.statemachine.memo.errorist.system_warning(
                  3, 'Unexpected section title at line %s.' % lineno)
            self.statemachine.node += sw
            return [], nextstate, []
        try:
            title = underline = ''
            title = self.statemachine.nextline()
            underline = self.statemachine.nextline()
        except IndexError:
            sw = self.statemachine.memo.errorist.system_warning(
                  3, 'Incomplete section title at line %s.' % lineno)
            self.statemachine.node += sw
            makesection = 0
        source = match.string + title + underline
        overline = match.string.rstrip()
        underline = underline.rstrip()
        if not self.transitions['overline'][0].match(underline):
            sw = self.statemachine.memo.errorist.system_warning(
                  3, 'Missing underline for overline at line %s.' % lineno)
            self.statemachine.node += sw
            makesection = 0
        elif overline != underline:
            sw = self.statemachine.memo.errorist.system_warning(
                  3, 'Title overline & underline mismatch at ' 'line %s.'
                  % lineno)
            self.statemachine.node += sw
            makesection = 0
        title = title.strip()
        if len(title) > len(overline):
            self.statemachine.node += \
                  self.statemachine.memo.errorist.system_warning(
                  0, 'Title overline too short at line %s.'% lineno)
        if makesection:
            style = (overline[0], underline[0])
            self.section(title, source, style, lineno + 1)
        return [], nextstate, []

    def firstfield(self, match, context, nextstate):
        return context, nextstate, []

    def text(self, match, context, nextstate):
        """Titles, definition lists, paragraphs."""
        return [match.string], nextstate, []

    def list_item(self, indent):
        indented, lineoffset, blankfinish = \
              self.statemachine.getknownindented(indent)
        if self.debug:
            print >>sys.stderr, ('\nstates.Body.list_item: indented=%r'
                                 % indented)
        i = nodes.list_item('\n'.join(indented))
        if indented:
            sm = self.indentSM(debug=self.debug, **self.indentSMkwargs)
            sm.run(indented, inputoffset=lineoffset,
                   memo=self.statemachine.memo, node=i, matchtitles=0)
            sm.unlink()
        return i, blankfinish


class BulletList(Body):

    """Second and subsequent bullet_list list_items."""

    def bullet(self, match, context, nextstate):
        """Bullet list item."""
        if match.string[0] != self.statemachine.node['bullet']:
            # different bullet: new list
            self.not_list_item()
        i, blankfinish = self.list_item(match.end())
        self.statemachine.node += i
        self.blankfinish = blankfinish
        return [], 'BulletList', []

    def not_list_item(self, match=None, context=None, nextstate=None):
        """Not a list item."""
        self.statemachine.previousline()
        raise EOFError

    indent = enum = option = doctest = table = explicit_markup = overline \
             = text = not_list_item


class DefinitionList(Body):

    """Second and subsequent definition_list_items."""

    def text(self, match, context, nextstate):
        """Definition lists."""
        return [match.string], 'Definition', []

    def not_definition_list_item(self, match, context, nextstate):
        """Not a definition list item."""
        self.statemachine.previousline()
        raise EOFError

    indent = bullet = enum = option = doctest = table = explicit_markup \
             = overline = not_definition_list_item


class Explicit(Body):

    """Second and subsequent explicit markup construct."""

    def explicit_markup(self, match, context, nextstate):
        """Footnotes, hyperlink targets, directives, comments."""
        nodelist, blankfinish = self.explicit_construct(match)
        self.statemachine.node.extend(nodelist)
        self.blankfinish = blankfinish
        return [], nextstate, []

    def not_explicit(self, match, context, nextstate):
        """Not an explicit construct."""
        self.statemachine.previousline()
        raise EOFError

    indent = bullet = enum = option = doctest = table = text = \
             not_explicit


class Text(RSTState):

    """
    Second line of a text block.

    Could be a paragraph, a definition list item, or a title.
    """

    patterns = {'underline': r'([!-/:-@[-`{-~])\1\1+ *$',
                'text': r''}
    initialtransitions = [('underline', 'Body'), ('text', 'Body')]

    def blank(self, match, context, nextstate):
        """End of paragraph."""
        p, literalnext = self.paragraph(context,
                                        self.statemachine.abslineno() - 1)
        self.statemachine.node.extend(p)
        if literalnext:
            self.statemachine.node.extend(self.literal_block())
        return [], 'Body', []

    def eof(self, context):
        if context:
            p, literalnext = self.paragraph(context,
                                            self.statemachine.abslineno() - 1)
            if self.debug:
                print >>sys.stderr, ('\nstates.Text.eof: context=%r, p=%r, '
                                     'node=%r' % (context, p,
                                                  self.statemachine.node))
            self.statemachine.node.extend(p)
            if literalnext:
                self.statemachine.node.extend(self.literal_block())
        return []

    def indent(self, match, context, nextstate):
        """Definition list item."""
        l = nodes.definition_list()
        i = self.definition_list_item(context)
        l += i
        self.statemachine.node += l
        offset = self.statemachine.lineoffset + 1   # next line
        kwargs = self.indentSMkwargs.copy()
        kwargs['initialstate'] = 'DefinitionList'
        sm = self.indentSM(debug=self.debug, **kwargs)
        sm.run(self.statemachine.inputlines[offset:],
               inputoffset=self.statemachine.abslineoffset() + 1,
               memo=self.statemachine.memo, node=l, matchtitles=0)
        sm.unlink()
        try:
            self.statemachine.gotoline(sm.abslineoffset())
        except IndexError:
            pass
        return [], 'Body', []

    def underline(self, match, context, nextstate):
        """Section title."""
        lineno = self.statemachine.abslineno()
        if not self.statemachine.matchtitles:
            sw = self.statemachine.memo.errorist.system_warning(
                  3, 'Unexpected section title at line %s.' % lineno)
            self.statemachine.node += sw
            return [], nextstate, []
        title = context[0].rstrip()
        underline = match.string.rstrip()
        source = title + '\n' + underline
        if self.debug:
            print >>sys.stderr, ('\nstates.Text.underline: context=%r, '
                                 'match.string=%r, title=%r, titlestyles=%r'
                                 % (context, match.string, title,
                                    self.statemachine.memo.titlestyles))
        if len(title) > len(underline):
            self.statemachine.node += \
                  self.statemachine.memo.errorist.system_warning(
                  0, 'Title underline too short at line %s.' % lineno)
        style = underline[0]
        context[:] = []
        self.section(title, source, style, lineno - 1)
        return [], nextstate, []

    def text(self, match, context, nextstate):
        """Paragraph."""
        startline = self.statemachine.abslineno() - 1
        sw = None
        try:
            block = self.statemachine.getunindented()
        except statemachine.UnexpectedIndentationError, instance:
            block, lineno = instance.args
            sw = self.statemachine.memo.errorist.system_warning(
                  2, 'Unexpected indentation at line %s.' % lineno)
        lines = context + block
        if self.debug:
            print >>sys.stderr, 'states.Text.text: lines=%r' % lines
        p, literalnext = self.paragraph(lines, startline)
        if self.debug:
            print >>sys.stderr, 'states.Text.text: p=%r' % p
        self.statemachine.node.extend(p)
        self.statemachine.node += sw
        if literalnext:
            self.statemachine.node.extend(self.literal_block())
        return [], nextstate, []

    def literal_block(self):
        """Return a list of nodes."""
        indented, indent, offset, blankfinish = self.statemachine.getindented()
        nodelist = []
        if indented:
            data = '\n'.join(indented)
            nodelist.append(nodes.literal_block(data, data))
        else:
            nodelist.append(self.statemachine.memo.errorist.system_warning(
                  1, 'Literal block expected at line %s; none found.'
                  % self.statemachine.abslineno()))
        if not blankfinish:
            nodelist.append(self.unindentwarning())
        return nodelist

    def definition_list_item(self, termline):
        indented, indent, lineoffset, blankfinish = \
              self.statemachine.getindented()
        if self.debug:
            print >>sys.stderr, ('\nstates.Text.indent (definition): indented=%r'
                                 % indented)
        t, warnings = self.term(termline, self.statemachine.abslineno() - 1)
        d = nodes.definition('', *warnings)
        if termline[0][-2:] == '::':
            d += self.statemachine.memo.errorist.system_warning(
                  2, 'Blank line missing before literal block? '
                  'Interpreted as a definition list item. '
                  'At line %s.' % (lineoffset + 1))
        sm = self.indentSM(debug=self.debug, **self.indentSMkwargs)
        sm.run(indented, inputoffset=lineoffset,
               memo=self.statemachine.memo, node=d, matchtitles=0)
        sm.unlink()
        if not blankfinish:
            d += self.unindentwarning()
        i = nodes.definition_list_item('\n'.join(termline + indented), t, d)
        return i

    def term(self, lines, lineno):
        """Return a definition_list's term object."""
        assert len(lines) == 1
        textnodes, warnings = self.inline_text(lines[0], lineno)
        t = nodes.term(lines[0], '', *textnodes)
        return t, warnings


class Definition(Text):

    """Second line of potential definition_list_item."""

    initialtransitions = ['underline', 'text']

    def not_definition(self, match, context, nextstate):
        """Not a definition."""
        raise EOFError

    blank = underline = text = not_definition

    def eof(self, context):
        """Not a definition."""
        self.statemachine.previousline(2)
        return []

    def indent(self, match, context, nextstate):
        """Definition list item."""
        i = self.definition_list_item(context)
        self.statemachine.node += i
        return [], 'DefinitionList', []


stateclasses = [Body, Text, BulletList, DefinitionList, Definition,
                Explicit]
"""Standard set of State classes used to start `RSTStateMachine`."""


def escape2null(text):
    """Return a string with escape-backslashes converted to nulls."""
    parts = []
    start = 0
    while 1:
        found = text.find('\\', start)
        if found == -1:
            parts.append(text[start:])
            return ''.join(parts)
        parts.append(text[start:found])
        parts.append('\x00' + text[found+1:found+2])
        start = found + 2               # skip character after escape

def unescape(text, restorebackslashes=0):
    """Return a string with nulls removed or restored to backslashes."""
    if restorebackslashes:
        return text.translate(RSTState.inline.null2backslash)
    else:
        return text.translate(RSTState.inline.identity, '\x00')

def normname(name):
    """Return a case- and whitespace-normalized name."""
    return ' '.join(name.lower().split())
