prosfvd
=======

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
