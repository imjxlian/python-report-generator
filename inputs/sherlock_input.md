# Issue M-9: Attacker can fill merkle tree in `L2ToL1MessagePasser`, blocking any future withdrawals

Source: https://github.com/sherlock-audit/2024-08-morphl2-judging/issues/178

This issue has been acknowledged by the team but won't be fixed at this time.

## Found by
mstpr-brainbot, n4nika

### Summary
An attacker can fill the merkle tree used for withdrawals from `L2 -> L1`, preventing any withdrawals from `L2` to `L1`.

### Root Cause
The protocol uses one single merkle tree with a maximum of `2**32-1` entries for all ever happening withdrawals. Once that tree is full, any calls made to `L2CrossDomainMessenger.sol::_sendMessage` will fail, since [`Tree.sol::_appendMessageHash`](https://github.com/sherlock-audit/2024-08-morphl2/blob/98e0ec4c5bbd0b28f3d3a9e9159d1184bc45b38d/morph/contracts/contracts/libraries/common/Tree.sol#L34-L36), called in `L2ToL1MessagePasser.sol::appendMessage` will revert.

### Attack Path
* Attacker deploys a contract with a function which initiates `200` withdrawals from `L2` to `L1` per transaction by calling `l2CrossDomainMessenger.sendMessage(payable(0), 0, "", 0)` `200` times
* They then automate calling that contract as many times as it takes to fill the `2**32-1` entries of the withdrawal merkle tree in `Tree.sol` (`~21,000,000 times`)
* This fills the merkle tree and once it is full, any withdrawals are blocked permanently

Cost for a DoS with the lowest gas cost: `~51152 USD` at `2400 USD/ETH`

Note that this exploit takes some time to execute. However with the low gas costs and block times on L2, it is absolutely feasible to do so causing massive damage to the protocol. Additionally, if the ether price goes down, this will cost even less to execute.

# Issue M-11: In the `revertBatch` function, `inChallenge` is set to `false` incorrectly, causing challenges to continue after the protocol is paused

Source: https://github.com/sherlock-audit/2024-08-morphl2-judging/issues/220

## Found by
0xRajkumar, mstpr-brainbot, p0wd3r, ulas

### Summary
An unchecked batch reversion will cause challenge invalidation for any committed batch, leading to batch rollback issues for challengers, as the isChallenged flag will reset unexpectedly.

### Root Cause
In the [revertBatch function](https://github.com/sherlock-audit/2024-08-morphl2/blob/main/morph/contracts/contracts/l1/rollup/Rollup.sol#L345), the `inChallenge` state is set to false even if the batch that was challenged is not part of the reverted batch set. This causes ongoing challenges to be incorrectly invalidated:

```solidity
function revertBatch(bytes calldata _batchHeader, uint256 _count) external onlyOwner {
    // REDACTED FOR BREVITY ...
    if (!challenges[_batchIndex].finished) {
        batchChallengeReward[challenges[_batchIndex].challenger] += challenges[_batchIndex].challengeDeposit;
        inChallenge = false;
    }
    // REDACTED FOR BREVITY ...
}
```

In the above code, `if (!challenges[_batchIndex].finished)` will hold `true` for challenges that doesn't exist. If there are no challenges for a specific `_batchIndex`, then `challenges[_batchIndex].finished` will be `false` which in turn will make the `if` condition true.