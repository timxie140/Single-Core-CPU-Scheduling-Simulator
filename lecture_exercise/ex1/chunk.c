#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

int main(int argc, char** argv) {
    if (argc != 3) {
        printf("Usage: ./a.out n filename\n");
        return 1;
    }

    int n = atoi(*(argv + 1));
    char* filename = *(argv + 2);

    int FILE = open(filename, O_RDONLY);
    if (FILE == -1) {
        perror("Error opening file");
        return 1;
    }

    char* buffer = (char*)malloc((n + 1) * sizeof(char));

    int offset = 0;
    int bytes_read;
    int count = 0;
    int print_delimiter = 0;

    while ((bytes_read = read(FILE, buffer, n)) > 0) {
        if (count % 2 == 0) {
            *(buffer + bytes_read) = '\0'; 
            if (print_delimiter) {
                printf("|");
            }
            printf("%s", buffer);
            print_delimiter = 1; 
        }
        count++;
        offset += n;
        lseek(FILE, offset, SEEK_SET);
    }

    printf("\n");

    free(buffer);
    close(FILE);

    return 0;
}
