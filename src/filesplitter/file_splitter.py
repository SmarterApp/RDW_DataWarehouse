import os
import csv
import math
import argparse

def split_file(file_name, delimiter=',', row_limit=10000, parts=0, output_path='.', keep_headers=True):
    """
    Splits a CSV file into multiple pieces.
    
    A quick bastardization of the Python CSV library.

    Arguments:

        `row_limit`: The number of rows you want in each output file. 10,000 by default.
        `output_name_template`: A %s-style template for the numbered output files.
        `output_path`: Where to stick the output files.
        `keep_headers`: Whether or not to print the headers in each output file.

    Example usage:
    
        >> from toolbox import csv_splitter;
        >> csv_splitter.split(open('/home/ben/input.csv', 'r'));
    
    """
    
    isValid = os.path.exists(file_name) and os.path.isfile(file_name)
    if isValid is False:
        print("invalid file ", file_name)
    
    #open file
    filehandler = open(file_name,'r')
    
    #if going by parts, get total rows and define row limit
    if parts > 0:
        count_rows_reader = csv.reader(filehandler)
        totalrows = 0
        for row in count_rows_reader: totalrows += 1
        totalrows -= 1 #don't want to count header
        row_limit = math.ceil(totalrows / parts) # round up for row limit
        filehandler.seek(0)
    #
    reader = csv.reader(filehandler, delimiter=delimiter)
    
    #create output template from supplied input file path
    base =  os.path.splitext(os.path.basename(file_name))[0]
    output_name_template = base+'_part_%s'
    
    #create first file
    current_piece = 1
    current_out_path = os.path.join(
         output_path,
         output_name_template  % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)
    
    #populate first file, then move to next file
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(output_path, output_name_template  % current_piece)
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process file splitter args')
    parser.add_argument('inputfile',help='input file path')
    parser.add_argument('-o','--output',help='output file path')
    
    #can split only by rows or parts, not both
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r','--rows',type=int,help='number of rows per each output file')
    group.add_argument('-p','--parts',type=int,help='number of parts to split file into, regardless of rows')
    
    args = parser.parse_args()
    print("Input file is: "+args.inputfile)
    if args.output: print("Output file path is: "+args.output)
    if args.rows: print("Rows per output file: "+str(args.rows))
    if args.parts: print("Number of output files: "+str(args.parts))
    
    if args.output and args.rows:
        split_file(args.inputfile,row_limit=args.rows,output_path=args.output)
    elif args.output and args.parts:
        split_file(args.inputfile,parts=args.parts,output_path=args.output)
    elif args.output:
        split_file(args.inputfile,output_path=args.output)
    elif args.rows:
        split_file(args.inputfile,row_limit=args.rows)
    elif args.parts:
        split_file(args.inputfile,parts=args.parts)
    else:
        split_file(args.inputfile)
    
