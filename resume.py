#!/usr/bin/env python

from lxml import etree

class ResumeParser:

    class ListParser:
        def __init__(self, element):
            self.items = []
            for child in element:
                assert child.tag == 'item', \
                  'XML error at line %d: <list> elements can only contain elements of type <item>' % child.sourceline
                assert len(child) == 0, \
                  'XML error at line %d: <item> elements cannot contain other elements' % child.sourceline

                self.items.append(child.text)

    class EntryParser:
        def __init__(self, element):
            self.title = None
            self.organization = None
            self.location = None
            self.start_date = None
            self.end_date = None
            self.list = None

            assert 'title' in element.attrib.keys(), \
              'XML error at line %d: <section> element must have a "title" attribute' % element.sourceline

            self.title = element.attrib['title']

            for child in element:
                if child.tag == 'organization':
                    self.organization = child.text
                elif child.tag == 'location':
                    self.location = child.text
                elif child.tag == 'start_date' or child.tag == 'date':
                    self.start_date = child.text
                elif child.tag == 'end_date':
                    self.end_date = child.text
                elif child.tag == 'list':
                    assert self.list is None, \
                      'XML error at line %d: <entry> element can contain no more than 1 <list> element' % element.sourceline
                    self.list = ResumeParser.ListParser(child)
                else:
                    print "XML error at line %d: Unrecognized element <%s>" % (child.sourceline, child.tag)


    class SectionParser:
        def __init__(self, element):
            self.title = None
            self.entries = []
            self.list = None

            assert 'title' in element.attrib.keys(), \
              'XML error at line %d: <section> element must have a "title" attribute' % element.sourceline

            self.title = element.attrib['title']

            for child in element:
                if child.tag == 'list':
                    assert len(element) == 1, \
                      'XML error at line %d: A <section> cannot contain a <list> element and other <elements>' % child.sourceline
                    self.list = ResumeParser.ListParser(child)
                elif child.tag == 'entry':
                    self.entries.append(ResumeParser.EntryParser(child))
                else:
                    print "XML error at line %d: Unrecognized element <%s>" % (child.sourceline, child.tag)


    def __init__(self, filename=None):
        self.name = None
        self.address = None
        self.email = None
        self.phone = None
        self.sections = []

        if not filename is None:
            self.parse(filename)

    def parse(self, filename):
        root = etree.parse(filename).getroot()

        assert root.tag == 'resume', 'Root element must be of type <resume>'

        for child in root:
            if child.tag == 'name':
                self.name = child.text
            elif child.tag == 'address':
                self.address = child.text
            elif child.tag == 'email':
                self.email = child.text
            elif child.tag == 'phone':
                self.phone = child.text
            elif child.tag == 'section':
                self.sections.append(ResumeParser.SectionParser(child))
            else:
                print "XML error at line %d: Unrecognized element <%s>" % (child.sourceline, child.tag)

class ResumeTextEmitter:
    def emit(self, resume):
        if not resume.name is None:
            print resume.name
        if not resume.address is None:
            print resume.address
        if not resume.email is None:
            print resume.email
        if not resume.phone is None:
            print resume.phone

        for section in resume.sections:
            print ''
            print section.title
            print '=' * len(section.title)

            if not section.list is None:
                for item in section.list.items:
                    print '  * %s' % item
            else:
                for entry in section.entries:
                    print ''
                    print entry.title
                    print '-' * len(entry.title)

                    if not entry.organization is None:
                        print entry.organization
                    if not entry.location is None:
                        print entry.location

                    if not entry.end_date is None:
                        print '%s -- %s' % (entry.start_date, entry.end_date)
                    elif not entry.start_date is None:
                        print entry.start_date

                    if not entry.list is None:
                        for item in entry.list.items:
                            print '  * %s' % item


class ResumeMarkDownEmitter:
    pass

class ResumeHTMLEmitter:
    pass

class ResumeLatexEmitter:
    pass

if __name__ == '__main__':
    resume = ResumeParser('resume.xml')

    text = ResumeTextEmitter()
    text.emit(resume)
