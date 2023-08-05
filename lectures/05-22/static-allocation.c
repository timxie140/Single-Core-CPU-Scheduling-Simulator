/* static-allocation.c */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
  int x = 5;  /* x is statically allocated (on the stack) */
              /*   (4 bytes are allocated on the stack)   */

  printf( "x is %d\n", x );
  printf( "sizeof( int ) is %lu bytes\n", sizeof( int ) );
  printf( "sizeof( x ) is %lu bytes\n", sizeof( x ) );
                  /* %lu is long unsigned */


  int * y = NULL;  /* y is statically allocated (on the stack) */
  printf( "sizeof( int* ) is %lu bytes\n", sizeof( int* ) );
  printf( "sizeof( y ) is %lu bytes\n", sizeof( y ) );

  printf( "sizeof( char* ) is %lu bytes\n", sizeof( char* ) );
  printf( "sizeof( void* ) is %lu bytes\n", sizeof( void* ) );

#if 0
  /* seg-fault! */
  printf( "y points to %d\n", *y );
#endif

  y = &x;  /* & is the address-of operator */
  printf( "y points to %d\n", *y );

  printf( "x is at memory address %p\n", &x );
  printf( "y is at memory address %p\n", &y );
  printf( "y points to memory address %p\n", y );

  /* TO DO: add a char variable and display its memory address above... */

  return EXIT_SUCCESS;
}