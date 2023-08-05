/* fork-with-waitpid.c */

/* man 7 signal */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

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

    sleep( 6 );

#if 0
    int * q = NULL;
    *q = 1234;
#endif

    return 0xffff;  /* this is not returning 65535; instead, return 255 */
#if 0
    return 0x0c;
    return 12;
    return EXIT_SUCCESS;
#endif
  }
  else /* p > 0 --- PARENT PROCESS */
  {
#if 0
    sleep( 30 );
#endif

    printf( "PARENT: my new child process PID is %d.\n", p );
    printf( "PARENT: my PID is %d.\n", getpid() );

    /* Wait (BLOCK) for my child process to complete/terminate */
    int status;
    pid_t child_pid = waitpid( p, &status, 0 );   /* BLOCKING */

    printf( "PARENT: child process %d terminated...\n", child_pid );

    if ( WIFSIGNALED( status ) ) /* child process was terminated   */
    {                            /*  by a signal (e.g., seg fault) */
      printf( "PARENT: ...abnormally (killed by a signal)\n" );
    }
    else if ( WIFEXITED( status ) )
    {
      int exit_status = WEXITSTATUS( status );
      printf( "PARENT: ...normally with exit status %d\n", exit_status );
    }

#if 0
    sleep( 30 );
#endif
  }

  usleep( 10000 ); /* <== add this so that the bash prompt delays printing */

  return EXIT_SUCCESS;
}