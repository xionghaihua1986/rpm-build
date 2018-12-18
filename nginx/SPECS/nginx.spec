#1.define 
%define name nginx
%define version 1.14.2
%define _prefix /opt/websuite/nginx

### 1.The introduction section 
Name: %{name}
Version: %{version}    
Summary: nginx-1.14.2.tar.gz to nginx-1.14.2.rpm   
Group: Applications/Archiving      
License: GPLv2                     
Release: 6%{?dist}
URL: http://nginx.org/
Packager: louis <851628816@qq.com>
Vendor: louis

Source0: %{name}-%{version}.tar.gz     
Source1: nginx.init                   
Source2: nginx.conf                  
Source3: fastcgi_params

BuildRoot: %_topdir/BUILDROOT
 
BuildRequires: gcc,make,gcc-c++,pcre,pcre-devel
Requires: openssl-devel,pcre-devel,zlib-devel
%description
Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and
IMAP protocols, with a strong focus on high concurrency, performance and low
memory usage.

 
###  2.The Prep section 准备阶段,主要就是把源码包解压到build目录下，设置一下环境变量，并cd进去
 
%prep 
%setup -q    
 
###  3.The Build Section 编译制作阶段，这一节主要用于编译源码
 
%build 
./configure --prefix=%{_prefix} \
--pid-path=/opt/run/nginx/nginx.pid \
--error-log-path=/opt/log/nginx/error.log \
--user=nginx \
--group=nginx \
--with-stream \
--with-file-aio \
--with-http_ssl_module \
--with-http_flv_module \
--with-http_v2_module \
--with-http_flv_module \
--with-http_mp4_module \
--with-http_stub_status_module \
--with-http_gzip_static_module \
--conf-path=/opt/config/nginx/conf/nginx.conf \
--with-pcre

make

#make %{?_smp_mflags}            # make后面的意思是：如果就多处理器的话make时并行编译 
 
###  4.Install section  这一节主要用于完成实际安装软件必须执行的命令，可包含4种类型脚本
 
%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}/etc/rc.d/init.d/nginx
%{__install} -p -D %{SOURCE2} %{buildroot}/opt/config/nginx/conf/nginx.conf
%{__install} -p -D %{SOURCE3} %{buildroot}/opt/config/nginx/conf/fastcgi_params

#脚本段
%pre 
if [ $1 == 1 ];then
	/usr/sbin/groupadd -g 888 nginx
        /usr/sbin/useradd -u 888 -g nginx -M nginx -s /sbin/nologin 2> /dev/nulll
fi          
                                                            
%post 
if [ $1 == 1 ];then
        /sbin/chkconfig --add nginx
        /sbin/chkconfig nginx on
fi
%preun 
if [ $1 == 0 ];then
        /usr/sbin/userdel -r nginx 2> /dev/null
        /etc/init.d/nginx stop > /dev/null 2>&1
fi
%postun
 
###  5.clean section 清理段,clean的主要作用就是删除BUILD
 
%clean
rm -rf %{buildroot}
 
###  6.file section 文件列表段，这个阶段是把前面已经编译好的内容要打包了,其中exclude是指要排除什么不打包进来。
 
%files              
%defattr(-,nginx,nginx,0755)
/opt/websuite/nginx
/opt/config/nginx
/opt/run/nginx
/opt/log/nginx
%doc LICENSE CHANGES README
%dir /opt/run/nginx
%attr(0755,root,root) /etc/rc.d/init.d/nginx
%config(noreplace) /opt/config/nginx/conf/nginx.conf
%config(noreplace) /opt/config/nginx/conf/fastcgi_params
 
###  7.chagelog section  日志改变段， 这一段主要描述软件的开发记录
 
%changelog
* Thu Oct 12 2018 louis <851628816@qq.com>  
- Initial version
