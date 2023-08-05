/* fork-multi-child.c */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>

int child();
void parent( int children, pid_t * pids );

int main( int argc, char ** argv )
{
  if ( argc != 2 )
  {
    fprintf( stderr, "ERROR: invalid arguments\n" );
    return EXIT_FAILURE;
  }

  int children = atoi( *(argv + 1) );

  /* TO DO: make sure the input from the user is not too large...
   *         ...possibly compare against RLIMIT_NPROC (rlimit.c)
   */

  pid_t * pids = calloc( children, sizeof( pid_t ) );

  if ( pids == NULL )
  {
    perror( "calloc() failed" );
    return EXIT_FAILURE;
  }

  for ( int i = 0 ; i < children ; i++ )
  {
    pid_t rc = fork();

    if ( rc == -1 )
    {
      perror( "fork() failed" );
      return EXIT_FAILURE;
    }

    if ( rc == 0 )
    {
      free( pids );      /* child processes do not use this array... */
      exit( child() );   /* return child(); */
    }

    /* PARENT */
    *(pids + i) = rc;
  }

  parent( children, pids );  /* waitpid() etc. will be in parent() */

  free( pids );

  return EXIT_SUCCESS;
}


int child()  /* each child process will sleep for a short period of time... */
{
#if 0
  srand( time( NULL ) );
#else
  srand( time( NULL ) * getpid() * getpid() );
#endif

  int t = 10 + ( rand() % 21 );  /* [10,30] seconds */
  printf( "CHILD %d: I'm gonna nap for %d seconds\n", getpid(), t );
  sleep( t );
  printf( "CHILD %d: I'm awake!\n", getpid() );
  return t;
}


/* TO DO: think of using the pids array for waitpid() instead of -1 ... */
void parent( int children, pid_t * pids )
{
  int status;  /* exit status from each child process */

  printf( "PARENT: I'm waiting for my child processes to wake up\n" );

  while ( children > 0 )
  {
    pid_t child_pid = waitpid( -1, &status, 0 );   /* BLOCKING CALL */
    /*                         ^^
     *                       wait for any of my child processes...
     */

    children--;

    printf( "PARENT: child process %d terminated...", child_pid );

    if ( WIFSIGNALED( status ) )  /* child process was terminated   */
    {                             /*  by a signal (e.g., seg fault) */
      printf( "abnormally (killed by a signal)\n" );
    }
    else if ( WIFEXITED( status ) )
    {
      int exit_status = WEXITSTATUS( status );
      printf( "normally with exit status %d\n", exit_status );
    }
  }

  printf( "PARENT: All done!\n" );
}
