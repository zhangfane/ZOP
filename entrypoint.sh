#!/bin/sh
#
#set -e


# init db
## init db
#if [ ! -d /var/lib/mysql/mysql ]; then
#    echo 'Initializing db, please wait ...'
#    REQUIRE_INIT_OPS=true
##    /bin/sh /ZOP/init_db.sh
#fi
#nohup /usr/bin/mysqld_safe --datadir=/var/lib/mysql --user=root
#tail -f /dev/null

python3.6 /ZOP/web/manage.py run
