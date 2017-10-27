# morion
STNS backed

http://stns.jp/en/interface

## ENdPoint

| path                          | Description            |
|----------------- -------------|------------------------|
| /v2/user/list                 | user list              |
| /v2/user/name/:user_name      | find by user name      |
| /v2/user/id/:uid              | find by user id        |
| /v2/group/list                | group list             |
| /v2/group/name/:group_name    | find by group name     |
| /v2/group/id/:gid             | find by group id       |
| /v2/sudo/name/:sudo_user_name | find by sudo user name |
| /v2/healthcheck               | health check url       |

## Metadata

| path        | Description                                          |
|-------------|------------------------------------------------------|
| api_version | api version                                          |
| result      | success only                                         |
| min_id      | please return the minimum Id in the All users, group |

## User

| Name       | Required | Description                           |
|------------|:--------:|---------------------------------------|
| id         |     x    | uid                                   |
| password   |          | login password by /etc/shadow format (mkpasswd --method=sha-512) |
| directory  |          | home directory                        |
| shell      |          | default shell                         |
| gecos      |          | general information about the account |
| keys       |          | public keys ([list] or null)          |
| link_users |          | stns link users ([list] or null)      |

```
"username": {
  "id": 1000,
  "password": "$6$qrSCOO2VM.qa3X$2wv5qLKr.WFNYeqhmcnvKuexhp0yNKSOT4hrAyK/368AqNrq/seCV6h.Oy2vZySu70fP6vjSiF5Xu4xuTnVK4.",
  "group_id": 100,
  "directory": "",
  "shell": "",
  "gecos": "John Peach",
  "keys": [
    "ecdsa-sha2-nistp256 AAAAE...",
    "ssh-rsa AAAAB3N..."
  ],
  "link_users": null
}
```
