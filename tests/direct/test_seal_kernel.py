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
