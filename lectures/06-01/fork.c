/* fork.c */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

int main()
{
  /* create a new (child) process */
  pid_t p = fork();

  if ( p == -1 )
  {
    perror( "fork() failed" );
    return EXIT_FAILURE;
  }

  if ( p == 0 ) /* CHILD PROCESS */
  {
    printf( "CHILD: happy birthday to me!  My PID is %d\n", getpid() );
    printf( "CHILD: my parent's PID is %d.\n", getppid() );
  }
  else /* p > 0 --- PARENT PROCESS */
  {
usleep( 50 );
    printf( "PARENT: my new child process PID is %d.\n", p );
    printf( "PARENT: my PID is %d.\n", getpid() );
  }

  usleep( 10000 ); /* <== add this so that the bash prompt delays printing */

  return EXIT_SUCCESS;
}

/*
 * goldsd@linux:~/u23/csci4210$ ./a.out
 * PARENT: my new child process PID is 2754682.
 * PARENT: my PID is 2754681.
 * CHILD: happy birthday to me!  My PID is 2754682.
 * CHILD: my parent's PID is 2754681.
 * goldsd@linux:~/u23/csci4210$ ./a.out
 * PARENT: my new child process PID is 2754684.
 * PARENT: my PID is 2754683.
 * CHILD: happy birthday to me!  My PID is 2754684.
 * CHILD: my parent's PID is 2754683.
 *
 * What are all possible outputs for this code?
 *
 *                                p = fork()
 *                                 /     \
 *                                /       \
 *                               /         \
 * PARENT: my new child process PID...    CHILD: happy birthday...
 * PARENT: my PID is ...                  CHILD: my parent's PID is ...
 *
 * (1) lines shown above in the <PARENT> section occur in that given order;
 *      same for <CHILD> section
 *
 * (2) lines shown above in the <PARENT> section could interleave with
 *      the lines shown in the <CHILD> section
 *
 *
 * goldsd@linux:~/u23/csci4210$ ./a.out
 * CHILD: happy birthday to me!  My PID is 2755920.
 * PARENT: my new child process PID is 2755920.
 * PARENT: my PID is 2755919.
 * CHILD: my parent's PID is 2755919.
 * goldsd@linux:~/u23/csci4210$ ./a.out
 * PARENT: my new child process PID is 2755922.
 * PARENT: my PID is 2755921.
 * CHILD: happy birthday to me!  My PID is 2755922.
 * CHILD: my parent's PID is 2755921.
 *
 * goldsd@linux:~/u23/csci4210$ ./a.out
 * CHILD: happy birthday to me!  My PID is 2795694
 * CHILD: my parent's PID is 2795693.
 * PARENT: my new child process PID is 2795694.
 * PARENT: my PID is 2795693.
 */