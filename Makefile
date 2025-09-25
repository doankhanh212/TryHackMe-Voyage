printf $'obj-m += reverse-shell.o\n\nall:\n\tmake -C /lib/modules/6.8.0-1030-aws/build M=$(PWD) modules\n\nclean:\n\tmake -C /lib/modules/6.8.0-1030-aws/build M=$(PWD) clean\n' > Makefile
