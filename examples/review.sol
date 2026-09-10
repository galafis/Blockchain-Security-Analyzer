// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Synthetic source-review exercise. No deployment or assets.
contract ReviewExercise {
    uint256 public count;
    function update() external {
        count += 1;
        if (block.timestamp > 2000000000) {
            count += 2;
        }
    }
}
