import sys,math
from PIL import Image

code=[]
IP=0
tape=[0 for i in range(65536)]
pointer=32768
loop_stack=[]
input_buffer=""
skip=0
program_size=0
def inc():
    global pointer,IP
    tape[pointer]=(tape[pointer]+1)%256
    IP+=1
def dec():
    global pointer,IP
    tape[pointer]=(tape[pointer]-1)%256
    IP+=1

def pointer_left():
    global pointer, tape,IP
    pointer+=1
    if pointer>=len(tape):
        temp=[0 for i in range(65536)]
        tape=tape+temp
    IP+=1
def pointer_right():
    global pointer, tape,IP
    pointer-=1
    if pointer<0:
        temp=[0 for i in range(65536)]
        tape=temp+tape
        pointer+=65536
    IP+=1
def output_char():
    global IP
    print(chr(tape[pointer]), end="")
    IP+=1
def input_char():
    global IP,input_buffer
    if (input_buffer==""):
        input_buffer+=input()+"\n"
    tape[pointer]=ord(input_buffer[0])
    input_buffer=input_buffer[1:]
    IP+=1
def loop():
    global IP,skip
    if (tape[pointer]==0):
        skip+=1
    else:
        loop_stack.append(IP+1)

    IP += 1

def end():
    global IP
    if (tape[pointer]==0):
        IP+=1
        loop_stack.pop()
    else:
        IP=loop_stack[-1]


instructions=[inc,dec,pointer_right,pointer_left,output_char,input_char,loop,end]
brainfuck_commands=["+","-",">","<",".",",","[","]"]
def encode(image_filename, code_string ,dest_filename, bppness=32):


    code_length=len(code_string)
    channel_count=4
    dest_image_mode="RGBA"
    if(bppness==24):
        channel_count=3
        dest_image_mode="RGB"
    elif(bppness!=32):
        print("I only support 24 and 32 bpp RGB(A) Images")
        sys.exit(1)
    source_image=Image.open(image_filename).convert(dest_image_mode)
    image_dump = source_image.load()


    x=0
    y=0
    number_of_comment_chars=0
    print("Encoding Code")
    for i in range(0,code_length,channel_count):
        new_pixel=[]
        j=0
        while j < channel_count:
            if(i+j+number_of_comment_chars>=code_length):
                amount_done=len(new_pixel)
                for k in range(channel_count-amount_done):
                    new_pixel.append(image_dump[(x,y)][k+amount_done])
                break
            Found=False
            for k in range(8):
                if (brainfuck_commands[k] == code_string[i+j+number_of_comment_chars]):
                    new_pixel.append(k) #must be at j
                    Found=True
                    break
            if not Found:
                number_of_comment_chars+=1
                
            else:
                new_pixel[j]|=image_dump[(x,y)][j]&0xf8
                j+=1
        image_dump[(x, y)]=tuple(new_pixel)
        x+=1

        if (x>=source_image.width):
            x=0
            y+=1
        if (y>=source_image.height or (y==source_image.height-1 and x>=source_image.width-math.ceil(32/channel_count))) :
            print("Original Image File too small for Brainfuck program")
            sys.exit(3)
    code_length-=number_of_comment_chars
    y=source_image.height-1
    x=source_image.width-1
    print("Encoding Length")
    for i in range(0,16,channel_count):

        new_pixel=[]

        for z in range(channel_count):
            new_pixel.append(image_dump[(x,y)][z]&0xfc) #must be at z
            #print(code_length&3)
            new_pixel[z]|=(code_length&3)
            code_length>>=2


        image_dump[(x, y)]=tuple(new_pixel)
        x-=1
        if (x<0):
            x=source_image.width-1
            y-=1



    print("Saving")
    #dest_image=Image.frombytes(dest_image_mode,source_image.size,image_dump)
    source_image.save(dest_filename)

    print("Image saved as ", dest_filename)




def run(image_filename):
    global IP,skip
    global program_size
    source_image=Image.open(image_filename)
    source_image_dump = source_image.load()
    if (source_image.mode=="RGB"):
        bppness=24
    elif(source_image.mode=="RGBA"):
        bppness=32
    else:
        print("I only support 24 and 32 bpp RGB(A) Images")
        sys.exit(1)

    x=source_image.width-1
    y=source_image.height-1
    counter=0
    program_size=0
    while (counter<32):
        pixel=source_image_dump[(x,y)]
        for channel in pixel:
            program_size+=(channel&3)<<(counter)
            counter+=2
            if (counter>=32):
                break
        x-=1
        if (x<0):
            x=source_image.width
            y-=1
    x = 0
    y = 0
    i=0
    while(i<program_size):
        pixel = source_image_dump[(x, y)]
        for channel in pixel:
            if (i>=program_size):
                break
            code.append(channel&7)
            i+=1
        x+=1
        if (x>=source_image.width):
            x=0
            y+=1
    while(IP<program_size):
        #print(brainfuck_commands[code[IP]])
        #print(IP,code[IP], skip)
        if (skip>0):
            if(code[IP]==7):
                skip-=1
            elif (code[IP]==6):
                skip+=1

            IP+=1
        else:
            instructions[code[IP]]()



if __name__=="__main__":
    if (sys.argv[1]=="-e"):
        if (sys.argv[3]=="-f"):
            source_file=open(sys.argv[4],"r")
            source_data=source_file.read().replace("\n","")
            encode(sys.argv[2],source_data, sys.argv[5])
            source_file.close()
        else:
            encode(sys.argv[2],sys.argv[3],sys.argv[4])

    else:
        run(sys.argv[1])

