/* static-allocation-buggy.c */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{                          /*       +---+---+---+---+---+----+ */
  char name[5] = "Dawid";  /* name: | D | a | w | i | d | \0 | */
                           /*       +---+---+---+---+---+----+ */
  name[2] = 'v';

  printf( "Hi, %s\n", name );

  char xyz[5] = "QRSTU";

  printf( "Hi again, %s\n", name );
  printf( "xyz is %s\n", xyz );

  /* TO DO: correct the bugs above by allocating [6] instead of [5] */
  /*        ...try different values, e.g., [3], [300], etc.?        */
  /* TO DO: can you make the code above seg-fault?                  */


#if 0
  char * cptr = "ABCdEFGHIJKLMNOPQRSTUVWXYZ";  /* implied '\0' at the end */
#endif

  char cptr[] = "ABCdEFGHIJKLMNOPQRSTUVWXYZ";  /* implied '\0' at the end */
  /* this "works" and lets the compiler figure out that we need 27 bytes */

  printf( "cptr points to \"%s\"\n", cptr );
  cptr[3] = 'D';  /* seg-fault occurs here because cptr points to read-only memory */
  printf( "cptr points to \"%s\"\n", cptr );


  return EXIT_SUCCESS;
}