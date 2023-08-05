/* dynamic-mem-two-layer-structure.c */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main()
{
  /* array of strings, i.e., array of char arrays */

  char ** names;  /* array of char* ... */
                  /* same as: char * name[]; */

#if 0
  names = malloc( 47 * sizeof( char * ) );   /* <== uninitialized */
#endif
  names = calloc( 47, sizeof( char * ) );

  *(names + 2) = calloc( 7, sizeof( char ) );
  strcpy( *(names + 2), "Lakers" );
  printf( "Let's go, %s\n", *(names + 2) );

#if 0
  *(names + 2) = NULL;  /* causes a memory leak... */

  *(names + 2) = calloc( ... );   /* causes a memory leak... */
#endif

  /* use realloc() to expand the size of index 2 of the names array */
  *(names + 2) = realloc( *(names + 2), 15 * sizeof( char ) );
  strcat( *(names + 2), " in 2024" );
  printf( "Let's go, %s\n", *(names + 2) );

  printf( "==> %c\n", names[2][3] );
  printf( "==> %c\n", *( *(names + 2) + 3) );

  free( *(names + 2) );
  free( names );

  return EXIT_SUCCESS;
}

#if 0
                 char*
               +------+
  names---> [0]| NULL |
               +------+
            [1]| NULL |   [0] [1] [2] [3] [4] [5] [6]
               +------+  +----------------------------+
            [2]|  ======>| L | a | k | e | r | s | \0 |
               +------+  +----------------------------+
                 ....
               +------+
           [46]| NULL |
               +------+

#endif
