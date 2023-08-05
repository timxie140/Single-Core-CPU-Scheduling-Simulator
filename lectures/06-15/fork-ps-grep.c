/* fork-ps-grep.c */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

/* use fork(), pipe(), and execl() to execute:
 *
 *   ps -ef | grep goldsd
 *
 */

int main()
{
  pid_t p1, p2;   /* process ids (pids) for two child processes */

  int pipefd[2];
  int rc = pipe( pipefd );
  if ( rc == -1 )
  {
    perror( "pipe() failed" );
    return EXIT_FAILURE;
  }

  /* fd table:
   *
   *  0: stdin
   *  1: stdout
   *  2: stderr                  +--------+
   *  3: pipefd[0] <====READ=====| buffer | think of this buffer as a
   *  4: pipefd[1] =====WRITE===>| buffer |  temporary hidden file...
   *                             +--------+
   */

  printf( "PARENT: going to create the first child process...\n" );

  /* create a new (child) process for ps */
  p1 = fork();

  if ( p1 == -1 )
  {
    perror( "fork() failed" );
    return EXIT_FAILURE;
  }

  if ( p1 == 0 )   /* first CHILD process (ps) executes here... */
  {
    printf( "CHILD: going to execute the ps command...\n" );

    close( pipefd[0] );    /* close the read end of the pipe */
    dup2( pipefd[1], 1 );  /* redirect stdout to the write end of the pipe */
    close( pipefd[1] );    /* since we now have two descriptors referencing
                            *  the write end of the pipe, close fd 4 since
                            *   ps won't use it...
                            */
  /* fd table:
   *
   *  0: stdin                   +--------+
   *  1: pipefd[1] =====WRITE===>| buffer |
   *  2: stderr                  +--------+
   */

    execl( "/usr/bin/ps", "ps", "-ef", NULL );
    perror( "execl() failed" );
    return EXIT_FAILURE;
  }


  printf( "PARENT: moving on to the second child process...\n" );

  /* create a new (child) process for grep */
  p2 = fork();

  if ( p2 == -1 )
  {
    perror( "fork() failed" );
    return EXIT_FAILURE;
  }

  if ( p2 == 0 )   /* second CHILD process (grep) executes here... */
  {
    printf( "CHILD: going to execute the grep command...\n" );

    close( pipefd[1] );    /* close the write end of the pipe */
    dup2( pipefd[0], 0 );  /* redirect stdin to the read end of the pipe */
    close( pipefd[0] );    /* since we now have two descriptors referencing
                            *  the read end of the pipe, close fd 3 since
                            *   grep won't use it...
                            */

  /* fd table:
   *                             +--------+
   *  0: pipefd[0] <====READ=====| buffer |
   *  1: stdout                  +--------+
   *  2: stderr
   */

    execl( "/usr/bin/grep", "grep", "goldsd", NULL );
    perror( "execl() failed" );
    return EXIT_FAILURE;
  }


  /* fd table:      (BACK IN THE PARENT PROCESS)
   *
   *  0: stdin
   *  1: stdout
   *  2: stderr                  +--------+
   *  3: pipefd[0] <====READ=====| buffer | think of this buffer as a
   *  4: pipefd[1] =====WRITE===>| buffer |  temporary hidden file...
   *                             +--------+
   */

#if 1
  close( pipefd[0] );  /* close the read end of the pipe */
  close( pipefd[1] );  /* close the write end of the pipe */
#endif

  /* fd table:      (BACK IN THE PARENT PROCESS)
   *
   *  0: stdin
   *  1: stdout
   *  2: stderr
   */

  int status;
  pid_t child_pid;

  child_pid = waitpid( p1, &status, 0 );   /* BLOCKING */

  printf( "PARENT: child process %d (ps) terminated...\n", child_pid );

  if ( WIFSIGNALED( status ) )  /* child process was terminated   */
  {                             /*  by a signal (e.g., seg fault) */
    printf( "PARENT: ...abnormally (killed by a signal)\n" );
  }
  else if ( WIFEXITED( status ) )
  {
    int exit_status = WEXITSTATUS( status );
    printf( "PARENT: ...successfully with exit status %d\n", exit_status );
  }


  child_pid = waitpid( p2, &status, 0 );   /* BLOCKING */

  printf( "PARENT: child process %d (grep) terminated...\n", child_pid );

  if ( WIFSIGNALED( status ) )  /* child process was terminated   */
  {                             /*  by a signal (e.g., seg fault) */
    printf( "PARENT: ...abnormally (killed by a signal)\n" );
  }
  else if ( WIFEXITED( status ) )
  {
    int exit_status = WEXITSTATUS( status );
    printf( "PARENT: ...successfully with exit status %d\n", exit_status );
  }

  return EXIT_SUCCESS;
}
