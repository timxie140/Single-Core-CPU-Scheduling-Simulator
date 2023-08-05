/* fd-write.c */

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
  char * name = "outfile.txt";

                   /* attempt to open this file:
                       O_WRONLY for writing
                       O_CREAT create the file if necessary
                       O_TRUNC truncate the file if it already exists
                              (i.e., erase the contents, set size to 0)
                       (also O_APPEND) */

  int fd = open( name, O_WRONLY | O_CREAT | O_TRUNC, 0660 );
             /*                                      ^^^^
                                                      |
                                      leading 0 means this is in octal
                                                               (base 8)
                0660 ==> 110 110 000
                         rwx rwx rwx
                         ^^^ ^^^ ^^^
                          |   |   |
                          |   |  no permissions for other/world
                          |   |
                          | rw for group permissions
                          |
                     rw for file owner */

  if ( fd == -1 )
  {
    perror( "open() failed" );
    return EXIT_FAILURE;
  }

  printf( "fd is %d\n", fd );

  /* fd table:
   *   0 stdin
   *   1 stdout
   *   2 stderr
   *   3 outfile.txt (O_WRONLY)
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