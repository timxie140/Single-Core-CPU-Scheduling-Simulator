/* delay.c */

/* run this in the background:
 *
 * bash$ ./a.out &
 * [1] 2048498    <== job number (in terminal) and PID
 * bash$
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

int main( int argc, char ** argv )
{
  printf( "PID %d: argc is %d\n", getpid(), argc );

  printf( "PID %d: My parent process is PID %d\n", getpid(), getppid() );
  printf( "PID %d: Calculating something very important...\n", getpid() );

  sleep( 30 );

  printf( "PID %d: All done --- terminating...\n", getpid() );

  return EXIT_SUCCESS;
}