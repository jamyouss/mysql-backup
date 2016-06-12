Mysql Backup
-----

This script aim to organize your MySql databases dump.

```
Dumping structure and contents of MySQL databases.
usage: python mysql-backup.py [options]

--help                 : Display this help message and exit.
-v, --version          : Output version information and exit.
-l, --login-path=name  : Login path name.
-D, --databases=name   : databases name to dump.
-d, --directory=name   : Backup directory.
-m, --max-days=days    : Maximum days of backup (default 15 days).
```

1. Create a Mysql config
---
For a better security, the script use the `--login-path` option of `mysqldump` instead of passing the password in clear.

Let's create a user named `my_user`

```
mysql_config_editor set --login-path=dev --host=localhost --user=my_user --password
```

2. Create a backup
---

Let's create a backup of databases named `database1` and `database2`.

```
python mysql-backup.py --login-path=dev --databases='database1 database2' --directory=/opt/mysql/backup
```

And if we list the `/opt/mysql/backup` directory:

![alt tag](https://raw.githubusercontent.com/razmo/mysql-backup/master/screen.png)

Enjoy !
