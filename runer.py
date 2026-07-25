import os

#-----------------------------------------------------
# STACK E VARIAVEIS LOCAIS
#-----------------------------------------------------

stack = []
locals_ = [0] * 256


#-----------------------------------------------------
# INSTRUCOES DA MINI JVM
#-----------------------------------------------------

def iconst(v):
    stack.append(v)


def bipush(v):
    stack.append(v)


def iload(n):
    stack.append(locals_[n])


def istore(n):
    locals_[n] = stack.pop()


def iadd():
    b = stack.pop()
    a = stack.pop()
    stack.append(a + b)


def isub():
    b = stack.pop()
    a = stack.pop()
    stack.append(a - b)


def imul():
    b = stack.pop()
    a = stack.pop()
    stack.append(a * b)


def idiv():
    b = stack.pop()
    a = stack.pop()

    if b == 0:
        print("division by zero")
        exit(1)

    stack.append(a // b)


def getstatic():

    # Ignorado nesta mini JVM.
    pass


def invokevirtual(text):

    # System.out.println(int)

    if "PrintStream.println" in text:

        if len(stack) == 0:
            print("stack underflow")
            exit(1)

        value = stack.pop()
        print(value)
        return

    print("invokevirtual nao suportado")
    print(text)
    exit(1)


#-----------------------------------------------------
# CARREGA O MAIN DO FICHEIRO JASM
#-----------------------------------------------------

def load_main(filename):

    f = open(filename, "r")
    body = f.readlines()
    f.close()

    code = []

    inside_main = False

    for line in body:

        line = line.strip()

        if ("public" in line) and ("main" in line):
            inside_main = True
            continue

        if inside_main:

            # fim do método
            if line == "}":
                break

            # ignorar informação do jdis
            if line == "":
                continue

            code.append(line)

    return code
#-----------------------------------------------------
# INTERPRETADOR
#-----------------------------------------------------

def execute(code):

    pc = 0

    while pc < len(code):

        line = code[pc].strip()
        line=line.replace(";","")
        #---------------------------------------------
        #print (line)
        if line == "iconst_0":
            iconst(0)

        elif line == "iconst_1":
            iconst(1)

        elif line == "iconst_2":
            iconst(2)

        elif line == "iconst_3":
            iconst(3)

        elif line == "iconst_4":
            iconst(4)

        elif line == "iconst_5":
            iconst(5)

        #---------------------------------------------

        elif line.startswith("bipush"):
            
            value = int(line.split()[1])
            bipush(value)

        #---------------------------------------------

        elif line.startswith("iload_"):

            n = int(line.split("_")[1])
            iload(n)

        elif line.startswith("iload "):

            n = int(line.split()[1])
            iload(n)

        #---------------------------------------------

        elif line.startswith("istore_"):

            n = int(line.split("_")[1])
            istore(n)

        elif line.startswith("istore "):

            n = int(line.split()[1])
            istore(n)

        #---------------------------------------------

        elif line == "iadd":
            iadd()

        elif line == "isub":
            isub()

        elif line == "imul":
            imul()

        elif line == "idiv":
            idiv()

        #---------------------------------------------

        elif line.startswith("getstatic"):

            getstatic()

        #---------------------------------------------

        elif line.startswith("invokevirtual"):

            invokevirtual(line)

        #---------------------------------------------

        elif line == "return":

            print("\nprogram finished.")
            return

        #---------------------------------------------

        else:

            # ignorar linhas do jdis que nao nos interessam

            pass

        pc += 1


#-----------------------------------------------------
# MAIN
#-----------------------------------------------------

print("\033c\033[47;30m")
print("give me file .class ?")
print()

filename = input().strip()

classname = filename.replace(".class", "")

#-----------------------------------------------------
# CONVERTER CLASS -> JASM
#-----------------------------------------------------

cmd = "/usr/bin/openjdk-asmtools-jdis $1 -w /tmp/"

cmd = cmd.replace("$1", filename)

os.system(cmd)

jasm_name = "/tmp/" + classname + ".jasm"

if not os.path.exists(jasm_name):

    print("cannot create jasm file")
    exit(1)

#-----------------------------------------------------
# CARREGAR O METODO MAIN
#-----------------------------------------------------

code = load_main(jasm_name)

print("\n------------ BYTECODES ------------\n")

for i in code:
    print(i)

print("\n------------ EXECUTION ------------\n")

#-----------------------------------------------------
# EXECUTAR
#-----------------------------------------------------

execute(code)