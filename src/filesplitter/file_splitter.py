import os
import csv
import math
import argparse
import time

def split_file(file_name, delimiter=',', row_limit=10000, parts=0, output_path='.', keep_headers=True):
    isValid = os.path.exists(file_name) and os.path.isfile(file_name)
    if isValid is False:
        print("invalid file ", file_name)
    
    #open file
    filehandler = open(file_name,'r')
    
    #if going by parts, get total rows and define row limit
    if parts > 0:
    	#read file to count total number of rows
        count_rows_reader = csv.reader(filehandler)
        totalrows = 0
        for row in count_rows_reader: totalrows += 1
        totalrows -= 1 #don't want to count header
        row_limit = math.ceil(totalrows / parts) # round up for row limit
        filehandler.seek(0)
        
    #read file for actual splitting
    reader = csv.reader(filehandler, delimiter=delimiter)
    
    #create output template from supplied input file path
    base =  os.path.splitext(os.path.basename(file_name))[0]
    output_name_template = base+'_part_%s.csv'
    
    #create output directory
    timestamp = int(time.time())
    output_dir = os.path.join(output_path,base,str(timestamp))
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    current_piece = 0
    current_limit = 0
    #populate first file, then move to next file
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(output_dir, output_name_template  % current_piece)
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if current_piece == 1 and keep_headers == 1: 
            	headers = row
            elif keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)
    
    output_list=[]
    abs_path = os.path.abspath(output_dir)
    for i in range(current_piece): output_list.append(os.path.join(abs_path,output_name_template % i))
    return output_list

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process file splitter args')
    parser.add_argument('inputfile',help='input file path')
    parser.add_argument('-o','--output',default='.',help='output file path')
    
    #can split only by rows or parts, not both
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r','--rows',type=int,default=10000,help='number of rows per each output file')
    group.add_argument('-p','--parts',type=int,default=0,help='number of parts to split file into, regardless of rows')
    
    args = parser.parse_args()
    print("Input file is: "+args.inputfile)
    if args.output: print("Output file path is: "+args.output)
    if args.rows and args.parts == 0: print("Rows per output file: "+str(args.rows))
    if args.parts: print("Number of output files: "+str(args.parts))
    
    split_file(args.inputfile,row_limit=args.rows,parts=args.parts,output_path=args.output)