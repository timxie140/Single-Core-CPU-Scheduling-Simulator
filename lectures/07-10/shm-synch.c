/* shm-synch.c */

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

/* TO DO: can you scale this up to have multiple child processes? */

/* TO DO: can you scale this up to have multiple readers...? */

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
  /* create the shared memory segment with a size of 8 bytes */
  key_t key = SHM_SHARED_KEY;
  int shmid = shmget( key, 2 * sizeof( int ), IPC_CREAT | IPC_EXCL | 0660 );
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

  if ( p == 0 )
  {
    printf( "CHILD: writing my pid %d to shared memory...\n", getpid() );
    *data = getpid();

    /* notify the parent/reader process that the data is not valid */
    *(data + 1) = 1;

    while ( *(data + 1) == 1 ) { /* nop */ }

#if 0
    sleep( 30 );
#endif
    printf( "CHILD: writing 1234 to shared memory...\n" );
    *data = 1234;

    /* notify the parent/reader process that the data is not valid */
    *(data + 1) = 1;
  }

  if ( p > 0 )
  {
    while ( *(data + 1) == 0 ) { /* nop */ }

    printf( "PARENT: shared memory contains %d\n", *data );

    /* notify the child/writer process that it is okay to write new data */
    *(data + 1) = 0;

    while ( *(data + 1) == 0 ) { /* nop */ }

    printf( "PARENT: shared memory contains %d\n", *data );
  }


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