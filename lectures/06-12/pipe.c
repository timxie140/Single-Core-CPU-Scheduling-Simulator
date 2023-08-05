/* pipe.c */

/* A "pipe" is a unidirectional communication channel -- man 2 pipe */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
  int pipefd[2];  /* array to hold the two pipe (file) descriptors:
                   *  pipefd[0] is the "read" end of the pipe
                   *  pipefd[1] is the "write" end of the pipe
                   */

  /* create a pipe */
  int rc = pipe( pipefd );

  if ( rc == -1 )
  {
    perror( "pipe() failed" );
    return EXIT_FAILURE;
  }

  /* fd table:
   *
   *  0: stdin
   *  1: stdout
   *  2: stderr                  +--------+
   *  3: pipefd[0] <====READ=====| buffer | think of this buffer as a
   *  4: pipefd[1] =====WRITE===>| buffer |  temporary hidden file...
   *                             +--------+
   */

  printf( "Created pipe: pipefd[0] is %d and pipefd[1] is %d\n",
          pipefd[0], pipefd[1] );

  /* write data to the pipe */
  int bytes_written = write( pipefd[1], "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 26 );
  printf( "Wrote %d bytes to the pipe\n", bytes_written );


  /* read data from the pipe */
  char buffer[20];
  int bytes_read = read( pipefd[0], buffer, 10 );
  buffer[bytes_read] = '\0';   /* assume character data */
  printf( "Read %d bytes: \"%s\"\n", bytes_read, buffer );

  bytes_read = read( pipefd[0], buffer, 10 );
  buffer[bytes_read] = '\0';   /* assume character data */
  printf( "Read %d bytes: \"%s\"\n", bytes_read, buffer );

  bytes_read = read( pipefd[0], buffer, 10 );
  buffer[bytes_read] = '\0';   /* assume character data */
  printf( "Read %d bytes: \"%s\"\n", bytes_read, buffer );

#if 0
  /* at this point, the pipe is empty...
   * ...so this next read() call below will BLOCK indefinitely (forever)
   *  because there's no data on the pipe --- and there is at least
   *   one active/open "write" descriptor on the pipe
   */
  bytes_read = read( pipefd[0], buffer, 10 );
  buffer[bytes_read] = '\0';   /* assume character data */
  printf( "Read %d bytes: \"%s\"\n", bytes_read, buffer );
#endif

  close( pipefd[1] );  /* close the write end of the pipe */

  /* fd table:
   *
   *  0: stdin
   *  1: stdout
   *  2: stderr                  +--------+
   *  3: pipefd[0] <====READ=====| buffer | think of this buffer as a
   *  4:                         | buffer |  temporary hidden file...
   *                             +--------+
   */

  bytes_read = read( pipefd[0], buffer, 10 );
  buffer[bytes_read] = '\0';   /* assume character data */
  printf( "(after write end is closed) Read %d bytes: \"%s\"\n",
          bytes_read, buffer );

  bytes_read = read( pipefd[0], buffer, 10 );
  buffer[bytes_read] = '\0';   /* assume character data */
  printf( "(after write end is closed) Read %d bytes: \"%s\"\n",
          bytes_read, buffer );


  close( pipefd[0] );  /* close the read end of the pipe */

  /* fd table:
   *
   *  0: stdin
   *  1: stdout
   *  2: stderr                  +--------+
   *  3:                         | buffer | the OS deletes this buffer
   *  4:                         | buffer |
   *                             +--------+
   */

  bytes_read = read( pipefd[0], buffer, 10 );
  printf( "bytes_read is %d\n", bytes_read );

  if ( bytes_read == -1 )
  {
    perror( "read() failed" );
    return EXIT_FAILURE;
  }

  /* bytes_read is now -1 (error) because pipefd[0] is no longer valid */

  return EXIT_SUCCESS;
}


/* TO DO: what would happen if we swapped the order of the close()
 *         calls above...?
 */




