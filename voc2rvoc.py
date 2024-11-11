'''
Convert standard VOC's to repeated VOC's. Simply:
* Search through the first 200 characters until encountering 0A012911
* Add 06020000FFFF at that point
* Copy all the remaining data
* Add 0700000000 at the end
'''

import sys

print('VOC2RVOC v2024 by Fish')

# Asking for help?
if len(sys.argv) <= 1 or ('?' in sys.argv) or ('/?' in sys.argv) or ('-?' in sys.argv) or ('-help' in sys.argv):
    print('\nUsage:\n\nvoc2rvoc inputfile [outputfile]\n')
    print('If no output file specified, the original input file will be modified.')
    print('Make sure you have got necessary permissions to read and write.\n')

# Load input data
try:
    inf = open(sys.argv[1], 'rb')
    infr = inf.read()
    inf.close()
except:
    print('Error - could not open the input file!')
    sys.exit(1)

# Determine output file
if len(sys.argv) == 2:
    outf = sys.argv[1]
else:
    outf = sys.argv[2]

# Locate the key header
hdrloc = infr.find(bytes([10, 1, 41, 17]))
if hdrloc < 0 or hdrloc > 200:
    print('Error - necessary header position not found in the input file!')
    sys.exit(1)

# Write a file
try:
    outf = open(outf, 'wb')
except:
    print('Error - could not open the output file!')
    sys.exit(1)

try:
    # Firstly write the chunk up to the header, including it
    outf.write(infr[0:hdrloc + 4])
    # Add the repeat marker
    outf.write(bytes([6, 2, 0, 0, 255, 255]))
    # Add the rest
    outf.write(infr[hdrloc+4:])
    # Final closer
    outf.write(bytes([7,0,0,0,0]))
except:
    print('Error - could not write to the output file!')
    sys.exit(1)

outf.close()
print('Done')