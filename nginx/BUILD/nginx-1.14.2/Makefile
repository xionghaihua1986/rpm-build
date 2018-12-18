
default:	build

clean:
	rm -rf Makefile objs

build:
	$(MAKE) -f objs/Makefile

install:
	$(MAKE) -f objs/Makefile install

modules:
	$(MAKE) -f objs/Makefile modules

upgrade:
	/opt/websuite/nginx/sbin/nginx -t

	kill -USR2 `cat /opt/run/nginx/nginx.pid`
	sleep 1
	test -f /opt/run/nginx/nginx.pid.oldbin

	kill -QUIT `cat /opt/run/nginx/nginx.pid.oldbin`
