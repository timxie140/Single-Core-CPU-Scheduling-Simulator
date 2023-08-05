/* fifo-reader.c */

/* man 7 pipe ; man 3 mkfifo */

/* A "pipe" is a unidirectional communication channel -- man 2 pipe */
/*               ^^^                                                */

/* TO DO: we know we can look at the FIFO in the filesystem:
 *
 *   bash$ ls -l /tmp/fifo1234
 *   prw-rw---- 1 goldsd goldsd 0 Jun 15 11:21 /tmp/fifo1234
 *
 * Does the file size shown actually show how many bytes are
 *  on the fifo???
 *
 * Also, what if we do this (as the two processes are running...):
 *
 *   bash$ rm /tmp/fifo1234
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main()
{
  char * fifo = "/tmp/fifo1234";

  int fd = open( fifo, O_RDONLY );
  if ( fd == -1 )
  {
    perror( "open() failed" );
    return EXIT_FAILURE;
  }

  /* fd table:

     0: stdin
     1: stdout                   IN MEMORY:
     2: stderr                   +--------+
     3: fd <=========READ========| buffer |   /tmp/fifo1234
                                 | buffer |
                                 +--------+
   */

  printf( "Opened fifo %s on fd %d for reading\n", fifo, fd );

  while ( 1 )
  {
    /* read data from the fifo */
    char buffer[5];
    int bytes_read = read( fd, buffer, 4 );

    if ( bytes_read == -1 )
    {
      perror( "read() failed on the fifo" );
      return EXIT_FAILURE;
    }

    if ( bytes_read == 0 )
    {
      printf( "all done; writer process closed its write descriptor on the fifo\n" );
      break;
    }

    buffer[bytes_read] = '\0';
    printf( "Read %d bytes: \"%s\"\n", bytes_read, buffer );
  }

  close( fd );

  return EXIT_SUCCESS;
}