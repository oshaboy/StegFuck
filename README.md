## StegFuck
This program takes a Brainfuck program and uses Steganography witchcraft to encode it as an image. 

# Requirements
  Python 3
  Pillow (install using `python3 -m pip install pillow`)
  
# Usage 
  encoding a file:  
  `python3 stegfuck.py -e [input image] [-f] [brainfuck code inline or code file] [output image]
  
  running an image:
  `python3 stegfuck.py [image]`
 
 
# Theory of operation. 
  The search term is Steganography. There is a good computerphile video about it. The code is encoded starting at the top left while the length of the program (which is neccessary to halt) is at the bottom right. 
  
 
  
