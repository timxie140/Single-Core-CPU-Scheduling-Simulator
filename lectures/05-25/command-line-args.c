/* command-line-args.c */

#include <stdio.h>
#include <stdlib.h>

#if 0
int main( int argc, char * argv[] )
#endif
int main( int argc, char ** argv )
{
  printf( "argc is %d\n", argc );    /* argument count */

  if ( argc != 4 )
  {
    fprintf( stderr, "ERROR: Invalid arguments\n" );
    fprintf( stderr, "USAGE: a.out <filename> <x> <y>\n" );
    return EXIT_FAILURE;
  }

  printf( "argv[0] is %s\n", argv[0] );  /* argv + 0 */
  printf( "argv[1] is %s\n", argv[1] );
  printf( "argv[2] is %s\n", argv[2] );
  printf( "argv[3] is %s\n", argv[3] );

  printf( "argv[4] is %s\n", argv[4] );
  printf( "argv[5] is %s\n", argv[5] );
  printf( "argv[6] is %s\n", argv[6] );


  /* other ways to display all command-line args... */
  for ( int i = 0 ; *(argv+i) != NULL ; i++ )
  {
    printf( "*(argv+%d) is %s\n", i, *(argv+i) );
  }


  for ( char ** ptr = argv ; *ptr ; ptr++ )
  {
    printf( "next arg is %s\n", *ptr );
  }

  return EXIT_SUCCESS;
}

#if 0
                   char*
                 +-------+
   argv ---> [0] |   ========>"./a.out" (array of char with '\0')
                 +-------+
             [1] |   ========>"abcd"
                 +-------+
             [2] |   ========>"1234"
                 +-------+
             [3] |   ========>"xyz"
                 +-------+
             [4] | NULL  |     argv[argc] is always NULL
                 +-------+
#endif
