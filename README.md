# pywnxml
Python3 API for WordNet XML (Hungarian WordNet in BalkaNet/VisDic XML format)

Authors: Balázs Indig (pyhton3 port), Márton Miháltz <mmihaltz@gmail.com> (C++ original version)

Files:

WNQuery.py: Pure Python 3 API for parsing and querying XML WordNet file.

wnxmlconsole.py: console application for executing queries on WN XML file using simple command strings.

Changes:

2015-04-29:
- wnxmlconsole.py will now run on non-Linux OS's (tested: Windows 7), i.e. no exception if readline module cannot be loaded
- stats printed by wnxmlconsole.py now includes number of distinct literals (words)

2015-02-18:
- First release on github. Changes introduced since python3 port:
- Fixed Synset.writeXML(): moved XML header printing to Synset.writeXMLHeader(). 
- Added support for the ID3 and ELR3 tags introduced in HuWN release 2014-08-14. 
- Bugfix: escaping illegal XML pcdata characters for literals.

See also:
- Hungarian WordNet in XML format: https://github.com/dlt-rilmta/huwn

License:
GNU GENERAL PUBLIC LICENSE, Version 2, June 1991
