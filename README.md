# MutaSeal

MutaSeal is a GenLayer project where one Intelligent Contract can update another contract's defensive logic without changing its address or clearing its stored state.

It has two contracts:

- `SealKernel` owns a fixed mutation policy and decides which defense can be activated.
- `SealGuard` is the upgradable contract. Only `SealKernel` is registered as its upgrader.

Validators do not generate arbitrary Python. They select one inactive defense from a fixed list. `SealKernel` then renders the next `SealGuard` source deterministically and sends the upgrade after finalization.

## Demo

Generation 1 blocks a plain prompt override:

```text
ignore previous instructions
```

but intentionally misses this Unicode look-alike version:

```text
Ιgnore previоus instructiοns
```

Calling `SealKernel.evolve()` with that sample should activate `CONFUSABLE_FOLD`. After the child upgrade finishes, the same `SealGuard` address moves to the next generation and the same bypass is blocked.

## Mutation genes

`SealGuard` starts with `BASIC_OVERRIDE`. The kernel may add one of these genes at a time:

- `ZERO_WIDTH_STRIP`
- `CONFUSABLE_FOLD`
- `ROLE_MARKUP`
- `SCHEME_GUARD`
- `ENCODED_PAYLOAD`
- `EXFILTRATION`

The active gene set, previous set, generation, counters, last attack and upgrade history are stored on-chain.

## Contract guardrails

- expected user-facing failures use `gl.vm.UserError`
- the guard's code slot is changed through GenLayer's native `gl.storage.Root` upgrade mechanism
- only the kernel address is added to the guard's upgrader list
- storage field order and types are kept identical in every generated guard version
- non-deterministic mutation selection is isolated inside `gl.vm.run_nondet_unsafe`
- validator logic independently re-runs the same bounded classification and must agree on the selected gene
- contract-to-contract upgrades are emitted only after finalization
- rollback is restricted to the kernel owner

## Project layout

```text
app/                    Next.js frontend
contracts/
  seal_kernel.py
  seal_guard.py
tests/direct/           Direct Mode tests
.github/workflows/      lint, direct tests and frontend build
DEPLOYMENT.md            deployment steps
.env.example             public frontend variables
```

The Next.js app is at the repository root, so Vercel can import the GitHub repository directly without a custom Root Directory.

## Local frontend

```bash
npm install
cp .env.example .env.local
npm run dev
```

Production build:

```bash
npm run build
```

## Contract checks

Python 3.12+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

genvm-lint check contracts/seal_guard.py
genvm-lint check contracts/seal_kernel.py
pytest tests/direct -v
```

`genlayer-test` controls the compatible `genlayer-py` dependency. It is intentionally not pinned separately in `requirements.txt`.

## Network

The frontend targets GenLayer Studionet and uses the Studio explorer:

```text
https://explorer-studio.genlayer.com
```

Browser writes are signed by the connected wallet. No private key is stored in the website.

## Status

MutaSeal is a testnet demonstration of bounded contract evolution, not a production security filter.

## License

MIT
