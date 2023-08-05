/* fifo-writer.c */

/* man 7 pipe ; man 3 mkfifo */

/* A "pipe" is a unidirectional communication channel -- man 2 pipe */
/*               ^^^                                                */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main()
{
  char * fifo = "/tmp/fifo1234";

  int rc = mkfifo( fifo, 0660 );
  if ( rc == -1 )
  {
    perror( "mkfifo() failed" );
    return EXIT_FAILURE;
  }

  printf( "Created fifo at %s\n", fifo );


  int fd = open( fifo, O_WRONLY );
  if ( fd == -1 )
  {
    perror( "open() failed" );
    return EXIT_FAILURE;
  }

  /* fd table:

     0: stdin
     1: stdout                   IN MEMORY:
     2: stderr                   +--------+
     3: fd =========WRITE=======>| buffer |   /tmp/fifo1234
                                 | buffer |
                                 +--------+
   */

  printf( "Opened fifo %s on fd %d for writing\n", fifo, fd );

  /* write data to the fifo */
  int bytes_written = write( fd, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 26 );

  if ( bytes_written == -1 )
  {
    perror( "write() failed on the fifo" );
    return EXIT_FAILURE;
  }

  printf( "Wrote %d bytes\n", bytes_written );

  sleep( 10 );

  /* write more data to the fifo */
  bytes_written = write( fd, "abcdefghijklmnopqrstuvwxyz", 26 );

  if ( bytes_written == -1 )
  {
    perror( "write() failed on the fifo" );
    return EXIT_FAILURE;
  }

  printf( "Wrote %d bytes\n", bytes_written );

  sleep( 10 );

  close( fd );


  printf( "marking this FIFO for deletion...\n" );

  /* mark the fifo for deletion now that we are done with it... */
  rc = unlink( fifo );
  if ( rc == -1 )
  {
    perror( "unlink() failed" );
    return EXIT_FAILURE;
  }

  return EXIT_SUCCESS;
}