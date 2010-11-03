#! /usr/bin/env python

if __name__ == '__main__':
    import sys
    import optparse
    
    option_parser = optparse.OptionParser()
    option_parser.add_option('-x','--xxx',dest='xxxx',type='int')
    (options,args) = option_parser.parse_args()
    
    if len(args) == 2:
        inhandle = open(args[0],'r')
        outhandle = open(args[1],'w')
    elif len(args) == 1:
        inhandle = open(args[0],'r')
        outhandle = sys.stdout
    elif len(args) == 0:
        inhandle = sys.stdin
        outhandle = sys.stdout



# OR

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) == 3:
        inhandle = open(sys.argv[1],'r')
        outhandle = open(sys.argv[2],'w')
    elif len(sys.argv) == 2:
        inhandle = open(sys.argv[1],'r')
        outhandle = sys.stdout
    elif len(sys.argv) == 1:
        inhandle = sys.stdin
        outhandle = sys.stdout
