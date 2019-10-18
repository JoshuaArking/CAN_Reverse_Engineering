This is a work in progress rewrite of the Odometer_Integration_Transform.

Todo:  
<strike>Fix file detection to be less strict with file names</strike>  
<strike>rewrite J1979.py to USE A .CSV file of known PIDS</strike>  
<strike>Add bytewise reverse endian operations</strike>  
Add GUI for ease of use  
Add bitwise reverse endian operations  
Integrate support for different filetypes from https://github.com/JoshuaArking/asc2log  
Add support for .DBC files  
Improve input filtering  
Add support for realtime processing on ICS HW using https://github.com/intrepidcs/python_ics  
Add multi-trip awareness
Improve ability to add and compare truth data other than J1979 pids   
Create delta analysis to find the difference between two signals  
Add filters for signals only incrementing / decrementing, among other things  


