/* alarm-v2.c */

/* multi-process solution */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

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
      pid_t p = fork();

      if ( p == -1 ) { perror( "fork() failed" ); return EXIT_FAILURE; }

      if ( p == 0 )
      {
        /* TO DO: fix the memory leaks in the child process... */
        printf( "Alarm set for %d seconds\n", seconds );
        sleep( seconds );
        fprintf( stderr, "ALARM (%d): %s\n", seconds, msg );
        exit( EXIT_SUCCESS );
      }

      /* TO DO: add waitpid() with the WNOHANG option... */
      usleep( 1000 );
    }
  }

  free( format_string );
  free( msg );
  free( line );

  return EXIT_SUCCESS;
}
