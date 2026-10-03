# Local-only interview setup

The original README is unchanged. Its GitHub fork/bootstrap steps have been replaced by a local Git source at the user's request. The migration exercise has not been implemented.

- Working repository: `/Users/pravinmohature/GitRepo/interview-local`, branch `main`.
- Cluster/context: `old-cluster` / `kind-old-cluster`.
- `interview-git` serves this repository read-only on Docker's `kind` network, without publishing a host port. No GitHub or token is used.
- Flux's `flux-system` GitRepository reads `http://172.19.0.4:8000/interview-local/.git` every 30 seconds.
- The root Flux Kustomization reads `clusters/production`; its children read `apps` and `infrastructure`.
- `api-lb` exposes the exercise at http://localhost:8080.

## Apply changes during practice

Edit manifests, then commit them locally on `main`. Flux sees commits; saving an uncommitted file is insufficient. There is no remote push step in this local variant.

```bash
cd /Users/pravinmohature/GitRepo/interview-local
git add <files-you-edited>
git -c user.name='Interview Local Setup' -c user.email='interview-local@localhost' commit -m 'Describe the change'
flux reconcile source git flux-system --context kind-old-cluster
flux get all --context kind-old-cluster
```

## Check the baseline

```bash
kubectl --context kind-old-cluster get pods -A
flux get all --context kind-old-cluster
curl http://localhost:8080/inference
curl http://localhost:8080/discovery
./traffic/send-traffic.sh
```

The expected inference response includes `cluster: old-cluster`, `allocated: true`, and `released: true`.

## Local Git server recovery

The Docker image contains the server; its build files are preserved in `local-setup/git-server`. Keep Docker and the `interview-git` container running. The working folder is mounted read-only into the server. If the server container is recreated, its Docker IP may change: inspect it with `docker inspect interview-git` and update the Flux GitRepository URL accordingly.

The original teardown script does not remove this additional `interview-git` container. To remove it when retiring the entire exercise, run `docker rm -f interview-git` separately.

The original README expects GitHub push access during the interview. This local adaptation provides equivalent commit-based reconciliation locally, but does not provide a GitHub fork.
