/* shm-string.c */

/* create a shared memory segment, then create a child process
    such that both parent and child are attached to the shared memory */

/* TO DO: write a separate program to attach to this shared memory segment */

/* you can use the shell to view/remove shared memory segments as follows:
 *
 *  bash$ ipcs
 *  bash$ ipcs -m
 *
 * this will remove all shared memory segments:
 *
 *   bash$ ipcrm -a
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <termios.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <sys/wait.h>

/* This constant defines the shared memory segment such that
   multiple processes can attach to this segment */
#define SHM_SHARED_KEY 8999

int main()
{
  struct termios ttyraw, ttyrestore;

  /* if stdin is a terminal/shell, switch to raw mode to avoid buffering */
  if ( isatty( STDIN_FILENO ) )
  {
    tcgetattr( STDIN_FILENO, &ttyrestore );
    cfmakeraw( &ttyraw );
    tcsetattr( STDIN_FILENO, TCSANOW, &ttyraw );
  }


  /* create the shared memory segment with a size of 16 bytes */
  key_t key = SHM_SHARED_KEY;
  int shmid = shmget( key, 16, IPC_CREAT | IPC_EXCL | 0660 );

  if ( shmid == -1 )
  {
    perror( "shmget() failed" );
    return EXIT_FAILURE;
  }


  /* attach to the shared memory segment */
  char * data = shmat( shmid, NULL, 0 );

  if ( data == (void *)-1 )
  {
    perror( "shmat() failed" );
    return EXIT_FAILURE;
  }


  /* create a child process */
  int p = fork();

  if ( p == -1 )
  {
    perror( "fork() failed" );
    return EXIT_FAILURE;
  }

  if ( p == 0 )
  {
    printf( "\rCHILD: type some characters (enter '!' to end)\n" );

    int c;
    char * ptr = data;

    do
    {
      printf( "\r" );
      c = getchar();
      *ptr = c;
      ptr++;
    }
    while ( c != '!' );
  }


  if ( p > 0 )
  {
    while ( 1 )
    {
      printf( "\rPARENT: shared memory contains \"%s\"\n", data );
      sleep( 1 );
      if ( waitpid( p, NULL, WNOHANG ) > 0 ) break;
    }

    printf( "\rPARENT: all done\n" );

    /* detach from the shared memory segment */
    int rc = shmdt( data );

    if ( rc == -1 )
    {
      perror( "shmdt() failed" );
      exit( EXIT_FAILURE );
    }

    /* remove the shared memory segment */
    if ( shmctl( shmid, IPC_RMID, 0 ) == -1 )
    {
      perror( "shmctl() failed" );
      exit( EXIT_FAILURE );
    }
  }

  if ( isatty( STDIN_FILENO ) )
  {
    tcsetattr( STDIN_FILENO, TCSANOW, &ttyrestore );
  }

  return EXIT_SUCCESS;
}
