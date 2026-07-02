# CI/CD

Two GitHub Actions workflows drive this repo:

| Workflow | File | Trigger | What it does |
|---|---|---|---|
| **CI** | [.github/workflows/ci.yml](../.github/workflows/ci.yml) | push to `development`; PRs into `development` or `production` | Analyser `pytest`, frontend `vitest` + `vite build`, and a `docker compose config` lint. |
| **Deploy** | [.github/workflows/deploy.yml](../.github/workflows/deploy.yml) | push to `production` | SSH into the Ubuntu box **through Cloudflare Access**, then rebuild and restart the stack on the server. |

## Branch flow

```
feature ─PR─▶ development ──(CI runs)──▶ PR ─▶ production ──(Deploy runs)──▶ live
```

- `development` is the integration branch. Every push runs CI. **No deploy.**
- Merging a `development → production` PR pushes to `production`, which triggers the deploy.

The `production` branch does not exist yet — create it once:

```bash
git checkout development
git checkout -b production
git push -u origin production
```

Then in GitHub → Settings → Branches, protect `production` (require the CI checks + a PR to merge). Nothing pushes to it directly except merges.

## How the deploy reaches the server

The box is behind a Cloudflare tunnel with **no public inbound SSH**. Cloud runners can't SSH to it directly, so the deploy job:

1. Installs `cloudflared`.
2. Opens SSH with `ProxyCommand cloudflared access ssh --hostname <SSH_HOST>`.
3. Cloudflare Access authorises the connection via a **service token** (machine credential); then normal SSH key auth logs into the deploy user.
4. On the server: `git reset --hard origin/production` → `docker compose -f docker-compose.prod.yaml up -d --build` → prune → health-check the `api` container.

Images are built **on the server** — no registry involved.

```
GitHub-hosted runner                       Ubuntu box (behind tunnel)
┌────────────────────┐   Access service    ┌───────────────────────────┐
│ ssh + cloudflared  │─────token (CF-*)───▶│ cloudflared tunnel :22    │
│  ProxyCommand      │   then SSH key      │  └▶ sshd ▶ deploy user     │
└────────────────────┘                     │      git pull + compose up │
                                           └───────────────────────────┘
```

---

## One-time server setup

### 1. Deploy user + Docker

```bash
sudo adduser --disabled-password --gecos "" deploy
sudo usermod -aG docker deploy          # run compose without sudo
# Docker Engine + compose plugin must be installed (docs.docker.com/engine/install)
```

### 2. Clone the repo to the deploy path

Pick a path and keep it consistent with the `DEPLOY_PATH` secret (e.g. `/opt/strata`):

```bash
sudo mkdir -p /opt/strata && sudo chown deploy:deploy /opt/strata
sudo -u deploy git clone git@github.com:sagarvincent/cv_analyser.git /opt/strata
cd /opt/strata && sudo -u deploy git checkout production
```

For a private repo, give the `deploy` user read access — either a GitHub **deploy key** (`ssh-keygen` on the box, add the public half as a read-only deploy key on the repo) or clone over HTTPS with a token. Create the production `.env`:

```bash
sudo -u deploy cp /opt/strata/.env.example /opt/strata/.env
sudo -u deploy nano /opt/strata/.env      # set DB_PASSWORD etc.
```

### 3. SSH key for the CI → server hop

This is the key SSH itself uses (separate from Cloudflare Access). Generate a dedicated keypair; **do not** add a passphrase (CI can't type one):

```bash
ssh-keygen -t ed25519 -f deploy_key -N "" -C "github-actions-deploy"
# public half → server:
sudo -u deploy mkdir -p /home/deploy/.ssh && sudo -u deploy chmod 700 /home/deploy/.ssh
cat deploy_key.pub | sudo -u deploy tee -a /home/deploy/.ssh/authorized_keys
sudo -u deploy chmod 600 /home/deploy/.ssh/authorized_keys
# private half (deploy_key) → GitHub secret SSH_PRIVATE_KEY (see below)
```

### 4. Cloudflare Access: SSH over the tunnel

In the Cloudflare Zero Trust dashboard:

1. **Tunnel → Public hostname**: add a hostname (e.g. `ssh.strata.example.com`) with service `SSH` → `localhost:22` on the existing tunnel.
2. **Access → Applications → Add → Self-hosted**: application domain = that same hostname.
3. **Service Auth**: create a **Service Token** — note the *Client ID* and *Client Secret* (secret shown once).
4. **Policy** on the application: action **Service Auth**, include → *Service Token* = the one you just made. (Add a second policy for your own email if you want to SSH in manually too.)

`cloudflared` on the server must already be routing the tunnel (it is, since the app is served this way).

---

## GitHub secrets

Set these under **Settings → Environments → `production` → Secrets** (the deploy job uses `environment: production`, so you can also add required reviewers there):

| Secret | Value |
|---|---|
| `SSH_HOST` | The Access hostname, e.g. `ssh.strata.example.com` |
| `SSH_USER` | `deploy` |
| `SSH_PRIVATE_KEY` | Contents of `deploy_key` (the private half, full PEM including header/footer) |
| `DEPLOY_PATH` | Repo path on the server, e.g. `/opt/strata` |
| `CF_ACCESS_CLIENT_ID` | Cloudflare Access service token *Client ID* (ends in `.access`) |
| `CF_ACCESS_CLIENT_SECRET` | Cloudflare Access service token *Client Secret* |

---

## Verifying the setup

**Locally**, confirm the Access + SSH path before relying on CI:

```bash
export TUNNEL_SERVICE_TOKEN_ID=<client-id>
export TUNNEL_SERVICE_TOKEN_SECRET=<client-secret>
ssh -o ProxyCommand="cloudflared access ssh --hostname ssh.strata.example.com" \
    -i deploy_key deploy@ssh.strata.example.com \
    "cd /opt/strata && docker compose -f docker-compose.prod.yaml ps"
```

**In CI**, push a trivial commit to `production` and watch the **Deploy** run. The health-check step polls the `api` container's Docker health status (defined in `docker-compose.prod.yaml`) for up to two minutes.

## Rollback

Deploys are just `git reset --hard origin/production` + rebuild, so to roll back, point `production` at the previous good commit:

```bash
git checkout production
git reset --hard <good-sha>
git push --force-with-lease origin production   # re-triggers Deploy on the old code
```
