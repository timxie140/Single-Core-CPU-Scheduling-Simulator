/* threads-example.c */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define CHILDREN 8

/* this function is called by each thread */
void * whattodo( void * arg );

int main()
{
  pthread_t tid[CHILDREN];    /* keep track of thread IDs */

  int i, rc, children = CHILDREN;

  for ( i = 0 ; i < children ; i++ )
  {
#if 0
    int t;
    t = 10 + ( rand() % 21 );  /* [10,30] seconds */
    printf( "MAIN: next child thread will nap for %d seconds\n", t );
    rc = pthread_create( &tid[i], NULL, whattodo, &t );
#else
    int * t = malloc( sizeof( int ) );
    *t = 10 + ( rand() % 21 );  /* [10,30] seconds */
    printf( "MAIN: next child thread will nap for %d seconds\n", *t );
    rc = pthread_create( &tid[i], NULL, whattodo, t );
#endif

    if ( rc != 0 )
    {
      fprintf( stderr, "pthread_create() failed (%d)\n", rc );
    }
  }

  /* wait for the child threads to terminate */
  for ( i = 0 ; i < CHILDREN ; i++ )
  {
#if 0
    pthread_join( tid[i], NULL );  /* BLOCKING CALL */
    printf( "MAIN: joined a child thread\n" );
#else
    int * retval;
    pthread_join( tid[i], (void **)&retval );  /* BLOCKING CALL */
    printf( "MAIN: joined a child thread that returned %d\n", *retval );
    free( retval );
#endif
  }

  printf( "MAIN: all child threads successfully joined\n" );

  return EXIT_SUCCESS;
}


void * whattodo( void * arg )
{
  int t = *(int *)arg;
  free( arg );

  printf( "I'm going to nap for %d seconds...\n", t );
  sleep( t );
  printf( "I'm awake!\n" );

  /* dynamically allocate memory to hold the return value from this thread */
  int * return_value = malloc( sizeof( int ) );
  *return_value = t;

  /* terminate this child thread and return the return_value pointer */
  pthread_exit( return_value );
}
