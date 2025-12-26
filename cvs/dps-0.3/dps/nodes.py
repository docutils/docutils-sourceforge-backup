#! /usr/bin/env python

"""
Author: David Goodger
Contact: dgoodger@bigfoot.com
Revision: $Revision: 1.1.1.1 $
Date: $Date: 2001/07/22 22:35:51 $
Copyright: This module has been placed in the public domain.

"""

import sys
import xml.dom.minidom as dom
from types import StringType
from UserString import MutableString

class _Node:

    def asdom(self):
        return self._dom_node()

    def _dom_node(self):
        pass
    
    def _rooted_dom_node(self, domroot):
        pass

    def astext(self):
        pass

    def validate(self):
        pass


class Text(_Node, MutableString):

    tagName = '#text'

    def __repr__(self):
        data = repr(self.data)
        if len(data) > 70:
            data = repr(self.data[:64] + ' ...')
        return '<%s: %s>' % (self.tagName, data)

    def _dom_node(self):
        return dom.Text(self.data)
    
    def _rooted_dom_node(self, domroot):
        return domroot.createTextNode(self.data)

    def astext(self):
        return self.data

    def pprint(self, indent='    ', level=0):
        result = []
        indent = indent * level
        for line in self.data.splitlines():
            result.append(indent + line + '\n')
        return ''.join(result)


class _Element(_Node):

    childtextsep = '\n\n'
    """Separator for child nodes, used by `astext()` method."""

    def __init__(self, rawsource='', *children, **attributes):
        self.rawsource = rawsource
        self.children = list(children)
        self.attributes = attributes
        self.tagName = self.__class__.__name__

    def _dom_node(self):
        element = dom.Element(self.tagName)
        for attribute, value in self.attributes.items():
            element.setAttribute(attribute, value)
        for child in self.children:
            element.appendChild(child._dom_node())
        return element

    def _rooted_dom_node(self, domroot):
        element = domroot.createElement(self.tagName)
        for attribute, value in self.attributes.items():
            element.setAttribute(attribute, value)
        for child in self.children:
            element.appendChild(child._rooted_dom_node(domroot))
        return element

    def __repr__(self):
        data = ''
        for c in self.children:
            data += '<%s...>' % c.tagName
            if len(data) > 60:
                data = data[:56] + ' ...'
                break
        return '<%s: %s>' % (self.__class__.__name__, data)

    def __str__(self):
        if self.children:
            return '%s%s%s' % (self.starttag(),
                                ''.join([str(c) for c in self.children]),
                                self.endtag())
        else:
            return self.emptytag()

    def starttag(self):
        return '<%s>' % ' '.join([self.tagName] +
                                 ['%s="%s"' % (n, v)
                                  for n, v in self.attlist()])

    def endtag(self):
        return '</%s>' % self.tagName

    def emptytag(self):
        return '<%s/>' % ' '.join([self.tagName] +
                                  ['%s="%s"' % (n, v)
                                   for n, v in self.attlist()])

    def __len__(self):
        return len(self.children)

    def __getitem__(self, key):
        if isinstance(key, StringType):
            return self.attributes[key]
        else:
            return self.children[key]

    def __setitem__(self, key, item):
        if isinstance(key, StringType):
            self.attributes[key] = item
        else:
            self.children[key] = item

    def __delitem__(self, key):
        if isinstance(key, StringType):
            del self.attributes[key]
        else:
            del self.children[key]

    def __add__(self, other):
        return self.children + other

    def __radd__(self, other):
        return other + self.children

    def __iadd__(self, other):
        if other is not None:
            assert isinstance(other, _Node)
            self.children.append(other)
        return self

    def astext(self):
        return self.childtextsep.join([child.astext()
                                       for child in self.children])

    def attlist(self):
        attlist = self.attributes.items()
        attlist.sort()
        return attlist

    def get(self, key, failobj=None):
        return self.attributes.get(key, failobj)

    def hasattr(self, attr):
        return self.attributes.has_key(attr)

    has_key = hasattr

    def append(self, item):
        assert isinstance(item, _Node)
        self.children.append(item)

    def extend(self, item):
        self.children.extend(item)

    def insert(self, i, item):
        assert isinstance(item, _Node)
        self.children.insert(i, item)

    def pop(self, i=-1):
        return self.children.pop(i)

    def remove(self, item):
        assert isinstance(item, _Node)
        self.children.remove(item)

    def pprint(self, indent='    ', level=0):
        if self.children:
            return ''.join(['%s%s\n' % (indent * level, self.starttag())] +
                           [c.pprint(indent, level+1) for c in self.children]
                           + ['%s%s\n' % (indent * level, self.endtag())])
        else:
            return '%s%s\n' % (indent * level, self.emptytag())


class _TextElement(_Element):

    """
    An element which directly contains text.

    Its children are all Text or _TextElement nodes.
    """

    childtextsep = ''
    """Separator for child nodes, used by `astext()` method."""

    def __init__(self, rawsource='', text='', *children, **attributes):
        if text != '':
            textnode = Text(text)
            _Element.__init__(self, rawsource, textnode, *children,
                              **attributes)
        else:
            _Element.__init__(self, rawsource, *children, **attributes)


# ==============
#  Root Element
# ==============

class document(_Element):

    def __init__(self, errorhandler, *args, **kwargs):
        _Element.__init__(self, *args, **kwargs)
        self.explicitlinks = {}
        self.implicitlinks = {}
        self.indirectlinks = {}
        self.refnames = {}
        self.errorhandler = errorhandler

    def asdom(self):
        domroot = dom.Document()
        domroot.appendChild(_Element._rooted_dom_node(self, domroot))
        return domroot

    def addimplicitlink(self, name, linknode, innode=None):
        if innode == None:
            innode = linknode
        if self.explicitlinks.has_key(name) \
              or self.indirectlinks.has_key(name) \
              or self.implicitlinks.has_key(name):
            sw = self.errorhandler.system_warning(
                  0, 'duplicate implicit link name: "%s"' % name)
            innode += sw
            self.clearlinknames(name, self.implicitlinks)
            self.implicitlinks[name].append(linknode)
        else:
            self.implicitlinks[name] = [linknode]
            linknode['name'] = name

    def addexplicitlink(self, name, linknode, innode=None):
        if innode == None:
            innode = linknode
        if self.explicitlinks.has_key(name) or self.indirectlinks.has_key(name):
            sw = self.errorhandler.system_warning(
                  1, 'duplicate explicit link name: "%s"' % name)
            innode += sw
            self.clearlinknames(name, self.explicitlinks, self.implicitlinks)
            self.explicitlinks[name].append(linknode)
            return
        elif self.implicitlinks.has_key(name):
            sw = self.errorhandler.system_warning(
                  0, 'duplicate implicit link name: "%s"' % name)
            innode += sw
            self.clearlinknames(name, self.implicitlinks)
        self.explicitlinks[name] = [linknode]
        linknode['name'] = name

    def clearlinknames(self, name, *linkdicts):
        for linkdict in linkdicts:
            for node in linkdict.get(name, []):
                if node.has_key('name'):
                    del node['name']

    def addrefname(self, name, node):
        self.refnames.setdefault(name, []).append(node)

    def addindirectlink(self, name, reference, linknode, innode):
        if self.explicitlinks.has_key(name) \
              or self.indirectlinks.has_key(name) \
              or self.implicitlinks.has_key(name):
            sw = self.errorhandler.system_warning(
                  1, 'duplicate indirect link name: "%s"' % name)
            innode += sw
        self.indirectlinks[name] = reference
        linknode['name'] = name


# ========================
#  Bibliographic Elements
# ========================

class title(_TextElement): pass
class subtitle(_TextElement): pass
class author(_TextElement): pass
class authors(_Element): pass
class organization(_TextElement): pass
class contact(_TextElement): pass
class version(_TextElement): pass
class revision(_TextElement): pass
class status(_TextElement): pass
class date(_TextElement): pass
class copyright(_TextElement): pass


# =====================
#  Structural Elements
# =====================

class abstract(_Element): pass
class section(_Element): pass

class package_section(_Element): pass
class module_section(_Element): pass
class class_section(_Element): pass
class method_section(_Element): pass
class function_section(_Element): pass
class module_attribute_section(_Element): pass
class class_attribute_section(_Element): pass
class instance_attribute_section(_Element): pass

# Structural Support Elements
# ---------------------------

class inheritance_list(_Element): pass
class parameter_list(_Element): pass
class parameter_item(_Element): pass
class optional_parameters(_Element): pass
class parameter_tuple(_Element): pass
class parameter_default(_TextElement): pass
class initial_value(_TextElement): pass


# ===============
#  Body Elements
# ===============

class paragraph(_TextElement): pass
class bullet_list(_Element): pass
class enumerated_list(_Element): pass
class list_item(_Element): pass
class definition_list(_Element): pass
class definition_list_item(_Element): pass
class term(_TextElement): pass
class definition(_Element): pass
class field_list(_Element): pass
class field(_Element): pass
class field_name(_TextElement): pass
class field_argument(_TextElement): pass
class field_body(_Element): pass
class literal_block(_TextElement): pass
class block_quote(_Element): pass
class note(_Element): pass
class tip(_Element): pass
class warning(_Element): pass
class caution(_Element): pass
class danger(_Element): pass
class important(_Element): pass
class comment(_TextElement): pass
class directive(_Element): pass
class target(_TextElement): pass
class footnote(_Element): pass
class label(_TextElement): pass
class figure(_Element): pass
class caption(_TextElement): pass
class legend(_Element): pass
class table(_Element): pass
class tgroup(_Element): pass
class colspec(_Element): pass
class thead(_Element): pass
class tbody(_Element): pass
class row(_Element): pass
class entry(_Element): pass


class system_warning(_Element):

    def __init__(self, comment=None, *children, **attributes):
        #print ('nodes.system_warning.__init__: comment=%r, children=%r, '
        #       'attributes=%r' % (comment, children, attributes))
        if comment:
            p = paragraph('', comment)
            children = (p,) + children
        _Element.__init__(self, '', *children, **attributes)

    def astext(self):
        return '[level %s] ' % self['level'] + _Element.astext(self)


class option_list(_Element): pass
class option_list_item(_Element): pass
class option(_Element): pass
class short_option(_TextElement): pass
class long_option(_TextElement): pass
class option_argument(_TextElement): pass
class description(_Element): pass
class doctest_block(_TextElement): pass


# =================
#  Inline Elements
# =================

class emphasis(_TextElement): pass
class strong(_TextElement): pass
class interpreted(_TextElement): pass
class literal(_TextElement): pass
class link(_TextElement): pass
class footnote_reference(_TextElement): pass
class graphic(_TextElement): pass

class package(_TextElement): pass
class module(_TextElement): pass


class inline_class(_TextElement):

    def __init__(self, *args, **kwargs):
        _TextElement.__init__(self, *args, **kwargs)
        self.tagName = 'class'


class method(_TextElement): pass
class function(_TextElement): pass
class variable(_TextElement): pass
class parameter(_TextElement): pass
class type(_TextElement): pass
class class_attribute(_TextElement): pass
class module_attribute(_TextElement): pass
class instance_attribute(_TextElement): pass
class exception_class(_TextElement): pass
class warning_class(_TextElement): pass
