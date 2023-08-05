/* tcp-client.c */

#include <sys/types.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <strings.h>
#include <unistd.h>

#define MAXBUFFER 128

/* TO DO: Remove MAXBUFFER and use dynamic memory allocation */

int main()
{
  /* create TCP client socket (endpoint) */
  int sd = socket( AF_INET, SOCK_STREAM, 0 );
  if ( sd == -1 ) { perror( "socket() failed" ); exit( EXIT_FAILURE ); }

  struct hostent * hp = gethostbyname( "linux02.cs.rpi.edu" );

#if 0
  struct hostent * hp = gethostbyname( "128.113.126.39" );
  struct hostent * hp = gethostbyname( "localhost" );
  struct hostent * hp = gethostbyname( "127.0.0.1" );
#endif

  /* TO DO: rewrite the code above to use getaddrinfo() */

  if ( hp == NULL )
  {
    fprintf( stderr, "ERROR: gethostbyname() failed\n" );
    return EXIT_FAILURE;
  }

  struct sockaddr_in tcp_server;
  tcp_server.sin_family = AF_INET;  /* IPv4 */
  memcpy( (void *)&tcp_server.sin_addr, (void *)hp->h_addr, hp->h_length );
  unsigned short server_port = 8123;
  tcp_server.sin_port = htons( server_port );

  printf( "CLIENT: TCP server address is %s\n", inet_ntoa( tcp_server.sin_addr ) );

  printf( "CLIENT: connecting to server...\n" );

  if ( connect( sd, (struct sockaddr *)&tcp_server, sizeof( tcp_server ) ) == -1 )
  {
    perror( "connect() failed" );
    return EXIT_FAILURE;
  }


  /* The implementation of the application protocol is below... */

  char * msg = "why not change the world?";
  printf( "CLIENT: Sending to server: [%s]\n", msg );
  int n = write( sd, msg, strlen( msg ) );    /* or use send()/recv() */
  if ( n == -1 ) { perror( "write() failed" ); return EXIT_FAILURE; }

  char buffer[MAXBUFFER+1];
  n = read( sd, buffer, MAXBUFFER );    /* BLOCKING */

  if ( n == -1 )
  {
    perror( "read() failed" );
    return EXIT_FAILURE;
  }
  else if ( n == 0 )
  {
    printf( "CLIENT: rcvd no data; TCP server socket was closed\n" );
  }
  else /* n > 0 */
  {
    *(buffer + n) = '\0';
    printf( "CLIENT: rcvd from server: \"%s\"\n", buffer );
  }


  printf( "CLIENT: disconnecting...\n" );

  close( sd );

  return EXIT_SUCCESS;
}
