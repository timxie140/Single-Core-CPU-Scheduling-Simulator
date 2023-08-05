/* fd-write-redirect.c */

/* bash$ hexdump -C outfile.txt */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

typedef struct
{
  unsigned int rin;  /* e.g., 660000001 */
  char rcsid[16];    /* e.g., "goldsd3" */
}
student_t;

int main()
{
  close( 1 );   /* close file descriptor 1 (stdout) */

  /* fd table:
   *
   *  0: stdin
   *  1:
   *  2: stderr
   */

  char * name = "outfile.txt";

  int fd = open( name, O_WRONLY | O_CREAT | O_TRUNC, 0660 );

  if ( fd == -1 )
  {
    perror( "open() failed" );
    return EXIT_FAILURE;
  }

  printf( "fd is %d\n", fd );

  /* fd table:
   *
   *  0: stdin
   *  1: outfile.txt (O_WRONLY)
   *  2: stderr
   */

  char buffer[20];
  sprintf( buffer, "ABCD%02dEFGH", fd );
  int rc = write( fd, buffer, strlen( buffer ) );
  printf( "wrote %d bytes to fd %d\n", rc, fd );

#if 0
  int * x = NULL;
  *x = 1234;
#endif

  rc = write( fd, buffer, 3 );
  printf( "wrote %d bytes to fd %d\n", rc, fd );

  /* write some binary data to the file... */
  int important = 32768;
  rc = write( fd, &important, sizeof( int ) );
  printf( "wrote %d bytes to fd %d\n", rc, fd );

  short q = 0xfade;
  rc = write( fd, &q, sizeof( short ) );
  printf( "wrote %d bytes to fd %d\n", rc, fd );

  student_t s1;
  s1.rin = 660000001;
  strcpy( s1.rcsid, "goldsd3" );
  rc = write( fd, &s1, sizeof( student_t ) );
  printf( "wrote %d bytes to fd %d\n", rc, fd );

  return EXIT_SUCCESS;
}


