prosfvd
=======

<<<<<<< HEAD
sfv-check-daemon for proftpd


setup
=====

proftpd.conf
------------
<pre><code>
Logformat sfv-auto "%m#%F"
Logformat sfv-cmd "%m#%d"
</code></pre>

virtuals.conf
-------------
<pre><code>
&lt;VirtualHost ...&gt;
    ExtendedLog /site/proftpd/fifo/sfv.fifo WRITE sfv-auto
    ExtendedLog /site/proftpd/fifo/sfv.fifo MISC sfv-cmd
&lt;/VirtualHost\&gt;
</code></pre>
=======
sfv-check-daemon for proftpd 
>>>>>>> d094a171abce2d0ebf428f244dccd48eac316f12
