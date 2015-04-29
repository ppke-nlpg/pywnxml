#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
import os
try:
    import readline
except:
    pass # Readline module not loaded, seems you're not using Linux. Be sure to fix that.

import WNQuery
import SemFeatures

def process_query(wn, sf, query, out):
    t = query.split(" ")
    if t[0] == ".h":    # .h
        buf = []
        buf.append("Available commands:")
        buf.append(".h                                                this help")
        buf.append(".q                                                quit")
        buf.append(".i   <id> <pos>                                   look up synset id in given POS (n,v,a,b)")
        buf.append(".l   <literal>                                    look up all synsets containing literal in all POS")
        buf.append(".l   <literal> <pos>                              look up all synsets containing literal in given POS")
        buf.append(".l   <literal> <sensenum> <pos>                   look up synset containing literal with given sense number in given POS")
        buf.append(".rl  <literal> <pos>                              list known relations of all senses of literal in POS")
        buf.append(".rl  <literal> <pos> <relation>                   look up relation (hypernym, hyponym) of all senses of literal with id and POS, list target ids")
        buf.append(".ri  <id> <pos> <relation>                        look up relation of synset with id and POS, list target ids")
        buf.append(".ti  <id> <pos> <relation>                        trace relations of synset with id and POS")
        buf.append(".tl  <literal> <pos> <relation>                   trace relations of all senses of literal in POS")
        buf.append(".ci  <id> <pos> <relation> <id1> [<id2>...]       check if any of id1,id2,... is reachable from id by following relation")
        buf.append(".cl  <literal> <pos> <relation> <id1> [<id2>...]  check if any of id1,id2,... is reachable from any sense of literal by following relation")
        buf.append(".cli <literal> <pos> <id> [hyponyms]              check if synset contains literal, or if \"hyponyms\" is added, any of its hyponyms")
        buf.append(".slc <literal1> <literal2> <pos> <relation> [top] calculate Leacock-Chodorow similarity for all senses of literals in pos using relation")
        buf.append("                                                  if 'top' is added, an artificial root node is added to relation paths, making WN interconnected.")
        buf.append(".md  <id> <pos> <relation>                        calculate the longest possible path to synset with id and POS from the root level using relation")
        buf.append(".sg  <id> <pos> <relation>                        calculate the number of nodes in the graph starting from synset id doing a recursive trace using relation")
        if sf:
            buf.append(".s  <feature>                                     look up semantic feature")
            buf.append(".sc <literal> <pos> <feature>                    check whether any sense of literal is compatible with semantic feature")
        print("\n".join(buf), end="\n\n", file=out)
        return

    if t[0] == ".i":    # .i
        if len(t) != 3:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return
        syns = wn.lookUpID(t[1], t[2])
        if not syns:
            print("Synset not found\n", file=out)
        else:
            write_synset(syns, out)
            print("", file=out)
        return

    if t[0] == ".l":    # .l
        if len(t) < 2 or len(t) > 4:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        if len(t) == 2:  # .l <literal>
            # For n, v, a, b elements we run the lookUpLiteral function,
            # then we flatten the resulting list of returned lists
            res = [item for i in ["n", "v", "a", "b"]
                         for item in wn.lookUpLiteral(t[1], i)]

            if not res:
                print("Literal not found\n", file=out)
            else:
                for i in res:
                    write_synset(i, out)
                print("", file=out)

        if len(t) == 3:  # .l <literal> <pos>
            res = wn.lookUpLiteral(t[1], t[2])
            if not res:
                print("Literal not found\n", file=out)
            else:
                for i in res:
                    write_synset(i, out)
                print("", file=out)

        if len(t) == 4:  # .l <literal> <sensenum> <pos>
            syns = wn.lookUpSense(t[1], int(t[2]), t[3])
            if not syns:
                print("Word sense not found\n", file=out)
            else:
                write_synset(syns, out)
                print("", file=out)
        return

    if t[0] == ".rl":   # .rl
        if len(t) != 3 and len(t) != 4:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        if len(t) == 3:  # .rl <literal> <pos>
            ss = wn.lookUpLiteral(t[1], t[2])
            if not ss:
                print("Literal not found", file=out)
            else:
                for j in ss:
                    write_synset(j, out)
                    rs = set()
                    for _, rel in j.ilrs:
                        if rel not in rs:
                            print("  {0}".format(rel))
                            rs.add(rel)
                    print("", file=out)

        if len(t) == 4:  # .rl <literal> <pos> <relation>
            ss = wn.lookUpLiteral(t[1], t[2])
            if not ss:
                print("Literal not found", file=out)
            else:
                for j in ss:
                    write_synset_id(wn, j.wnid, t[2], out)
                    ids = wn.lookUpRelation(j.wnid, t[2], t[3])
                    if ids:
                        for i in ids:
                            print("  ", end="", file=out)
                            write_synset_id(wn, i, t[2], out)
                    print("", file=out)
        return

    if t[0] == ".ri":   # .ri
        if len(t) != 4:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        ids = wn.lookUpRelation(t[1], t[2], t[3])
        if not ids:
            print("Synset not found or has no relations of the specified type", file=out)
        else:
            for i in ids:
                write_synset_id(wn, i, t[2], out)
        return

    if t[0] == ".ti":   # .ti
        if len(t) != 4:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        oss = wn.traceRelationOS(t[1], t[2], t[3])
        if not oss:
            print("Synset not found\n", file=out)
        else:
            print("\n".join(oss), end="\n\n", file=out)
        return

    if t[0] == ".tl":   # .tl
        if len(t) != 4:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        senses = wn.lookUpLiteral(t[1], t[2])
        if not senses:
            print("Literal not found\n", file=out)
        else:
            for i in senses:
                oss = wn.traceRelationOS(i.wnid, t[2], t[3])
                if not oss:
                    print("Synset not found\n", file=out)
                else:
                    print("\n".join(oss), end="\n\n", file=out)
        return

    if t[0] == ".ci":   # .ci
        if len(t) < 5:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        foundtarg = wn.isIDConnectedWith(t[1], t[2], t[3], set(t[4:]))
        if foundtarg:
            print("Connection found to {0}".format(foundtarg), file=out)
        else:
            print("No connection found", file=out)
        return

    if t[0] == ".cl":   # .cl
        if len(t) < 5:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        foundid, foundtarg = wn.isLiteralConnectedWith(t[1], t[2], t[3], set(t[4:]))
        if foundid and foundtarg:
            print("Connection found:\nSense of literal: {0}\nTarget id: {1}".format(foundid, foundtarg), file=out)
        else:
            print("No connection found", file=out)
        return

    if t[0] == ".s":    # .s
        if not sf:
            print("Sorry, semantic features not loaded.", file=out)
            return

        if len(t) != 2:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        ids = sorted(sf.lookUpFeature(t[1]))
        if ids:
            print("{0} synset(s) found:\n{1}".format(len(ids), "\n".join(ids)), file=out)
        else:
            print("Semantic feature not found", file=out)
        return

    if t[0] == ".sc":   # .sc
        if not sf:
            print("Sorry, semantic features not loaded.", file=out)
            return

        if len(t) != 4:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        foundid, foundtargid = sf.isLiteralCompatibleWithFeature(t[1], t[2], t[3])
        if foundid and foundtargid:
            print("Compatibility found:\nSense of literal: ", end="", file=out)
            write_synset_id(wn, foundid, t[2], out)
            print("Synset ID pertaining to feature: ", end="", file=out)
            write_synset_id(wn, foundtargid, t[2], out)
        else:
            print("Compatibility not found", file=out)
        return

    if t[0] == ".cli":  # .cli <literal> <pos> <id> [hyponyms]
        hyps = len(t) == 5 and t[4] == "hyponyms"

        if not (len(t) == 4 or hyps):
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        if wn.isLiteralCompatibleWithSynset(t[1], t[2], t[3], hyps):
            print("Compatible", file=out)
        else:
            print("Not compatible", file=out)
        return

    if t[0] == ".slc":  # .slc <literal1> <literal2> <pos> <relation>
        addtop = len(t) == 6 and t[5] == "top"

        if not (len(t) == 5 or addtop):
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        print("Results:", file=out)
        for key, (wnid1, wnid2) in sorted(wn.similarityLeacockChodorow(t[1], t[2], t[3], t[4], addtop).items(), reverse=True):  # tSims
            print("  {0}\t{1}  {2}".format(key, wnid1, wnid2), file=out)
        return

    if t[0] == ".md":   # .md
        if len(t) != 4:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        print(wn.getMaxDepth(t[1], t[2], t[3]), file=out)
        return

    if t[0] == ".sg":   # .sg
        if len(t) != 4:
            print("Incorrect format for command {0}\n".format(t[0]), file=out)
            return

        print(wn.getSubGraphSize(t[1], t[2], t[3]), file=out)
        return

    print("Unknown command\n", file=out)

# This is exact same function as Synset.writeStr(out)
def write_synset(syns, out):
    buff = []
    for i in syns.synonyms:
        buff.append("{0}:{1}".format(i.literal, i.sense))
    print("{0}  {{{1}}}  ({2})".format(syns.wnid, ", ".join(buff), syns.definition), file=out)


def write_synset_id(wn, wnid, pos, out):
    syns = wn.lookUpID(wnid, pos)
    if syns:
        write_synset(syns, out)


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage:\n  {0} <WN_XML_file> [<semantic_features_XML_file>]".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    # init WN
    print("Reading XML...", file=sys.stderr)
    # Logging to devnull for all OS
    # Source: http://stackoverflow.com/a/2929946
    wn = WNQuery.WNQuery(sys.argv[1], open(os.devnull, "w"))
    wn.writeStats(sys.stderr)

    # init SemFeatures (if appl.)
    if len(sys.argv) == 3:
        print("Reading SemFeatures...", file=sys.stderr)
        sf = SemFeatures.SemFeaturesParserContentHandler(wn)
        stats = sf.readXML(sys.argv[2])
        print("{0} pairs read".format(stats), file=sys.stderr)
    else:
        sf = None

    # query loop
    print("Type your query, or .h for help, .q to quit", file=sys.stderr)
    while True:
        #print(">", end="", file=sys.stderr)
        #line = sys.stdin.readline().strip()
        sys.stderr.flush()
        line = input('>').strip()
        if line == ".q":
            sys.exit(0)
        elif line != "":
            try:
                process_query(wn, sf, line, sys.stdout)
            except InvalidPOSException as e:
                print(e, file=sys.stderr)

class InvalidPOSException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

if __name__ == '__main__':
    main()
