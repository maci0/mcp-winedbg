#include <stdio.h>

int main() {
    printf("Hello from the test application!\n");
    printf("PID: %d\n", getpid());
    printf("Press Enter to exit...\n");
    getchar();
    return 0;
}
