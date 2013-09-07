prosfvd
=======

sfv-check-daemon for proftpd


setup
=======

* proftpd.conf

Logformat sfv-auto "%m#%F"
Logformat sfv-cmd "%m#%d"

* virtuals.conf
<VirtualHost ....>
    ExtendedLog /site/proftpd/fifo/sfv.fifo WRITE sfv-auto
    ExtendedLog /site/proftpd/fifo/sfv.fifo MISC sfv-cmd
</VirtualHost>