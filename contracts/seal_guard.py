# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class SealGuard(gl.Contract):
    kernel_address: str
    generation: u64
    genes: str
    previous_genes: str
    last_upgrade_reason: str
    last_attack: str
    history: str
    total_recorded_checks: u64
    blocked_recorded_checks: u64

    def __init__(self, kernel_address: str):
        self.kernel_address = kernel_address
        self.generation = u64(1)
        self.genes = "BASIC_OVERRIDE"
        self.previous_genes = ""
        self.last_upgrade_reason = "GENESIS"
        self.last_attack = ""
        self.history = "g1:BASIC_OVERRIDE:GENESIS"
        self.total_recorded_checks = u64(0)
        self.blocked_recorded_checks = u64(0)

        root = gl.storage.Root.get()
        root.upgraders.get().append(Address(kernel_address))

    def _evaluate(self, text: str) -> str:
        t = text.lower()
        if "ignore previous instructions" in t or "ignore all previous instructions" in t:
            return "BLOCK:BASIC_OVERRIDE"
        return "ALLOW"

    @gl.public.view
    def check(self, text: str) -> str:
        return self._evaluate(text)

    @gl.public.write
    def record_check(self, text: str) -> str:
        self.total_recorded_checks = self.total_recorded_checks + u64(1)
        result = self._evaluate(text)
        if result.startswith("BLOCK:"):
            self.blocked_recorded_checks = self.blocked_recorded_checks + u64(1)
        return result

    @gl.public.view
    def get_generation(self) -> u64:
        return self.generation

    @gl.public.view
    def get_genes(self) -> str:
        return self.genes

    @gl.public.view
    def get_previous_genes(self) -> str:
        return self.previous_genes

    @gl.public.view
    def get_state(self) -> str:
        return (
            "generation=" + str(self.generation)
            + "\ngenes=" + self.genes
            + "\nprevious_genes=" + self.previous_genes
            + "\nlast_upgrade_reason=" + self.last_upgrade_reason
            + "\nlast_attack=" + self.last_attack
            + "\ntotal_recorded_checks=" + str(self.total_recorded_checks)
            + "\nblocked_recorded_checks=" + str(self.blocked_recorded_checks)
            + "\nhistory=" + self.history
        )

    @gl.public.write
    def upgrade(
        self,
        new_code: bytes,
        new_generation: u64,
        new_genes: str,
        reason: str,
        attack_sample: str,
    ) -> None:
        if gl.message.sender_address != Address(self.kernel_address):
            raise gl.vm.UserError("Only SealKernel can upgrade SealGuard")

        self.previous_genes = self.genes
        self.generation = new_generation
        self.genes = new_genes
        self.last_upgrade_reason = reason
        self.last_attack = attack_sample
        self.history = (
            self.history
            + "||g" + str(new_generation)
            + ":" + new_genes
            + ":" + reason
        )

        root = gl.storage.Root.get()
        code = root.code.get()
        code.truncate()
        code.extend(new_code)
