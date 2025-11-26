# VekPlay Database Setup

This guide helps to create, edit and load empty VekPlay database into MySQL.

## MySQL

```sql
mysql$ DROP DATABASE IF EXISTS vekplay;
mysql$ CREATE DATABASE vekplay;
mysql$ USE vekplay
mysql$ SOURCE /data/all/projects/git/VekPlay/db/vekplay_empty.sql
mysql$ CREATE USER 'vekplay_user'@'%' IDENTIFIED BY 'some_password';
mysql$ GRANT SELECT ON vekplay.* TO vekplay_user@'%';
mysql$ GRANT ALL ON vekplay.* TO vekplay_user@'%';
mysql$ FLUSH PRIVILEGES;
```

If MySQL shows an access denied error, try using "localhost" instead of "%":
```sql
mysql$ GRANT SELECT ON vekplay.* TO vekplay_user@'localhost';
```

You can list the privileges granted to a MySQL user account ('vekplay_user'):
```sql
mysql$ SHOW GRANTS FOR vekplay_user;
```

## Details

  * Edit `vekplay.mwb` file in MySQL Workbench, export it to `vekplay_empty.sql`
  * Make substitution in `vekplay_empty.sql` in VIM by RE:
```
%s/`mydb`\.//g
```
  * Create DB in MySQL, e.g. `vekplay`
  * `USE vekplay`
  * `SOURCE vekplay_empty.sql`
