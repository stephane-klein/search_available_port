# Search available port helper script

Issue context (in French): https://github.com/stephane-klein/backlog/issues/330


```sh
$ ./search_available_port.py --from=5432 --name=issue8 --state=./state.json
Free port: 5434
./state.json updated
```

```sh
$ cat state.json
{
    "issue3": 5435,
    "issue4": 5433,
    "issue8": 5434
}
```

```sh
$ ./get_instance_port.py --name=issue3 --state=./state.json
5435
```

```sh
$ ./get_instance_port.py --name=notfound --state=./state.json
Not found
```

```sh
$ ./remove_instance_port.py --name=issue3 --state=./state.json
state file updated
```

```sh
$ cat state.json
{
    "issue4": 5433,
    "issue8": 5434
}
```

```sh
$ ./remove_instance_port.py --name=issue3 --state=./state.json
instance not found in state file, no change made
```
