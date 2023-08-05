/* shm-count.c */

/* create a shared memory segment, then create a child process
 *  such that both parent and child are attached to the shared memory
 */

/* you can use the shell to view/remove shared memory segments as follows:
 *
 *  bash$ ipcs
 *  bash$ ipcs -m
 *
 * and this will remove all shared memory segments:
 *
 *   bash$ ipcrm -a
 */

/* TO DO: write a separate program to attach to this shared memory segment... */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <sys/wait.h>

#define SHM_SHARED_KEY 8999

int main()
{
  /* create the shared memory segment with a size of 4 bytes */
  key_t key = SHM_SHARED_KEY;
  int shmid = shmget( key, sizeof( int ), IPC_CREAT | IPC_EXCL | 0660 );
                                                               /* rw-rw---- */

  /* When created, the shared memory segment is initialized to zeroes */

  if ( shmid == -1 )
  {
    perror( "shmget() failed" );
    return EXIT_FAILURE;
  }

  printf( "shmget() returned %d\n", shmid );


  /* attach to the shared memory segment */
  int * data = shmat( shmid, NULL, 0 );

  if ( data == (void *)-1 )   /* TO DO: why doesn't shmat() return NULL... */
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


  if ( p > 0 ) usleep( 1200 );  /* delay the parent process... */


  /* both parent and child processes will run the code below, */
  /*  both accessing (and changing) the shared memory segment */
  int i, stop = 10000;

  for ( i = 1 ; i <= stop ; i++ )
  {
    printf( "%s: adding %d\n", ( p > 0 ? "PARENT" : "CHILD" ), i );

    *data += i;
  }

  printf( "\n%s: Sum 1..%d is %d\n", p > 0 ? "PARENT" : "CHILD", stop, *data );



  /* detach from the shared memory segment */
  int rc = shmdt( data );

  if ( rc == -1 )
  {
    perror( "shmdt() failed" );
    return EXIT_FAILURE;
  }

#if 1
  if ( p > 0 )
  {
    printf( "PARENT: removing shared memory segment...\n" );

    /* remove the shared memory segment */
    if ( shmctl( shmid, IPC_RMID, 0 ) == -1 )
    {
      perror( "shmctl() failed" );
      return EXIT_FAILURE;
    }
  }
#endif

  usleep( 10000 );

  return EXIT_SUCCESS;
}
