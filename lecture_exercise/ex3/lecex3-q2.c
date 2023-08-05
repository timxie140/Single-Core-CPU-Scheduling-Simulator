#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ipc.h> 
#include <sys/shm.h> 
#include <ctype.h>
#include <string.h> 
#include <pthread.h>

void * copy_file( void * arg );

int main (int argc, char **argv) {
    int num_files = argc - 1;
    int total_bytes = 0;
    pthread_t *threads = calloc(num_files, sizeof(pthread_t));
    if (threads == NULL) {
        perror("calloc() failed");
        return EXIT_FAILURE;
    }

    int *rc = calloc(num_files, sizeof(int));
    if (rc == NULL) {
        perror("calloc() failed");
        return EXIT_FAILURE;
    }

    for (int i = 0; i < num_files; i++) {
        *(rc + i) = pthread_create(&*(threads + i), NULL, copy_file, *(argv + i + 1));
        if (*(rc + i) != 0) {
            perror("pthread_create() failed");
            return EXIT_FAILURE;
        }
        printf("MAIN: Creating thread to copy \"%s\"\n", *(argv + i + 1));
    }

    for (int i = 0; i < num_files; i++) {
        int *retval;
        *(rc + i) = pthread_join(*(threads + i), (void **)&retval);
        if (*(rc + i) != 0) {
            perror("pthread_join() failed");
            return EXIT_FAILURE;
        }
        printf("MAIN: Thread completed copying %d bytes for \"%s\"\n", *retval, *(argv + i + 1));
        total_bytes += *retval;
        free(retval);
    }

    if (num_files != 1) {
        printf("MAIN: Successfully copied %d bytes via %d child threads\n", total_bytes, num_files);
    }
    else {
        printf("MAIN: Successfully copied %d bytes via %d child thread\n", total_bytes, num_files);
    }
    free(threads);
    free(rc);

    return EXIT_SUCCESS;
}