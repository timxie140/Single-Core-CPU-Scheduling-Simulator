/* alarm-v3.c */

/* multi-threaded solution */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>

#define MAXLINE 80

typedef struct
{
  int seconds;
  char msg[MAXLINE];
} alarm_t;

/* function executed by each thread */
void * alarm_thread_function( void * arg )
{
  alarm_t * alarm = (alarm_t *)arg;

  pthread_t mytid = pthread_self();  /* get my thread ID */

  /* pthread_detach() enables pthreads to reclaim the
   *  thread resources when this thread terminates,
   *   i.e., do not leave a "zombie" thread behind
   */
  pthread_detach( mytid );

  printf( "Alarm set for %d seconds\n", alarm->seconds );
  sleep( alarm->seconds );
  fprintf( stderr, "ALARM (%d): %s\n", alarm->seconds, alarm->msg );

  free( alarm );  /* or free( arg ); */

  return NULL;
}


int main()
{
  const int maxline = 80;

  char * format_string = calloc( maxline, sizeof( char ) );
  sprintf( format_string, "%%d %%%d[^\n]", maxline - 1 );    /* "%d %79[^\n]" */

  char * line = calloc( maxline, sizeof( char ) );
  char * msg = calloc( maxline, sizeof( char ) );

  while ( 1 )
  {
    int seconds;

    printf( "Set alarm (<sec> <msg>) -- 0 to exit: " );

    if ( fgets( line, maxline - 1, stdin ) == NULL ) return EXIT_FAILURE;

    if ( strlen( line ) <= 1 ) continue;   /* skip blank lines */

    if ( sscanf( line, format_string, &seconds, msg ) < 2 || seconds < 0 )
    {
      if ( seconds == 0 ) break;
      fprintf( stderr, "ERROR: invalid alarm request\n" );
    }
    else
    {
      pthread_t tid;  /* thread ID */

#if 0
      /* create the next alarm */
      /* -- DO NOT DO THIS BC EACH THREAD ACCESSES THE SAME MEMORY */
      alarm_t alarm;
      alarm.seconds = seconds;
      strcpy( alarm.msg, msg );
      int rc = pthread_create( &tid, NULL, alarm_thread_function, &alarm );
#else
      /* dynamically allocate memory for the next alarm thread */
      alarm_t * alarm = malloc( sizeof( alarm_t ) );
      alarm->seconds = seconds;
      strcpy( alarm->msg, msg );

      int rc = pthread_create( &tid, NULL, alarm_thread_function, alarm );
#endif

      if ( rc != 0 )
      {
        fprintf( stderr, "ERROR: pthread_create() failed (%d): %s\n",
                 rc, strerror( rc ) );
        return EXIT_FAILURE;
      }

      usleep( 1000 );
    }
  }

  free( format_string );
  free( msg );
  free( line );

  return EXIT_SUCCESS;
}
