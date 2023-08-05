/* fork-with-exec.c */

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
                        /* argv[0], argv[1], argv[2],        argv[3] */
    execl( "/usr/bin/xyz", "ls",    "-l",    "nosuchfile.c", NULL );

                       /* argv[0], argv[1], argv[2],        argv[3] */
    execl( "/usr/bin/ls", "ls",    "-l",    "nosuchfile.c", NULL );

                   /* argv[0], argv[1] */
    execl( "./a.out", "a.out", NULL );        /* FORK BOMB! */

#endif
                       /* argv[0], argv[1], argv[2],    argv[3] */
    execl( "/usr/bin/ls", "ls",    "-l",    "rlimit.c", NULL );

    perror( "execl() failed" );
    return EXIT_FAILURE;
  }
  else /* p > 0 --- PARENT PROCESS */
  {
#if 0
    sleep( 30 );
#endif

    printf( "PARENT: my new child process PID is %d.\n", p );
    printf( "PARENT: my PID is %d.\n", getpid() );

    /* wait (BLOCK) for my child process to complete/terminate */
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
  }

  usleep( 10000 ); /* <== add this so that the bash prompt delays printing */

  return EXIT_SUCCESS;
}