import os
if __name__ == '__main__':
    os.system("sphinx-apidoc -F -H cvxFin -A thomas.schmelzer -V 1.0 -R 1.0.0 -o doc cvxFin [*/tests]")

    os.chdir("doc")
    os.system("make clean")
    os.system("make html")
    os.chdir("..")
