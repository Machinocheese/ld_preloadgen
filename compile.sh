gcc -fPIC -c -o hook.o hook.c
gcc -shared -o hook.so hook.o -ldl
