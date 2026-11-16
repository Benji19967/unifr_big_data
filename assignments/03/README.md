# Redis

## Using [mise](https://mise.jdx.dev/) tasks

```
mise trust && mise install
mise run redis-start
mise run redis-load
...redis-cli commands...
mise run redis-stop
```

and `mise tasks` to get reminded of the available tasks.

## Running manual commands

### Launch a server

Launch a redis server instance, `/tmp` is where the `dump.rdb` data will be dumped on shutdown.
```
redis-server --dir /tmp
```

Or in the background

```
redis-server --daemonize yes --dir /tmp
```

Use `--dir ~/.local/share/redis` for the data to survive a reboot.

### Load the data

```
redis-cli < data/bookshop_database.txt
```

### Check it worked

```
redis-cli DBSIZE              # expect 101
redis-cli HGETALL book:0
```

### Shutdown the server

```
redis-cli shutdown
```

or `Ctrl-C` if the server is running in the foreground.
