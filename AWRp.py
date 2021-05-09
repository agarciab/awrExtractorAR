#!/usr/bin/python
"""
    AWRp.py - Oracle AWR Parser 
    Copyright 2019 Alexandre Marti. All rights reserved. To more info send mail to alexandremarti@gmail.com.
    Licensed under the Apache License, Version 2.0. See LICENSE.txt for terms & conditions.

    Purpose: Print AWR HTML file content as a table format.
    Author: Alexandre Marti
                  
    Usage:       
        python AWRp.py -files <html file name list or mask>         

    Optional Parameters
        -fmt: table type output format. the default format is psql 
              csv,plain,simple,grid,fancy_grid,pipe,orgtbl,jira,presto,psql,rst,mediawiki,moinmoin,youtrack,html,latex,latex_raw,latex_booktabs,textile
              more details on https://pypi.org/project/tabulate/
              
        -listsections : print a list of all sections parsed by AWRp.py. It´s useful to find section number for parameter -sections
        -sections: used to restrict which awr sections the AWRp.py will return. use -listsections to get the list of sections available.        

    Example1:
        python AWRp.py -files /files/awrfile.html
    
    Example2:    
        python AWRp.py -files /files/*.html
        
    Example3:    
        python AWRp.py -files '/files/awrfile01.html','/files/awrfile02.html'

    Example4:        
        python AWRp.py -listsections
        
    Example5:        
        python AWRp.py -files /files/*.html -sections 1,3,4               

    Help:
        python AWRp.py -h

"""

import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import glob   
import argparse
import sys

NoneType = type(None)

def getData(content, filter):    
    '''
        Find AWR Table Section using the filter
    '''

    table = content.find('table', {'summary': filter})       
    # Testing if it didn´t find awr section
    if not isinstance(table, NoneType):    
        ret = pd.read_html(str(table),header=0)
        ret[0].rename(columns = {'Unnamed: 0': 'Info'}, inplace=True)
        return ret


def printTable(data,fmt):  
    '''
        Print the pandas dataframe in the format defined
    '''

    if not isinstance(data, NoneType):    
        if fmt == 'csv':            
            print(data[0].to_csv(index=False))
        else:
            print( tabulate(data[0], headers='keys', tablefmt=fmt,showindex=False) )  


def main():

    try:
        # CMD Parameters
        version = "1.0"
        version_description = "AWRp - Oracle AWR Parser {}".format(version)

        parser = argparse.ArgumentParser(description = version_description) 
        parser.add_argument("-files", help="Comma-delimited list of HTML AWR files", default="")
        parser.add_argument("-fmt", help="Table Format to display. The default is psql", default="psql", choices=['jira','csv','plain','simple','grid','fancy_grid','pipe','orgtbl','presto','psql','rst','mediawiki','moinmoin','youtrack','html','latex','latex_raw','latex_booktabs','textile'])
        parser.add_argument("-listsections", help="List of all sections parsed by AWRp.py", action="store_true")        
        parser.add_argument("-sections", help="Comma-delimited numbers of awr sections to be returned by AWRp.py", default="")
        
               
        # If parse fail will show help
        args = parser.parse_args()
        
        sections = []
        if args.sections != "":
            sections = args.sections.split(",")

        # list of awr sections to parse
        infolist = ['This table displays database instance information',
                    'This table displays snapshot information',
                    'This table displays load profile',
					'This table displays CPU usage and wait statistics',
                    'This table displays top 10 wait events by total wait time',
                    'This table displays top SQL by elapsed time', 
                    'This table displays top SQL by CPU time',
                    'This table displays top SQL by user I/O time',
                    'This table displays top SQL by buffer gets',
                    'This table displays top SQL by physical reads',
                    'This table displays top SQL by unoptimized read requests',
                    'This table displays top SQL by number of executions',
                    'This table displays top SQL by number of parse calls',
                    'This table displays top SQL by amount of shared memory used',
                    'This table displays top SQL by version counts',
                    'This table displays top SQL by cluster wait time',
                    'This table displays Foreground Wait Events and their wait statistics',
                    ]
        #infolist = ['This table displays top SQL by cluster wait time',]
        
        
        if args.listsections:
            print("Printing the List of Parseable AWR Sections")
            print("===========================================\n")                
            for i, info in enumerate(infolist):                                
                print("    Section {}: {}".format(i,info)) 
                
        elif args.files == "":
            print("Ops! You need to pass the HTML file name.")
            print("Example:")            
            print("    AWRp.py -file /path/awrfile.html or AWRp.py -file /path/*.html")            
        else:                
            filelist = args.files.split(",")
            
            for fn in filelist:
                files=glob.glob(fn)           
                for file in files:
                    try:
                        print("Data from File: {}\n".format(file), file=sys.stderr)
                        f=open(file)
                        soup = BeautifulSoup(f,'lxml')                                    
                        for i, info in enumerate(infolist):                        
                            if len(sections) == 0 or str(i) in sections:
                                print("\nSECTION {}: {}\n".format(i,info), file=sys.stderr)                    
                                printTable(getData(soup,info),args.fmt)                            
                            
                    finally:
                        f.close()
    
    finally:    
        print("\nAWRp.py Finished\n", file=sys.stderr)
        

if __name__ == '__main__':
    main()
    