__Reader-Writer Problem__: shared database, many readers + 1 writer

目标: reader只读完整的内容

Correctness Constraints:
– Readers can access database when no writers
– Writers can access database when no readers or writers
– Only one thread manipulates state variables at a time

– State variables (Protected by a lock called “lock”):
» int AR: Number of active readers; initially = 0
» int WR: Number of waiting readers; initially = 0
» int AW: Number of active writers; initially = 0
» int WW: Number of waiting writers; initially = 0

» Condition okToRead = NIL

» Condition okToWrite = NIL

- 2 waiting places

``` c
Reader() {
    // First check self into system
    lock.Acquire();
    while ((AW + WW) > 0) { // Is it safe to read?
        WR++; // No. Writers exist
        okToRead.wait(&lock); // Sleep on cond var
        WR--; // No longer waiting
    }
    AR++; // Now we are active!
    lock.release();
    // Perform actual read-only access
    AccessDatabase(ReadOnly);
    // Now, check out of system
    lock.Acquire();
    AR--; // No longer active
    if (AR == 0 && WW > 0) // No other active readers
    okToWrite.signal(); // Wake up one writer
    lock.release();
}
```

``` c
Writer() {
    // First check self into system
    lock.Acquire();
    while ((AW + AR) > 0) { // Is it safe to write?
        WW++; // No. Active users exist
        okToWrite.wait(&lock); // Sleep on cond var
        WW--; // No longer waiting
    }
    AW++; // Now we are active!
    lock.release();
    // Perform actual read/write access
    AccessDatabase(ReadWrite);
    // Now, check out of system
    lock.Acquire();
    AW--; // No longer active
    if (WW > 0){ // Give priority to writers
        okToWrite.signal(); // Wake up one writer
    } else if (WR > 0) { // Otherwise, wake reader
        okToRead.broadcast(); // Wake all readers
    }
    lock.release();
}
```

writer有优先级，否则writer一直进不去

叫醒一个人的代价: some context switches, 不是很多也不是很少

__LANGUAGE SUPPORT FOR SYNCHRONIZATION__

C++的问题： throw exception

需要catch+release lock

C++ support: destruct lock时直接release

Java: __Synchronized__ -> 隐藏lock (有关键字的函数就创建锁，out of scope就释放); lock是属于一个class的


# New way: communicate by sending messages

instead of sharing memory

In `Go`: using channel (queue)

# Deadlocks

__Preemptive / non-preemptive resources__: preemptable -> can take it away; (CPU)

non -> must leave it with the thread; (lock, printer)

__Starvation & Deadlock__: deadlock必须是cyclic waiting for resources

2 resources / 2 users

__4 requirements for deadlock__: 

- Mutual exclusion

- Hold and wait

- No preemption

- circular wait

To fix deadlock: kill & restart (often database)

OS: ignore

__Prevention__:

1. Infinite resources! 

- illusion of infinite resources: virtual memory

2. No sharing (不现实)

3. No waiting (traditional phone company)

4. Make all threads request everything at the beginning -> some waste, but correct

5. In particular order so that no circular -> require global order
