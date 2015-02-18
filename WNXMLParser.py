#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
import xml.sax

import synset

DEBUG = False

class WNXMLParserException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class WNXMLParserErrorHandler(xml.sax.ErrorHandler):
    def warning(self, msg):
        print("SAX parser warning: {0}".format(msg), file=sys.stderr)

    def error(self, msg):
        raise WNXMLParserException("SAX parser error: {0}".format(msg))

    def fatal(self, msg):
        raise WNXMLParserException("SAX parser fatal error: {0}".format(msg))

class WNXMLParserContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.m_lcnt = 0                # input line number
        self.m_ppath = []              # contains the XML path to the current node (names of the ancestors)
        self.m_done = -1               # -1: not started synset yet, 0: inside synset, 1: done with synset
        self.m_syns = synset.Synset()  # points to the output struct
        self.m_syns_list = []          # points to the output struct

        self.m_ilrs0_temp = ""         # Temp vars for Tuples (std::pair in C++)
        self.m_ilrs1_temp = ""

        self.m_sumolinks0_temp = ""
        self.m_sumolinks1_temp = ""

        self.m_elrs0_temp = ""
        self.m_elrs1_temp = ""

        self.m_elrs30_temp = ""
        self.m_elrs31_temp = ""

        self.m_ekszlinks0_temp = ""
        self.m_ekszlinks1_temp = ""

        self.m_vframelinks0_temp = ""
        self.m_vframelinks1_temp = ""

        self.m_startroot = False      # was there a starting root tag?
        self.m_endroot = False        # was there an end root tag?


    def endDocument(self):
        if self.m_done != 1:  # reached eof before end of segment
            raise WNXMLParserException("Warning: end of file reached before </SYNSET>, possibly corrupt input")

    def startElement(self, name, attrs):
        if DEBUG:
            print("({0}, {1}): /{2}/START: {3}".format(self._locator.getLineNumber(),
                                                        self._locator.getColumnNumber(),
                                                         "/".join(self.m_ppath),
                                                         name))

        self.m_ppath.append(name)

        if len(self.m_ppath) >= 2:
            parent = self.m_ppath[-2]
        else:
            parent = ""

        if len(self.m_ppath) >= 3:
            gparent = self.m_ppath[-3]
        else:
            gparent = ""

        # VisDic XML format fault tolerance (no root tag)
        if name == "WNXML":
            self.m_startroot = True

        elif name == "SYNSET":
            if self.m_done == 0:
                raise WNXMLParserException("WNXMLParser internal error: SYNSET should start now, but m_done is not 0 ({0})!".format(self.m_done))
            self.m_done = 0
            self.m_lcnt = self._locator.getLineNumber()

        elif name == "LITERAL" and parent == "SYNONYM" and gparent == "SYNSET":
            self.m_syns.synonyms.append(synset.Synonym("", ""))

        elif name == "ILR" and parent == "SYNSET":
            self.m_ilrs0_temp = ""
            self.m_ilrs1_temp = ""

        elif name == "SUMO" and parent == "SYNSET":
            self.m_sumolinks0_temp = ""
            self.m_sumolinks1_temp = ""

        elif name == "ELR" and parent == "SYNSET":
            self.m_elrs0_temp = ""
            self.m_elrs1_temp = ""

        elif name == "ELR3" and parent == "SYNSET":
            self.m_elrs30_temp = ""
            self.m_elrs31_temp = ""

        elif name == "EKSZ" and parent == "SYNSET":
            self.m_ekszlinks0_temp = ""
            self.m_ekszlinks1_temp = ""

        elif name == "VFRAME" and parent == "SYNSET":
            self.m_vframelinks0_temp = ""
            self.m_vframelinks1_temp = ""

        elif name == "USAGE" and parent == "SYNSET":
            self.m_syns.usages.append("")

        elif name == "SNOTE" and parent == "SYNSET":
            self.m_syns.snotes.append("")

        elif name == "EQ_NEAR_SYNONYM" and parent == "SYNSET":
            self.m_syns.elrs.append(["", "eq_near_synonym"])

        elif name == "EQ_HYPERNYM" and parent == "SYNSET":
            self.m_syns.elrs.append(["", "eq_has_hypernym"])

        elif name == "EQ_HYPONYM" and parent == "SYNSET":
            self.m_syns.elrs.append(["", "eq_has_hyponym"])

        #elif name == "ELR" and parent == "SYNSET":
        #    self.m_syns.elrs.append(["", ""])

        elif name == "EKSZ" and parent == "SYNSET":
            self.m_syns.ekszlinks.append(["", ""])

        elif name == "VFRAME" and parent == "SYNSET":
            self.m_syns.vframelinks.append(["", ""])

    def characters(self, chrs):
        if DEBUG:
            print("({0}, {1}): /{2}/#PCDATA: {3}".format(self._locator.getLineNumber(),
                                                        self._locator.getColumnNumber(),
                                                         "/".join(self.m_ppath),
                                                         chrs))

        if self.m_done == 1 or self.m_done == -1:
            return

        self.m_ppath.append("#PCDATA")

        if 2 <= len(self.m_ppath):
            parent = self.m_ppath[-2]
        else:
            parent = ""

        if 3 <= len(self.m_ppath):
            gparent = self.m_ppath[-3]
        else:
            gparent = ""

        if 4 <= len(self.m_ppath):
            ggparent = self.m_ppath[-4]
        else:
            ggparent = ""

        if parent == "ID" and gparent == "SYNSET":  # SYNSET/ID
            self.m_syns.wnid += chrs

        elif parent == "ID3" and gparent == "SYNSET":  # SYNSET/ID3
            self.m_syns.wnid3 += chrs

        elif parent == "POS" and gparent == "SYNSET":  # SYNSET/POS
            self.m_syns.pos += chrs

        elif parent == "LITERAL" and gparent == "SYNONYM":  # SYNSET/SYNONYM/LITERAL
            if len(self.m_syns.synonyms) == 0:
                raise WNXMLParserException("WNXMLParser internal error: synonyms empty at LITERAL tag")
            self.m_syns.synonyms[-1].literal += chrs

        elif parent == "SENSE" and gparent == "LITERAL" and ggparent == "SYNONYM":  # SYNSET/SYNONYM/LITERAL/SENSE
            if len(self.m_syns.synonyms) == 0:
                raise WNXMLParserException("WNXMLParser internal error: synonyms empty at SENSE tag")
            self.m_syns.synonyms[-1].sense += chrs

        elif parent == "LNOTE" and gparent == "LITERAL" and ggparent == "SYNONYM":  # SYNSET/SYNONYM/LITERAL/LNOTE
            if len(self.m_syns.synonyms) == 0:
                raise WNXMLParserException("WNXMLParser internal error: synonyms empty({0}) at LNOTE tag".format(len(self.m_syns.synonyms)))
            self.m_syns.synonyms[-1].lnote += chrs

        elif parent == "NUCLEUS" and gparent == "LITERAL" and ggparent == "SYNONYM":  # SYNSET/SYNONYM/LITERAL/NUCLEUS
            if len(self.m_syns.synonyms) == 0:
                raise WNXMLParserException("WNXMLParser internal error: synonyms empty at NUCLEUS tag")
            self.m_syns.synonyms[-1].nucleus += chrs

        elif parent == "DEF" and gparent == "SYNSET":  # SYNSET/DEF
            self.m_syns.definition += chrs

        elif parent == "BCS" and gparent == "SYNSET":  # SYNSET/BCS
            self.m_syns.bcs += chrs

        elif parent == "USAGE" and gparent == "SYNSET":  # SYNSET/USAGE
            if len(self.m_syns.usages) == 0:
                raise WNXMLParserException("WNXMLParser internal error: usages empty at USAGE tag")
            self.m_syns.usages[-1] += chrs

        elif parent == "SNOTE" and gparent == "SYNSET":  # SYNSET/SNOTE
            if len(self.m_syns.snotes) == 0:
                raise WNXMLParserException("WNXMLParser internal error: snotes empty at SNOTE tag")
            self.m_syns.snotes[-1] += chrs

        elif parent == "STAMP" and gparent == "SYNSET":  # SYNSET/STAMP
            self.m_syns.stamp += chrs

        elif parent == "DOMAIN" and gparent == "SYNSET":  # SYNSET/STAMP
            self.m_syns.domain += chrs

        elif parent == "NL" and gparent == "SYNSET":  # SYNSET/NL
            self.m_syns.nl += chrs

        elif parent == "TNL" and gparent == "SYNSET":  # SYNSET/TNL
            self.m_syns.tnl += chrs

        elif parent == "ILR" and gparent == "SYNSET":  # SYNSET/ILR
            self.m_ilrs0_temp += chrs

        elif parent == "TYPE" and gparent == "ILR":  # SYNSET/ILR/TYPE
            self.m_ilrs1_temp += chrs

        elif parent == "SUMO" and gparent == "SYNSET":  # SYNSET/SUMO
            self.m_sumolinks0_temp += chrs

        elif parent == "TYPE" and gparent == "SUMO":  # SYNSET/SUMO/TYPE
            self.m_sumolinks1_temp += chrs

        elif parent == "EQ_NEAR_SYNONYM" and gparent == "SYNSET":  # SYNSET/EQ_NEAR_SYNONYM
            self.m_elrs0_temp += chrs

        elif parent == "EQ_HYPERNYM" and gparent == "SYNSET":  # SYNSET/EQ_HYPERNYM
            self.m_elrs0_temp += chrs

        elif parent == "EQ_HYPONYM" and gparent == "SYNSET":  # SYNSET/EQ_HYPONYM
            self.m_elrs0_temp += chrs

        elif parent == "ELR" and gparent == "SYNSET":  # SYNSET/ELR
            self.m_elrs0_temp += chrs

        elif parent == "TYPE" and gparent == "ELR":  # SYNSET/ELR/TYPE
            self.m_elrs1_temp += chrs

        elif parent == "ELR3" and gparent == "SYNSET":  # SYNSET/ELR3
            self.m_elrs30_temp += chrs

        elif parent == "TYPE" and gparent == "ELR3":  # SYNSET/ELR3/TYPE
            self.m_elrs31_temp += chrs

        elif parent == "EKSZ" and gparent == "SYNSET":  # SYNSET/EKSZ
            self.m_ekszlinks0_temp += chrs

        elif parent == "TYPE" and gparent == "EKSZ":  # SYNSET/EKSZ/TYPE
            self.m_ekszlinks1_temp += chrs

        elif parent == "VFRAME" and gparent == "SYNSET":  # SYNSET/VFRAME
            self.m_vframelinks0_temp += chrs

        elif parent == "TYPE" and gparent == "VFRAME":  # SYNSET/VFRAME/TYPE
            self.m_vframelinks1_temp += chrs

        self.m_ppath.pop()

    def endElement(self, name):
        if DEBUG:
            print("({0}, {1}): /{2}/END: {3}".format(self._locator.getLineNumber(),
                                                        self._locator.getColumnNumber(),
                                                         "/".join(self.m_ppath),
                                                         name))

        if len(self.m_ppath) >= 2:
            parent = self.m_ppath[-2]
        else:
            parent = ""

        if name == "WNXML":  # WNXML
            self.m_endroot = True

        elif name == "SYNSET":  # SYNSET
            if self.m_done != 0:
                raise WNXMLParserException("This is impossible!\nThe parser should've caught this error: 'SYNSET' end tag without previous begin tag")
            self.m_done = 1
            self.m_syns_list.append((self.m_syns, self.m_lcnt))
            self.m_syns = synset.Synset()

        elif name == "ILR" and parent == "SYNSET":
            self.m_syns.ilrs.append((self.m_ilrs0_temp, self.m_ilrs1_temp))
            self.m_ilrs0_temp = ""
            self.m_ilrs1_temp = ""

        elif name == "SUMO" and parent == "SYNSET":
            self.m_syns.sumolinks.append((self.m_sumolinks0_temp, self.m_sumolinks1_temp))
            self.m_sumolinks0_temp = ""
            self.m_sumolinks1_temp = ""

        elif name == "ELR" and parent == "SYNSET":
            self.m_syns.elrs.append((self.m_elrs0_temp, self.m_elrs1_temp))
            self.m_elrs0_temp = ""
            self.m_elrs0_temp = ""

        elif name == "ELR3" and parent == "SYNSET":
            self.m_syns.elrs3.append((self.m_elrs30_temp, self.m_elrs31_temp))
            self.m_elrs30_temp = ""
            self.m_elrs30_temp = ""

        elif name == "EKSZ" and parent == "SYNSET":
            self.m_syns.ekszlinks.append((self.m_ekszlinks0_temp, self.m_ekszlinks1_temp))
            self.m_ekszlinks0_temp = ""
            self.m_ekszlinks1_temp = ""

        elif name == "VFRAME" and parent == "SYNSET":
            self.m_syns.vframelinks.append((self.m_vframelinks0_temp, self.m_vframelinks1_temp))
            self.m_vframelinks0_temp = ""
            self.m_vframelinks1_temp = ""

        self.m_ppath.pop()

    # Magic lies here
    # Source: http://stackoverflow.com/a/12263340
    def parse(self, input_file):
        # Make parser
        xmlReader = xml.sax.make_parser()
        # set self as ContentHandler
        xmlReader.setContentHandler(self)
        # Set ErrorHandler
        xmlReader.setErrorHandler(WNXMLParserErrorHandler())
        # Do the actual parsing
        xmlReader.parse(input_file)
        # Return the gathered result
        return self.m_syns_list

