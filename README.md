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

License
------

The MIT License (MIT)

Copyright (c) 2016 Jamal Youssefi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
