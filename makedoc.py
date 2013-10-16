import os
if __name__ == '__main__':
    #os.system("sphinx-apidoc -f -F -H cvxFin -A \"Thomas Schmelzer\" -V 1.0 -R 1.0.0 -o doc cvxFin")
    os.chdir("doc")
    os.system("make clean")
    os.system("make html")
    os.chdir("..")
