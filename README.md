# pywnxml
Python3 API for WordNet XML (Hungarian WordNet / BalkaNet / VisDic format)

Authors: Balázs Indig (pyhton3 port), Márton Miháltz <mmihaltz@gmail.com> (C++ original version)

Files:

WNQuery.py: Pure Python 3 API for parsing and querying XML WordNet file.

wnxmlconsole.py: console application for executing queries on WN XML file using simple command strings.

Changes:

2015-02-18:
- First release on github. Changes introduced since python3 port:
- Fixed Synset.writeXML(): moved XML header printing to Synset.writeXMLHeader(). 
- Added support for the ID3 and ELR3 tags introduced in HuWN release 2014-08-14. 
- Bugfix: escaping illegal XML pcdata characters for literals.

See also:
- Hungarian WordNet in XML format: http://github.com/mmihaltz/huwn

License:
GNU GENERAL PUBLIC LICENSE, Version 2, June 1991
