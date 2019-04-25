import sys
import getopt

class Inputs():
    def __init__(self):
        self.args = self.parse_command_line()
        
    def parse_command_line(self):
        sys.stdout.write('Collecting input ... ')
        shortopts = 'd:s:p:g:i:a:e:hm:o:'
        longopts = ['domain2domain=', 'gene2svars=', 'svar2protein=', 'gene2gene=', \
                    'svar2domains=', 'significant_svars=', 'expression=', 'help',\
                    'min_threshold=', 'output=']
        try:
            opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
        except getopt.GetoptError as err:
            print(err)
            self.help()
            sys.exit(2)
            
        values = {'min_threshold':0.15, 'output':'multi_granularity_graphs.tsv'}
        for o, a in opts:
            if o == '-d' or o == '--domain2domain':
                values['domain2domain'] = a
            elif o == '-s' or o == '--gene2svars':
                values['gene2svars'] = a
            elif o == '-p' or o == '--svar2protein':
                values['svar2protein'] = a
            elif o == '-g' or o == '--gene2gene':
                values['gene2gene'] = a
            elif o == '-i' or o == '--svar2domains':
                values['svar2domains'] = a
            elif o == '-a' or o == '--significant_svars':
                values['significant_svars'] = a
            elif o == '-e' or o == '--expression':
                values['expression'] = a
            elif o == '-m' or o == '--min_threshold':
                values['min_threshold'] = float(a)
            elif o == '-o' or o == '--output':
                values['output'] = a
            elif o == '-h' or o == '--help':
                self.help()
                sys.exit(0)
                
        if not opts:
            self.help()
            sys.exit(0)
            
        sys.stdout.write('done\n')
        return values
    
    def help(self):
        out = '\n'
        out += 'command: multi_granularity_graphs\n'
        out += 'purpose: construct potential protein mechanistic from domains of interest in survival-significant splice variants\n'
        out += '\n'
        
        out += 'required parameters:\n'
        out += '\t-d  --domain2domain=\t\tFile with structure: "<domain>\t<domain>\\n"\n'
        out += '\t-s  --gene2svars=\t\tFile with structure: "<gene>\t<splice variant1>,<splice variant2>,...,<final splice variant>\\n"\n'
        out += '\t-p  --svar2protein=\t\tFile with structure: "<splice variant>\t<protein>\\n"\n'
        out += '\t-g  --gene2gene=\t\tFile with structure: "<gene>\t<gene>\\n"\n'
        out += '\t-i  --svar2domains=\t\tFile with structure: "<splice variant>\t<domain1>,<domain2>,...,<final domain>\\n"\n'
        out += '\t-a  --significant_svars=\tOutput file from NEEP code. (1st col: name; 4th col: adjusted significance value)\n'
        out += '\t-e  --expression=\t\tCSV file with expression table. (1st row: header)\n'
        out += '\n'
        
        out += 'optional parameters:\n'
        out += '\t-m  --min_threshold\tThe minimum threshold used for NEEP. (default: 0.15)\n'
        out += '\t-h  --help\tPrint this message.\n'
        out += '\n'
        
        sys.stdout.write(out)
        return