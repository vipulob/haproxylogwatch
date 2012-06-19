#!/usr/bin/env python


# haproxylogwatch v.1
# Author : Vipul Borikar

# Created : 15/06/2012
# Modified : 16/06/2012

# Usage :    python haproxy date "yyyy-mm-dd"  time "hh:mm:ss" file '/path/to/file'

import sys
import re
    


class haproxy():
    
    def date_formation(self,month,day):
        
        month_dict = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','July':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        
        self.date = "2012-%s-%s" %(month_dict[month],day)
    
        #print self.date
    
    def main(self):
        
        # oepn a log file in read mode
        fp = open(file_name,"r")
        
        self.first_line=""
        
        # Counter for GET request. The number of GET request took place.
        self.count_GET = 0
        
        # Counter for POS request. The number of POST request took place.
        self.count_POST = 0
        
        # Count the Client IP
        self.count_IP = 0
        
        # Client IP Dict
        self.client_dict = {}
        
        # To count total bytes 
        self.count_bytes = 0
        
        # Successful transaction counter
        self.count_success = 0
        
        # Run the loop over the log file to check for the line where the user
        # suplied date gets match or is greater. Stop the iteration as soon as match happens 
        for lines in fp:
            
            match_date = re.search(r"(\w+)  (\d+) (\d+:\d+:\d+)",lines)
            
            if not match_date:
                match_date = re.search(r"(\w+) (\d+) (\d+:\d+:\d+)",lines)
                
            self.date_formation(match_date.group(1),match_date.group(2))
            
            if self.date == date_input or self.date > date_input:
                #print "Matched"
                first_line = lines
                break
                
        #print self.date
        
        # Process the first line
        match_first_line_GET = re.search(r"GET",first_line)
        
        if match_first_line_GET:
            self.count_GET +=1
            
        match_first_line_POST = re.search(r"POST",first_line)
        
        if match_first_line_POST:
            self.count_POST += 1
            
            
        # Run the loop again for remaining lines to gather info about request.
        for lines in fp:
            
            # Try to grep GET in the line. If it mactches count it.
            match_GET = re.search(r"GET",lines)             
            
            if match_GET:
                self.count_GET += 1
                
            
            # Try to grep POST in the line. If it mactches count it.
            match_POST = re.search(r"POST",lines)         
            
            if match_POST:
                self.count_POST += 1    
    
            # Try to grep client IP address in the line. If it mactches count it.
            match_client_IP = re.search(r"\d+\.\d+\.\d+\.\d+", lines)
            
            if match_client_IP:
                
                try:
                    
                    self.client_dict[match_client_IP.group()] += 1
                except KeyError:
                    
                    self.client_dict[match_client_IP.group()] = 1
                    
                
                    
            match_request_size = re.search(r"(\d+/\d+/\d+/\d+/\d+) (\d+) (\d+)",lines)
            
            self.count_bytes = int(match_request_size.group(3)) + self.count_bytes
            
            if match_request_size.group(2) == '200':
                
                self.count_success += 1
    
        print " The No of GET Request is:%d" %self.count_GET
        print " The No of POST Request is:%d" %self.count_POST
        

        for IP,count in self.client_dict.iteritems():
            print " Client IP: %s  Connections: %d" %(IP,count) 
    
        print " Size of Data: %d KB" %(self.count_bytes/1000)
        
        print " No of Successful Transactions : %d"  %(self.count_success)
        

# Taking Input from command line       
if len(sys.argv) != 7:
    
    print " Please enter Proper Attributes"
    print " Usage : python haproxy date yyyy-mm-dd  time hh:mm:ss file /path/to/file "
    exit()

date_input = sys.argv[2]
time_input = sys.argv[4]
file_name =  sys.argv[6]

ha = haproxy()

ha.main()