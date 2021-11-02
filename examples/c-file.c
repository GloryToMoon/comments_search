#include <stdio.h> // this is include
#include <string.h>


void /*this is main function*/ main() {
/*
	this code just create 3 variables
	copy a and b to c
	then print c

*/
	char a[20],b[20],c[40];
	strcpy(a,"/*/Test ");  // first string
	strcpy(b,"string//"); // to copy it in 'c'
	strcpy(c,a);
	strcat(c,b);
	printf/*printf*/ ("%s\n",c);
}
