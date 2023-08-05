/* signals.c */

/* TO DO: check out "man 2 signal" and "man 7 signal" */

/* THIS IS USEFUL FOR HOMEWORK 3 !!! */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void signal_handler( int sig )
{
  printf( "Rcvd signal %d\n", sig );

  if ( sig == SIGINT )
  {
    printf( "Stop hitting CTRL-C and answer the question!\n" );
  }
  else if ( sig == SIGTERM )
  {
    printf( "Sorry, I'm not shutting down.\n" );
  }
  else if ( sig == SIGUSR1 )
  {
    printf( "Okay...reloading my config file....\n" );
  }
}

int main()
{
  char name[128];
  printf( "Enter your name: " );
  scanf( "%s", name );   /* BUFFER OVERFLOW POSSIBLE HERE... */
  printf( "Hi, %s\n", name );

  signal( SIGINT, SIG_IGN );   /* ignore SIGINT (CTRL-C) */
  signal( SIGTERM, SIG_IGN );  /* ignore SIGTERM */

  /* redefine SIGINT to call signal_handler() */
  signal( SIGINT, signal_handler );

  /* redefine SIGTERM to call signal_handler() */
  signal( SIGTERM, signal_handler );

  /* redefine SIGUSR1 to call signal_handler() */
  signal( SIGUSR1, signal_handler );

  printf( "Enter your name: " );
  scanf( "%s", name );   /* BUFFER OVERFLOW POSSIBLE HERE... */
  printf( "Hi, %s\n", name );

  /* restore SIGINT (CTRL-C) to default behavior -- see signal(7) */
  signal( SIGINT, SIG_DFL );

  /* etc. */

  return EXIT_SUCCESS;
}