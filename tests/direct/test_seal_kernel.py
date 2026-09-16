def test_kernel_starts_unbound(direct_deploy):
    kernel = direct_deploy("contracts/seal_kernel.py")
    state = kernel.get_state()
    assert "guard_address=" in state
    assert "MutaSeal mutation constitution v1" in state


def test_only_owner_can_register_guard(direct_vm, direct_deploy, direct_bob):
    kernel = direct_deploy("contracts/seal_kernel.py")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Only owner"):
        kernel.register_guard("0x1111111111111111111111111111111111111111")


def test_guard_can_only_be_registered_once(direct_vm, direct_deploy, direct_alice):
    kernel = direct_deploy("contracts/seal_kernel.py")
    direct_vm.sender = direct_alice
    kernel.register_guard("0x1111111111111111111111111111111111111111")
    with direct_vm.expect_revert("Guard already registered"):
        kernel.register_guard("0x2222222222222222222222222222222222222222")


def test_register_guard_rejects_bad_address(direct_vm, direct_deploy, direct_alice):
    kernel = direct_deploy("contracts/seal_kernel.py")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("Guard address is invalid"):
        kernel.register_guard("not-an-address")


def test_evolve_rejects_short_sample_before_external_call(direct_vm, direct_deploy, direct_alice):
    kernel = direct_deploy("contracts/seal_kernel.py")
    direct_vm.sender = direct_alice
    kernel.register_guard("0x1111111111111111111111111111111111111111")
    with direct_vm.expect_revert("Attack sample must be 4..1200 characters"):
        kernel.evolve("x")
