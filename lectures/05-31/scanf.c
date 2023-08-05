/* scanf.c */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <string.h>

int main()
{                       /*       [0]1 2 3 4  ...[15] */
                        /*       +-----------------+ */
  char * name;          /* name=>| | | | | | ... | | */
  name = malloc( 16 );  /*       +-----------------+ */

  printf( "Enter your name: " );

#if 0
  scanf( "%s", name );
  scanf( "%15s", name );
#endif

  /* attempt to read in the entire line of input... */
#if 0
  scanf( "%[^\n]s", name );
#endif

  char * rc = fgets( name, 16, stdin );

  if ( rc == NULL )
  {
    fprintf( stderr, "\nERROR: fgets() didn't work...\n" );
    return EXIT_FAILURE;
  }

  /* remove the trailing newline... */
  int len = strlen( name );
  if ( name[len-1] == '\n' ) name[len-1] = '\0';


  /*
   *  char * name;
   *  scanf( "%ms", &name );
   *   ...
   *  free( name );
   */

  printf( "Hello, %s\n", name );

  float x;
  printf( "Enter a number: " );
  scanf( "%f", &x );
  printf( "The square root of %f is %f\n", x, sqrt( x ) );

  free( name );

  return EXIT_SUCCESS;
}
