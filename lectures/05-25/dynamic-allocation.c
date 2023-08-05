/* dynamic-allocation.c */

/* compile from terminal/shell with -g option as follows:
 *
 *   bash$ gcc -Wall -Werror -g dynamic-allocation.c -lm
 *
 *
 * this enables valgrind to show line numbers of where memory errors occur:
 *
 *   bash$ valgrind ./a.out
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main()
{
  /* dynamically allocate 16 bytes on the runtime heap */
  char * path = malloc( 16 );

  if ( path == NULL )
  {
    perror( "malloc() failed" );
    return EXIT_FAILURE;
  }

  char * path2 = malloc( 16 );

  if ( path2 == NULL )
  {
    perror( "malloc() failed" );
    return EXIT_FAILURE;
  }

  printf( "sizeof path is %lu\n", sizeof( path ) );
  printf( "sizeof path2 is %lu\n", sizeof( path2 ) );

  strcpy( path, "/cs/goldsd/u23/" );
  printf( "path is \"%s\" (strlen is %lu)\n", path, strlen( path ) );

  strcpy( path2, "ABCDEFGHIJKLMNOP" );  /* one-byte overflow */
  printf( "path2 is \"%s\" (strlen is %lu)\n", path2, strlen( path2 ) );

  strcpy( path2, "/cs/goldsd/u23/blah/BLAH/blAh/blaH/meme" );
  printf( "path is \"%s\" (strlen is %lu)\n", path, strlen( path ) );
  printf( "path2 is \"%s\" (strlen is %lu)\n", path2, strlen( path2 ) );

  free( path );
  free( path2 );

  return EXIT_SUCCESS;
}
