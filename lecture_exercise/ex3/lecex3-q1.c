#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ipc.h> 
#include <sys/shm.h> 
#include <ctype.h>
#include <string.h> 

int lecex3_q1_child( int pipefd ){
    int shmid, shmsize, shmkey;
    
    /* Reading shared memory key and size from pipe */
    if(read(pipefd, &shmkey, sizeof(int)) == -1){
        perror("Error in reading shmid from pipe");
        return EXIT_FAILURE;
    }
    if(read(pipefd, &shmsize, sizeof(int)) == -1){
        perror("Error in reading size from pipe");
        return EXIT_FAILURE;
    }

    shmid = shmget(shmkey, shmsize, 0666);
    
    /* Attach to the shared memory segment */
    char *str = (char*) shmat(shmid, NULL, 0);
    if(str == (char*)-1){
        perror("Error in attaching to shared memory");
        return EXIT_FAILURE;
    }

    /* Convert all lowercase letters to uppercase */
    for(int i = 0; i < shmsize; i++){
        if (isalpha(*(str + i))){
            *(str + i) = toupper(*(str + i));
        }
    }

    /* Detach from shared memory */
    if(shmdt(str) == -1){
        perror("Error in detaching from shared memory");
        return EXIT_FAILURE;
    }
    
    /* Exit the child process */
    exit(EXIT_SUCCESS);
}
