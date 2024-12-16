Have you ever seen this? 

***UnicodeEncodeError: 'XXXXX' codec can't encode character 'XXXXX' in position 15: ordinal ...***

Probably more than once, right? :) After having spent too much time on finding the right codecs for files, I wrote [BruteCodecChecker](https://github.com/hansalemaos/BruteCodecChecker). BruteCodecChecker (MIT) opens a file in all codecs available in your environment and prints the results. It also works for byte objects. 

If you work, like me,  with a lot of text files, it will save you a lot of time.

### Install it:

```python
pip install BruteCodecChecker
```

### Try it:

```python
from BruteCodecChecker import CodecChecker
teststuff = b"""This is a test! 
Hi there!
A little test! """
testfilename = "test_utf8.tmp"
with open("test_utf8.tmp", mode="w", encoding="utf-8-sig") as f:
    f.write(teststuff.decode("utf-8-sig"))
codechecker = CodecChecker()
codechecker.try_open_file(testfilename, readlines=2).print_results(
    pause_after_interval=1, items_per_interval=10
)
codechecker.try_open_file(testfilename).print_results()
codechecker.try_convert_bytes(teststuff.decode("cp850").encode()).print_results(
    pause_after_interval=1, items_per_interval=10
)


```

### **Output**

```
Codec               : palmos                                                       
Mode                : strict
Length              : 32
Converted           : 
Line: 0              ï»¿This is a test! 
Line: 1                  Hi there!
Codec               : ptcp154                                                      
Mode                : strict
Length              : 32
Converted           : 
Line: 0              п»ҝThis is a test! 
Line: 1                  Hi there!
Codec               : punycode                                                     
Mode                : strict
Codec               : quopri_codec                                                 
Mode                : strict
Codec               : raw_unicode_escape                                           
Mode                : strict
Length              : 32
Converted           : 
Line: 0              ï»¿This is a test! 
Line: 1                  Hi there!
Codec               : rot_13                                                       
Mode                : strict
Codec               : shift_jis                                                    
Mode                : strict
Codec               : shift_jisx0213                                               
Mode                : strict
Length              : 31
Converted           : 
Line: 0              鬠ｿThis is a test! 
Line: 1                  Hi there!
Codec               : shift_jis_2004                                               
Mode                : strict
Length              : 31
Converted           : 
Line: 0              鬠ｿThis is a test! 
Line: 1                  Hi there!
Codec               : tis_620                                                      
Mode                : strict
Length              : 32
Converted           : 
Line: 0              ๏ปฟThis is a test! 
Line: 1                  Hi there!
Codec               : undefined                                                    
Mode                : strict
Codec               : unicode_escape                                               
Mode                : strict
Length              : 32
Converted           : 
Line: 0              ï»¿This is a test! 
Line: 1                  Hi there!
Codec               : utf_16                                                       
Mode                : strict
Codec               : utf_16_be                                                    
Mode                : strict
Codec               : utf_16_le                                                    
Mode                : strict
Codec               : utf_32                                                       
Mode                : strict
Codec               : utf_32_be                                                    
Mode                : strict
Codec               : utf_32_le                                                    
Mode                : strict
Codec               : utf_7                                                        
Mode                : strict
Codec               : utf_8                                                        
Mode                : strict
Length              : 30
Converted           : 
Line: 0              ﻿This is a test! 
Line: 1                  Hi there!
Codec               : utf_8_sig                                                    
Mode                : strict
Length              : 29
Converted           : 
Line: 0              This is a test! 
Line: 1                  Hi there!
```
