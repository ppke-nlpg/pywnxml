# pywnxml
Python3 API for WordNet XML (Hungarian WordNet in BalkaNet/VisDic XML format)

*Authors*: Balázs Indig (pyhton3 port), Márton Miháltz <mmihaltz@gmail.com> (C++ original version)

**Contents**

- Pure Python 3 API for parsing and querying the XML WordNet file (import `WNQuery`)
- `wnxmlconsole.py`: console application for executing queries on WN XML file using simple command strings.

## Using the console application with *Hungarian WordNet*

*Requirements:*
- [Python 3](https://www.python.org/downloads/)
- [Hungarian WordNet XML files](https://github.com/mmihaltz/huwn)

Type `python wnxmlconsole.py <huwn_xml_file>` to launch the application. Once it has started, type `.h` to get help on the available commands. The following example queries hyponyms for all senses of the noun *kutya*:

```
>.rl kutya n hyponym
ENG20-02001223-n  {Canis familiaris:1, házikutya:1, kutya:1, eb:1}  (Ház- és nyájőrzésre, vadászatra használt vagy kedvtelésből tartott háziállat.)
  ENG20-02001977-n  {korcs kutya:1, korcs:1, keverék kutya:1}  (Nem fajtatiszta kutya.)
  ENG20-02002490-n  {öleb:1}  (Kedvtelésből tartott kis testű kutya.)
  ENG20-02004217-n  {vadászkutya:1}  (Vadászatra idomított kutyafajta.)
  ENG20-02020367-n  {munkakutya:1}  (Hasznos szolgálatáért tenyésztett, tartott kutya.)
  ENG20-02027313-n  {mopszli:1, mopsz:1}  (Tömpe orrú, kerek fejű öleb, szőre sima, farka hátára görbül; ázsiai eredetű.)
  ENG20-02027929-n  {spicc:1}  (Hegyes orrú, álló fülű, hosszú szőrű, zömök kutyafajta; északi eredetű.)
  ENG20-02029627-n  {uszkár:1, pudli:1}  (Hosszú, selymes fehér, fekete stb. szőrű, rendszerint különlegesen nyírt kisebb ősi kutyafajta, intelligens, gyakran vadászatra vagy előadásra idomították.)

ENG20-09256536-n  {kutya:2}  (Jelzett tulajdonsága miatt megvetést érdemlő személy.)
``` 

## Changes

2015-04-29:
- wnxmlconsole.py will now run on non-Linux OS's (tested: Windows 7), i.e. no exception if readline module cannot be loaded
- stats printed by wnxmlconsole.py now includes number of distinct literals (words)

2015-02-18:
- First release on github. Changes introduced since python3 port:
- Fixed Synset.writeXML(): moved XML header printing to Synset.writeXMLHeader(). 
- Added support for the ID3 and ELR3 tags introduced in HuWN release 2014-08-14. 
- Bugfix: escaping illegal XML pcdata characters for literals.

## See also

Hungarian WordNet in XML format: https://github.com/dlt-rilmta/huwn

## License
GNU GENERAL PUBLIC LICENSE, Version 2, June 1991
