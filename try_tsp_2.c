/* 
    A simple TSP solver.  Tries all possible combinations. 
    Not optimal.....
*/

#include	<stdio.h>
#include	<stdlib.h>
#include	<time.h>
#include	<unistd.h>
#include	<math.h>


/* #define NUM_CITIES	15 */
/* #define NUM_CITIES	12 */
#define NUM_CITIES	14


typedef struct {
        int x;
        int y;
} CITIES;


/* we are using too many global variables.... */
CITIES *cities = NULL;
long long factorial = 1;
double min_length = 1.0e38;


double calc_distance(int i, int j)
{
        return sqrt(pow(fabs(cities[i].x - cities[j].x), 2.0) + pow(fabs(cities[i].y - cities[j].y), 2.0));
}


CITIES *gen_cities(int how_many_cities, int min_x, int max_x, int min_y, int max_y)
{
        CITIES *ret;
        int i;


        ret = malloc(how_many_cities * sizeof(CITIES));
        if (ret == NULL) {
                fprintf(stderr, "Can't allocate in 'gen_cities()'\n");
                exit(1);
        }

        for (i = 0; i < how_many_cities; i++) {
                ret[i].x = min_x + (random() % (max_x - min_x));
                ret[i].y = min_y + (random() % (max_y - min_y));
        }

        return ret;
}

void    show_short_route(char *s, int curr_len, int *arr)
{
    int     i;

    printf("%s (%d)\n", s, curr_len);
    for (i = 0; i < NUM_CITIES; i++) {
            printf("(%d,%d)", cities[arr[i]].x, cities[arr[i]].y);
            if (i < (NUM_CITIES - 1)) {
                    printf("->");
            }
    }
    printf("->(%d,%d)\n", cities[arr[0]].x, cities[arr[0]].y);
}


/* called once per permutated item in arr */
void main_worker(int n, int *arr)
{
        int i;
        double current_length = 0.0;

        factorial--;

        if ((factorial % 1000000) == 0) {
                printf("remaining: %llu\n", factorial);
        }

        for (i = 0; i < (NUM_CITIES - 1); i++) {
                current_length += calc_distance(arr[i], arr[i + 1]);
        }
        /* close the circle... */
        current_length += calc_distance(arr[0], arr[NUM_CITIES - 1]);

        if (current_length < min_length) {
                min_length = current_length;

                show_short_route("new shortest way: ", min_length, arr);
        }
}


void walk_permutations(int n, int *arr, void (*func) (int n, int *arr))
{
        static int *c = NULL;
        int i;
        int x;

        if (c == NULL) {
                c = (int *) malloc(n * sizeof(int));
                if (c == NULL) {
                        fprintf(stderr, "Sorry, can't run.  Malloc() returns NULL\n");
                        exit(1);
                }
        }

        for (i = 0; i < n; i++) {
                c[i] = 0;
        }

        /* return arr;      *//* the first iteration */
        func(n, arr);

        i = 0;
        while (i < n) {
                if (c[i] < i) {
                        if ((i % 2) == 0) {
                                /* swap(arr[0], arr[i]) */
                                x = arr[0];
                                arr[0] = arr[i];
                                arr[i] = x;
                        } else {
                                /* swap(arr[c[i]], arr[i]) */
                                x = arr[c[i]];
                                arr[c[i]] = arr[i];
                                arr[i] = x;
                        }

                        /* return arr; */
                        func(n, arr);

                        c[i]++;
                        i = 0;
                } else {
                        c[i] = 0;
                        i++;
                }
        }
}


int main(void)
{
        int *arr = NULL;
        int i;

        for (i = 1; i < (NUM_CITIES + 1); i++) {
                factorial *= i;
        }
        printf("Factorial: %llu\n", factorial);

        srandom(time(NULL) ^ getpid() ^ (getppid() << 8));

        cities = gen_cities(NUM_CITIES, 0, 1000, 0, 1000);
        arr = malloc(NUM_CITIES * sizeof(int));

        for (i = 0; i < NUM_CITIES; i++) {
                arr[i] = i;
                printf("(%d, %d)\n", cities[i].x, cities[i].y);
        }

        walk_permutations(NUM_CITIES, &arr[0], main_worker);

        show_short_route("finally: ", min_length, arr);
}
