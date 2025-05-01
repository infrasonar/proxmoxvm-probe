[![CI](https://github.com/infrasonar/proxmoxvm-probe/workflows/CI/badge.svg)](https://github.com/infrasonar/proxmoxvm-probe/actions)
[![Release Version](https://img.shields.io/github/release/infrasonar/proxmoxvm-probe)](https://github.com/infrasonar/proxmoxvm-probe/releases)

# InfraSonar Proxmox Guest Probe

## Environment variable

Variable            | Default                        | Description
------------------- | ------------------------------ | ------------
`AGENTCORE_HOST`    | `127.0.0.1`                    | Hostname or Ip address of the AgentCore.
`AGENTCORE_PORT`    | `8750`                         | AgentCore port to connect to.
`INFRASONAR_CONF`   | `/data/config/infrasonar.yaml` | File with probe and asset configuration like credentials.
`MAX_PACKAGE_SIZE`  | `500`                          | Maximum package size in kilobytes _(1..2000)_.
`MAX_CHECK_TIMEOUT` | `300`                          | Check time-out is 80% of the interval time with `MAX_CHECK_TIMEOUT` in seconds as absolute maximum.
`DRY_RUN`           | _none_                         | Do not run demonized, just return checks and assets specified in the given yaml _(see the [Dry run section](#dry-run) below)_.
`LOG_LEVEL`         | `warning`                      | Log level (`debug`, `info`, `warning`, `error` or `critical`).
`LOG_COLORIZED`     | `0`                            | Log using colors (`0`=disabled, `1`=enabled).
`LOG_FTM`           | `%y%m%d %H:%M:%S`              | Log format prefix.

## Docker build

```
docker build -t proxmoxvm-probe . --no-cache
```

## Config

Example config _(change the `username`, `token_id` and `secret` to your own values and if required choose another `realm`)_:

```yaml
proxmoxcluster:
  config:
    username: root
    realm: pam
    token_id: monitoring
    secret: 12345678-1234-1234-1234-1234567890ab
proxmoxnode:
  use: proxmoxcluster
proxmoxvm:
  use: proxmoxcluster
```

## Dry run

Available checks:
- `proxmoxvm`

Create a yaml file, for example _(test.yaml)_:

```yaml
asset:
  name: "foo.local"
  check: "proxmoxvm"
  config:
    address: "10.0.0.1"
    node: "pve"
    vmid: "123"
    port: 8006
    ssl: false
```

Run the probe with the `DRY_RUN` environment variable set the the yaml file above.

```
DRY_RUN=test.yaml python main.py
```

## Proxmox API documentation

https://pve.proxmox.com/pve-docs/api-viewer
