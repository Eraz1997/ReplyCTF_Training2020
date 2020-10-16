# 2PAC Write-Up

## Analysis

```
> file 2pac

2pac: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=0b4c41222ea8f30b587e1520098bcb6beae49b59, stripped


> ./2pac

FLAG: {l0l xD}
```

* **strings** does not detect anything

* **ltrace** and **strace** does not work because of a anti-debugging tecnique

  * Through **strace** you can see that *ptrace()* is called and fails, then the program exits

* Through **ghidra** you can see that in **0x00001016** it checks *ptrace()* return value

  * *ptrace()* call is the syscall **0x80** just above the check

## Solution

* Delete the check in the binary with **radare2**

```
> r2 -w 2pac
> aaa
> s 0x00001016
> wx 0x9090909090
```

* Then run the executable through **radare2**

```
> ood
> dc
```

* In memory line **0x565e5020** you can see the fake flag *FLAG: {l0l xD}*

* In memory line **0x565e5000** there is the real flag
