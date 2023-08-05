/* buffering.c */

/* When printing to the terminal (shell) via stdout (fd 1),
 *  a '\n' character will "flush" the stdout buffer,
 *   i.e., output everything that has been stored in
 *    the stdout buffer so far...
 *
 * ==> this is called line-based buffering
 *
 * TO DO (fix): add a '\n' to the end of each debugging printf()
 *
 * When we instead output fd 1 to a file...
 *
 *  bash$ ./a.out > STDOUT.txt
 *
 *  ...the '\n' character no longer flushes the stdout buffer
 *
 * ==> this is called block-based buffering
 *      (also referred to as fully buffered)
 *
 * Another approach is to use fflush(stdout) or fflush(NULL)
 *
 * A third type of buffering is non-buffered (unbuffered),
 *  which is what is used for stderr (fd 2)
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
printf( "HERE0" );      /* stdout buffer: "HERE0" */
  int * x = NULL;

fprintf( stderr, "crashing here?" );
printf( "HERE1" );      /* stdout buffer: "HERE0HERE1" */
  *x = 1234;

printf( "HERE2" );
  printf( "*x is %d\n", *x );

  return EXIT_SUCCESS;
}
