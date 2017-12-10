# morion

STNS server

http://stns.jp/en/interface

## ENdPoint

| path                          | Description            |
|-------------------------------|------------------------|
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

## Server Setup

### CentOS 7

```
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install git gcc python36u python36u-devel python36u-pip
git clone https://github.com/yteraoka/morion.git
cd morion
git checkout develop
python3.6 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
cd morion
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

## Client Setup

http://stns.jp/ja/install

### RHEL / CentOS

#### package のインストールと libnss_stns.conf 設定

```
curl -fsSL https://repo.stns.jp/scripts/yum-repo.sh | sh
sudo yum -y install stns libnss-stns libpam-stns nscd
sudoedit /etc/stns/libnss_stns.conf
```

#### ログイン時に Home directory を作成するための設定

```
echo 'session required pam_mkhomedir.so skel=/etc/skel/ umask=0022' \
   | sudo bash -c "cat >> /etc/pam.d/sshd"
```

#### OpenSSH Server が Public key を stns から取得できるようにする

```
sudo sed -i -r \
  -e 's@^#?(AuthorizedKeysCommand) .*@\1 /usr/lib/stns/stns-key-wrapper@' \
  -e 's@^#?(AuthorizedKeysCommandUser) .*@\1 root@' \
   /tmp/sshd_config
```

#### nsswitch.conf 設定 (passwd, shadow, group に stns を追加)

```
sudoedit /etc/nsswitch.conf
```

```
passwd:     files sss stns
shadow:     files sss stns
group:      files sss stns
```

#### nscd.conf 設定 (毎回外部へ問い合わせていては遅いのでキャッシュさせる)

```
sudoedit /etc/nscd.conf
sudo systemctl enable nscd
sudo systemctl start nscd
```

TTL 設定が期待とちがってよくわからん・・・

#### SELinux が有効だとうまく動かないため、関係するドメインを無効にする

```
sudo yum -y install policycoreutils-python
sudo semanage permissive -a sshd_t
sudo semanage permissive -a chkpwd_t
sudo semanage permissive -a nscd_t
```

