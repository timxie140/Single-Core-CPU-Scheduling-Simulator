#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>

int lecex2_child(int n) {
    int fd = open("lecex2.txt", O_RDONLY);
    if (fd == -1) {
        fprintf(stderr, "Error opening file: lecex2.txt\n");
        abort();
    }

    lseek(fd, n - 1, SEEK_SET);

    char ch;
    int bytes_read = read(fd, &ch, sizeof(char));
    if (bytes_read == 0) {
        fprintf(stderr, "Error reading from file\n");
        close(fd);
        abort();
    }

    close(fd);
    exit(ch);
}

int lecex2_parent() {
    int child_status;
    waitpid(-1, &child_status, 0);

    if (WIFEXITED(child_status)) {
        int exit_status = WEXITSTATUS(child_status);
        printf("PARENT: child process successfully returned '%c'\n", (char)exit_status);
        return EXIT_SUCCESS;
    } else {
        printf("PARENT: oh no, child process terminated abnormally!\n");
        return EXIT_FAILURE;
    }
}
