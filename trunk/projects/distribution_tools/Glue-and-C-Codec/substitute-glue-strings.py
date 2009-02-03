import sys


theVersion=sys.argv[1]
uploadedDevFileBase=sys.argv[2]
uploadedMacFileBase=sys.argv[3]
uploadedDevFileName=uploadedDevFileBase+".tar.gz"

devLink="http://rl-glue-ext.googlecode.com/files/"+uploadedDevFileName
devDetailsLink="http://code.google.com/p/rl-glue-ext/downloads/detail?name="+uploadedDevFileName

macLink="http://rl-glue-ext.googlecode.com/files/"+uploadedMacFileBase
macDetailsLink="http://code.google.com/p/rl-glue-ext/downloads/detail?name="+uploadedMacFileBase

fileName="RLGlueCore.wiki.template"
outfileName="RLGlueCore.wiki"

subs={}
subs['GLUE-DEV-VERSION']=theVersion
subs['GLUE-DEV-LINK']=devLink
subs['GLUE-DEV-DETAILS-LINK']=devDetailsLink
subs['GLUE-DEV-FILE-BASE']=uploadedDevFileBase
subs['MAC-LINK']=macLink
subs['MAC-DETAILS-LINK']=macDetailsLink
f = file(fileName)
newlines = []
for line in f:
	for key,value in subs.iteritems():
		if key in line:
			line=line.replace(key,value)
	newlines.append(line)

outfile = file(outfileName, 'w')
outfile.writelines(newlines)