#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>

int main() {
    int fd;
    int read_val;
    int status;

    pid_t pid = fork();

    

    if (pid == 0) { 
        //child process
        printf("PARENT: start here\n");
        
        fd = open("lecex2-q1-input.txt", O_RDONLY);
        if(fd < 0){
            perror("open");
            exit(EXIT_FAILURE);
        }
        printf("CHILD: opened lecex2-q1-input.txt\n");

        if(read(fd, &read_val, sizeof(int)) != sizeof(int)){
            perror("read");
            close(fd);
            exit(EXIT_FAILURE);
        }
        printf("CHILD: read an int\n");

        printf("CHILD: returning the int\n");
        close(fd);
        exit(read_val);
    } 
    else if (pid > 0) { 
        //parent process
        waitpid(pid, &status, 0);
        if(WIFEXITED(status)){
            printf("PARENT: heat in %d\n", WEXITSTATUS(status));
        } else {
            printf("PARENT: child process killed by a signal\n");
        }
        return WEXITSTATUS(status);
    } 
    else { // Fork failed
        printf("Fork failed!\n");
        return 1;
    }
}
