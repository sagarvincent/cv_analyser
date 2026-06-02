# TLS certificates

The **Vite dev server** serves local HTTPS by reading two files from this directory:

- `fullchain.pem` — the certificate plus its intermediate chain
- `privkey.pem` — the matching private key

These files are **gitignored** (private keys must never be committed). Use recipe
**§A** for local development.

**Production does not use this directory** — its certs are obtained and renewed
automatically by `nginx-proxy` + `acme-companion` into a Docker volume (see **§B**).
Recipes **§C** (AWS) and **§D** (provided certs) cover other deployment targets.

---

## A. Local development — self-signed via `openssl` (no extra install)

A public CA never issues a certificate for `localhost`, so generate a self-signed
pair. `openssl` ships with **Git for Windows** (`C:\Program Files\Git\usr\bin\`), so
run this from a **Git Bash** shell, in this `certs/` directory:

```bash
# MSYS_NO_PATHCONV stops Git Bash from mangling the "/CN=localhost" argument
MSYS_NO_PATHCONV=1 openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
  -keyout privkey.pem -out fullchain.pem \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

> macOS / Linux (openssl on PATH): drop the `MSYS_NO_PATHCONV=1` prefix.
> PowerShell: openssl is usually not on PATH there — use Git Bash, or call it by
> full path: `& 'C:\Program Files\Git\usr\bin\openssl.exe' ...`.

The browser shows a one-time "not trusted" warning (click **Proceed** / **Advanced
→ Continue**) because the cert is self-signed rather than chained to a trusted CA.

Each developer runs this on their own machine. The resulting PEMs stay local.

> Optional, warning-free alternative: install [`mkcert`](https://github.com/FiloSottile/mkcert),
> run `mkcert -install` once, then `mkcert localhost 127.0.0.1 ::1` and rename the
> outputs to `fullchain.pem` / `privkey.pem`. This trusts a local CA so the lock
> icon is green with no warning. Not required.

---

## B. Production (Docker on a real domain) — automatic via nginx-proxy + acme-companion

Production does **not** use this `certs/` host directory. `docker-compose.yaml`
runs two extra containers that obtain and renew Let's Encrypt certificates with no
manual steps, storing them in a Docker-managed `certs` volume:

- **`nginx-proxy`** terminates TLS on `:443`, redirects `:80 → :443`, and routes by
  the `frontend` container's `VIRTUAL_HOST`.
- **`acme-companion`** runs the ACME HTTP-01 challenge for `LETSENCRYPT_HOST` and
  renews ~every 60 days.

**Prerequisites:**
1. A real domain with a DNS **A/AAAA record pointing at this host**.
2. Ports **80 and 443 reachable from the internet** (the ACME challenge needs them).

**Steps:**
```bash
cp .env.example .env          # then set PROD_DOMAIN and ACME_EMAIL
docker compose up -d --build  # certs auto-issue into the `certs` volume
docker compose logs -f acme-companion   # watch issuance
```

> **Test first against staging** to avoid Let's Encrypt rate limits: uncomment
> `ACME_CA_URI: https://acme-staging-v02.api.letsencrypt.org/directory` on the
> `acme-companion` service. Browsers will warn (staging CA is untrusted) — that's
> expected. Remove it and `docker compose up -d` again to get a real trusted cert.

---

## C. AWS ECS — terminate TLS at the ALB (preferred)

The idiomatic AWS path does **not** put certs in the container:

1. Request a free **ACM** certificate for your domain (DNS-validated, auto-renews).
2. Attach it to the Application Load Balancer's **:443** listener.
3. Add a **:80 → :443** redirect listener.

The ECS task then keeps serving plain HTTP on `:80` behind the ALB. The nginx
`:443` block in `frontend/nginx.conf` is only needed if you also want TLS *inside*
the task.

---

## D. Provided / internal-CA certificates

Place the certificate chain as `fullchain.pem` and the key as `privkey.pem`. If
you were given separate files (e.g. `cert.crt` + `chain.crt`), concatenate them
**cert first, then intermediates** into `fullchain.pem`.
