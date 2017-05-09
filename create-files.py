import os
numtab = open('gold/numtab.txt')

print numtab
print os.path.getsize('gold/numtab.txt')
for line in numtab:
	print 'test'
	print line
