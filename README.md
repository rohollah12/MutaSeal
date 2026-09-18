# MutaSeal

MutaSeal is a GenLayer project where one Intelligent Contract can update another contract's defensive logic without changing its address or clearing its stored state.

It has two contracts:

- `SealKernel` owns a fixed mutation policy and decides which defense can be activated.
- `SealGuard` is the upgradable contract. Only `SealKernel` is registered as its upgrader.

Validators do not generate arbitrary Python. They select one inactive defense from a fixed list. `SealKernel` then renders the next `SealGuard` source deterministically and sends the upgrade after finalization.

## Reviewer quick start

The public demo is a shared on-chain deployment. Its generation may already be higher than 1 when you open the site because every successful mutation persists on the same `SealGuard` contract.

That is expected. You do **not** need to redeploy contracts to keep testing.

1. Open the live site and look at **Generation** and **Active genes**.
2. In **Attack lab**, choose a preset marked **TRY NEXT**. Presets already covered by the guard are marked **LEARNED**.
3. Click **Test (read)**. For a useful next mutation, the current result should be `ALLOW`.
4. Connect a Studionet wallet and click **Evolve from bypass**.
5. Wait for the parent `SealKernel.evolve()` transaction and the finalized child upgrade transaction.
6. The same `SealGuard` address should advance by one generation.
7. The frontend checks the same sample again. It should now return a `BLOCK:...` result.

If a sample is already blocked, the frontend will not submit another evolution for it. Pick another preset marked **TRY NEXT**.

### Clean first-generation demo

A freshly deployed `SealGuard` starts with:

```text
generation=1
genes=BASIC_OVERRIDE
```

It blocks:

```text
ignore previous instructions
```

but intentionally misses this Unicode look-alike version:

```text
Ιgnore previоus instructiοns
```

Calling `SealKernel.evolve()` with that bypass should activate `CONFUSABLE_FOLD`. When the finalized child upgrade completes, the **same SealGuard address** moves to generation 2 and blocks the same Unicode input.

For the final public demo, the project owner can deploy a fresh Kernel/Guard pair so reviewers can see the clean `generation 1 → generation 2` path first. After that, the same pair remains usable for additional generations.

## Continuing after generation 2

MutaSeal is not a one-shot demo. The same guard can keep learning one bounded defense at a time. The frontend includes these presets:

| Preset | Gene it demonstrates | Example behavior before activation |
| --- | --- | --- |
| Homoglyph | `CONFUSABLE_FOLD` | Unicode look-alikes hide the plain override phrase |
| Zero-width | `ZERO_WIDTH_STRIP` | a zero-width character splits `ignore` |
| Role markup | `ROLE_MARKUP` | injected `<system>` / role markup |
| Script URL | `SCHEME_GUARD` | `javascript:` / data-style executable schemes |
| Encoded payload | `ENCODED_PAYLOAD` | obvious base64/payload handoff language |
| Exfiltration | `EXFILTRATION` | direct request for hidden/system/developer instructions |

Example lifecycle:

```text
Gen1  BASIC_OVERRIDE
  ↓ Homoglyph bypass
Gen2  + CONFUSABLE_FOLD
  ↓ Zero-width bypass
Gen3  + ZERO_WIDTH_STRIP
  ↓ Role-markup bypass
Gen4  + ROLE_MARKUP
  ↓ ...
```

The exact mutation selected is still decided by GenLayer consensus. The frontend presets are designed to map directly to one inactive bounded gene, but reviewers can also type their own samples.

### Reviewer permissions

The wallet that deployed `SealKernel` is its **owner**, but reviewers do not need the owner's wallet. A reviewer can connect any Studionet wallet and call `evolve()` for a sample that currently returns `ALLOW`. If consensus selects a valid inactive gene, `SealKernel` performs the upgrade on the registered `SealGuard`.

Owner-only functions are intentionally kept out of the public demo UI:

- `register_guard(...)` — initial/admin setup
- `rollback()` — recovery to the immediately previous gene set

The public frontend focuses only on the reviewer path: **Test → Evolve → verify the same sample is now blocked**.

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
- `evolve()` is permissionless, so any reviewer can submit a currently unblocked bypass from their own wallet
- `register_guard()` and `rollback()` are owner-only administrative actions
- rollback is intentionally not exposed in the public frontend; it is a recovery/admin function, not part of the reviewer demo
- direct `SealGuard.upgrade()` calls are not available to reviewers; SealGuard accepts upgrades only from its registered SealKernel

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

The Python tooling follows the GenLayer project boilerplate branches used by this Studionet build: `genlayer-py@v0.18`, `genlayer-testing-suite@v0.29`, and `genvm-linter@main`.

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
