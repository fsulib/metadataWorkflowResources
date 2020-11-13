import sys
import urllib2
import zlib
import time
import re
import xml.dom.pulldom
import operator
import codecs
from optparse import OptionParser

nDataBytes, nRawBytes, nRecoveries, maxRecoveries = 0, 0, 0, 3

def getFile(serverString, command, verbose=1, sleepTime=0):
	global nRecoveries, nDataBytes, nRawBytes
	if sleepTime:
		time.sleep(sleepTime)
	remoteAddr = serverString + '?verb=%s' % command
	if verbose:
		print "\r", "Fetching set list ...'%s'" % remoteAddr[-90:]
	headers = {'User-Agent': 'OAIHarvester/2.0', 'Accept': 'text/html', 'Accept-Encoding': 'compress, deflate'}
	try:
		remoteData = urllib2.urlopen(remoteAddr).read()
	except urllib2.HTTPError, exValue:
		if exValue.code == 503:
			retryWait = int(exValue.hdrs.get("Retry-After", "-1"))
			if retryWait < 0:
				return None
			print 'Waiting %d seconds' % retryWait
			return getFile(serverString, command, 0, retryWait)
		print exValue
		if nRecoveries < maxRecoveries:
			nRecoveries += 1
			return getFile(serverString, command, 1, 60)
		return
	nRawBytes += len(remoteData)
	try:
		remoteData = zlib.decompressobj().decompress(remoteData)
	except:
		pass
	nDataBytes += len(remoteData)
	mo = re.search('<error *code=\"([^"]*)">(.*)</error>', remoteData)
	if mo:
		print "OAIERROR code=%s '%s'" % (mo.group(1), mo.group(2))
	else:
		return remoteData

if __name__ == "__main__":

	serverString = 'http://fsu.digital.flvc.org/oai2'
	outFileName = 'assets/setSpec.xml'

	print "Writing records to %s from %s" % (outFileName, serverString)
	
	ofile = codecs.lookup('utf-8')[-1](file(outFileName, 'wb'))

	ofile.write('<repository xmlns:oai_dc="http://www.openarichives.org/OAI/2.0/oai_dc/" \
	 xmlns:dc="http://purl.org/dc/elements/1.1/" \
	 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n')

	data = getFile(serverString, 'ListSets')

	recordCount = 0

	while data:
		events = xml.dom.pulldom.parseString(data)
		for (event, node) in events:
			if event == "START_ELEMENT" and node.tagName == 'set':
				events.expandNode(node)
				node.writexml(ofile)
				recordCount += 1
		mo = re.search('resumptionToken[^>]*>(.*)</resumptionToken>', data)
		if not mo:
			break
		data = getFile(serverString, "ListSets&resumptionToken=%s" % mo.group(1))
	
	ofile.write('\n</repository>\n'), ofile.close()

	print "\nRead %d bytes (%.2f compression)" % (nDataBytes, float(nDataBytes) / nRawBytes)
	print "Wrote out %d records" % recordCount
