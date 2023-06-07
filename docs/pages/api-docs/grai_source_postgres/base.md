---
sidebar_label: base
title: grai_source_postgres.base
---

#### get\_nodes\_and\_edges

```python
def get_nodes_and_edges(
        connector: PostgresConnector,
        version: Literal["v1"]) -> Tuple[List[Node], List[Edge]]
```

**Arguments**:

  connector (PostgresConnector):
  version (Literal[&quot;v1&quot;]):


**Returns**:



#### update\_server

```python
def update_server(client: BaseClient,
                  dbname: Optional[str] = None,
                  namespace: Optional[str] = None,
                  user: Optional[str] = None,
                  password: Optional[str] = None,
                  host: Optional[str] = None,
                  port: Optional[str] = None)
```

**Arguments**:

  client (BaseClient):
- `dbname` _Optional[str], optional_ - (Default value = None)
- `namespace` _Optional[str], optional_ - (Default value = None)
- `user` _Optional[str], optional_ - (Default value = None)
- `password` _Optional[str], optional_ - (Default value = None)
- `host` _Optional[str], optional_ - (Default value = None)
- `port` _Optional[str], optional_ - (Default value = None)


**Returns**: