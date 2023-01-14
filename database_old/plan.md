
### Connector
- connection details
- abstract calls
- test connection details

```
ConnConfig
    classvars which apply everywhere
    children change classvars only for their connection
    children can also have instance configuration
    params:
        - logger
        - instant_client
        - connection parameters
        - cursor parameters
        - test mode
        - read file parent directory
        - write file parent directory
        
Connection
    connection params:
        - GSecret
        - Environ
        - dsn
    conn configuration param
    altr connection as param
    test connection as param
    abstract conn calls:
        - async execute
        - async copy in/out
        - connection pool
        - sequencial execute
        - sequential executemany
        - sequential copy in/out
```