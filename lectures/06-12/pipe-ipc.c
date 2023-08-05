/* pipe-ipc.c */

/* A "pipe" is a unidirectional communication channel -- man 2 pipe */
/*               ^^^                                                */

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


  /* fork() will copy the fd table to the child process */
  pid_t p = fork();

  if ( p == -1 )
  {
    perror( "fork() failed" );
    return EXIT_FAILURE;
  }

  /* fd table:
   *
   *  <<PARENT>>                                       <<CHILD>>
   *  0: stdin                                         0: stdin
   *  1: stdout                                        1: stdout
   *  2: stderr                  +--------+            2: stderr
   *  3: pipefd[0] <====READ=====| buffer |===READ===> 3: pipefd[0]
   *  4: pipefd[1] =====WRITE===>| buffer |<==WRITE=== 4: pipefd[1]
   *                             +--------+
   */

  /* fd table (AFTER the two close() calls below):
   *
   *  <<PARENT>>                                       <<CHILD>>
   *  0: stdin                                         0: stdin
   *  1: stdout                                        1: stdout
   *  2: stderr                  +--------+            2: stderr
   *  3: pipefd[0] <====READ=====| buffer |            3:
   *  4:                         | buffer |<==WRITE=== 4: pipefd[1]
   *                             +--------+
   */

  if ( p == 0 )  /* CHILD PROCESS */
  {
    close( pipefd[0] );  /* close the read end of the pipe */

    /* write data to the pipe */
    int bytes_written = write( pipefd[1], "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 26 );
/* <----------context-switch from child to parent...----------------------> */
    printf( "CHILD: Wrote %d bytes to the pipe\n", bytes_written );
  }
  else  /* p > 0 --- PARENT PROCESS */
  {
    close( pipefd[1] );  /* close the write end of the pipe */

#if 0
usleep( 10 );
#endif
    /* read data from the pipe */
    char buffer[20];
    int bytes_read = read( pipefd[0], buffer, 10 );
    buffer[bytes_read] = '\0';   /* assume character data */
    printf( "PARENT: Read %d bytes: \"%s\"\n", bytes_read, buffer );

    bytes_read = read( pipefd[0], buffer, 10 );
    buffer[bytes_read] = '\0';   /* assume character data */
    printf( "PARENT: Read %d bytes: \"%s\"\n", bytes_read, buffer );

    bytes_read = read( pipefd[0], buffer, 10 );
    buffer[bytes_read] = '\0';   /* assume character data */
    printf( "PARENT: Read %d bytes: \"%s\"\n", bytes_read, buffer );
  }

  usleep( 10000 );

  return EXIT_SUCCESS;
}

/* TO DO: What are all possible outputs of this code?
 *
 * TO DO: Test what happens when we call read() a 4th time, etc.
 *         in the parent process...
 */


