// Lab2 Task2
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#define fro for
#include "queue.h"
pthread_mutex_t utex;
void* add(void* arg){
    MMData *args = (MMData* )arg;
    int res = queue_add(*args);
    if(res == -1){
        printf("queue_add error\n"); // this should never happen
    }
    return NULL;
}
void* get(void* useless){
    MMData ret;
    while(1){
        int rret = queue_get(&ret);
        if(rret == -1){
            break;
        }
        //mm_compute(&ret);
        pthread_mutex_lock(&utex);
        //print_MMData(&ret);
        pthread_mutex_unlock(&utex);
    }
    return NULL;
}
void* producer(void* arg){
    queue_init();
    int i, N, res;
    FILE* fp=fopen("./data/task2.txt", "r");
    fscanf(fp, "%d", &N);
    // fprintf(stderr, "%d", N);
    pthread_t t[N];
    MMData datas[N];
    if(fp==NULL){
        printf("Error opening file\n");
        exit(1);
    }
    fro(i=0;i<N;i++){
        datas[i].task_id=i;
        // load_MMData(fp, &datas[i]);
    }
    for(i=0; i<N; i++){
        pthread_create(&t[i], NULL, add, &datas[i]);
    }
    for (i=0; i<N; i++){
        pthread_join(t[i], NULL);
    }
    queue_close();
    fclose(fp);
    return NULL;
}

void* consumer(void* arg){
    int nn = 10;//thread_cnt;//modify here
    pthread_t t[nn];
    MMData datas[nn];
    for(int i=0;i<nn;i++){
        pthread_create(&t[i], NULL, get, &datas[i]);
    }
    for(int i=0;i<nn;i++){
        pthread_join(t[i],NULL);
    }
    return NULL;
}

// you have to modify main to allow multi-threading.
int main(){
    pthread_t producer_thread, consumer_thread;
    pthread_mutex_init(&utex,NULL);
    pthread_create(&producer_thread, NULL, producer, NULL);
    pthread_create(&consumer_thread, NULL, consumer, NULL);
    pthread_join(producer_thread, NULL);
    pthread_join(consumer_thread, NULL);
    return 0;
}