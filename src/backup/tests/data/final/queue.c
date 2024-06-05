// naive implementation
#include "mm.h" // MMData
#include "queue.h"
#include <pthread.h> // for thread synchronization

pthread_cond_t cond;
pthread_mutex_t mutex;

struct MMQueue{
    // Circular Queue
    MMData data[MAX_QUEUE_LEN];
    // head, tail of this queue
    int h, t; 
    // closed means no more data can be added
    int closed;
}QData;

void queue_init(){
    // init/reset the queue
    QData.h = 0;
    QData.t = 0;
    QData.closed = 0;
    pthread_cond_init(&cond, NULL);
    pthread_mutex_init(&mutex, NULL);
}

int queue_get(MMData *ret){
    pthread_mutex_lock(&mutex);
    // pthread_mutex_lock(&mutex2);
    // printf("remove begin one\n");
    // pthread_mutex_unlock(&mutex2);
    while(QData.h >= QData.t){
        if(QData.closed){
            pthread_mutex_unlock(&mutex);
            return -1;
        }
        // pthread_mutex_lock(&mutex2);
        // printf("remove wait one\n");
        // pthread_mutex_unlock(&mutex2);
        pthread_cond_wait(&cond, &mutex);
        // pthread_mutex_lock(&mutex2);
        // printf("%d %d\n",QData.h,QData.t);
        // pthread_mutex_unlock(&mutex2);
    }
    int h = QData.h;
    QData.h++;
    // pthread_mutex_lock(&mutex2);
    // printf("remove one\n");
    // pthread_mutex_unlock(&mutex2);
    *ret = QData.data[h%MAX_QUEUE_LEN]; // circular use the QData.data
    // printf("%d, %d, %s\n", cond.__align,cond.__data, cond.__size);
    pthread_cond_broadcast(&cond);
    pthread_mutex_unlock(&mutex);
    return 0; // 0 means success
}

int queue_add(MMData data){
    if(QData.closed) return -1;
    pthread_mutex_lock(&mutex);
    // pthread_mutex_lock(&mutex2);
    // printf("add begin one\n");
    // pthread_mutex_unlock(&mutex2);
    while(QData.t - QData.h >= MAX_QUEUE_LEN){
        if(QData.closed){
            pthread_mutex_unlock(&mutex);
            return -1;
        }
        // pthread_mutex_lock(&mutex2);
        // printf("add wait one\n");
        // pthread_mutex_unlock(&mutex2);
        pthread_cond_wait(&cond, &mutex);
        // pthread_mutex_lock(&mutex2);
        // printf("%d %d\n",QData.h,QData.t);
        // pthread_mutex_unlock(&mutex2);
    }
    int t = QData.t;
    QData.t++;
    // pthread_mutex_lock(&mutex2);
    // printf("add one\n");
    // printf("add 1919\n");
    // pthread_mutex_unlock(&mutex2);
    QData.data[t%MAX_QUEUE_LEN] = data;
    printf("add 514\n");
    // pthread_cond_broadcast(&bird);
    // printf("%d, %d, %s\n", cond.__align,cond.__data.__g_size[0], cond.__size);
    pthread_cond_broadcast(&cond);
    printf("add 114\n");
    pthread_mutex_unlock(&mutex);
    return 0; // 0 means success
}

void queue_close(){
    // pthread_mutex_lock(&mutex2);
    // printf("queue closed\n");
    // pthread_mutex_unlock(&mutex2);
    QData.closed = 1;
    pthread_mutex_lock(&mutex);
    pthread_cond_broadcast(&cond);
    pthread_mutex_unlock(&mutex);
}
