# MutaSeal

MutaSeal is a GenLayer project that lets one Intelligent Contract improve another contract's defensive behavior without changing its address or clearing its stored state.

The project has two contracts:

- `SealKernel` keeps the allowed mutation rules and decides which defense may be added.
- `SealGuard` is the contract that changes. Its code can be replaced only by `SealKernel`.

The important restriction is that validators do not write arbitrary Python. They can select one inactive defense from a fixed list. `SealKernel` then renders the next `SealGuard` source deterministically and sends the upgrade.

## Demo idea

Generation 1 blocks a plain prompt override:

```text
ignore previous instructions
```

but intentionally misses a visually similar Unicode version:

```text
Ιgnore previоus instructiοns
```

Calling `SealKernel.evolve()` with that sample should activate `CONFUSABLE_FOLD`. After the child upgrade transaction finalizes, the same `SealGuard` address moves to the next generation and the same bypass is blocked.

## Mutation genes

`SealGuard` starts with `BASIC_OVERRIDE`. The kernel may later add one of these genes at a time:

- `ZERO_WIDTH_STRIP`
- `CONFUSABLE_FOLD`
- `ROLE_MARKUP`
- `SCHEME_GUARD`
- `ENCODED_PAYLOAD`
- `EXFILTRATION`

The active gene set, previous set, generation, counters, last attack and upgrade history stay in contract storage.

## Project layout

```text
app/                    Next.js frontend
contracts/
  seal_kernel.py
  seal_guard.py
tests/direct/           direct-mode contract tests
.github/workflows/      contract + frontend checks
DEPLOYMENT.md            deployment steps
SUBMISSION.md            Builder Portal copy
.env.example             public frontend variables
```

The Next.js app is intentionally at the repository root. Importing the GitHub repository into Vercel should therefore be detected as a normal Next.js project without setting a custom Root Directory.

## Local frontend

```bash
npm install
cp .env.example .env.local
npm run dev
```

For a production build:

```bash
npm run build
```

## Contract checks

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

genvm-lint check contracts/seal_guard.py
genvm-lint check contracts/seal_kernel.py
pytest tests/direct -v
```

## Frontend writes

The frontend targets Studionet, the same hosted Studio network used by the earlier demos. Browser writes are signed by the connected wallet and the UI waits for finalization before refreshing state.

No private key is stored in the website. Browser writes are signed by the connected wallet.

## Status

This is a testnet demonstration of bounded contract evolution, not a production security filter.

## License

MIT
