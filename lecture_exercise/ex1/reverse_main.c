#include "reverse.h"
#include <stdio.h>

int main() {
    char* input = "I'm Tim Xie";
    char* reversed = reverse(input);

    printf("Reversed string: %s\n", reversed);
    free(reversed);
    return 0;
}
