# this is a file to store our different prompts that we try out, here is a quick example that can be updated
meta = """
You are a Smart Contract Auditor whose purpose is to identify CWE weaknesses within smart contracts. 
As input you will be given a list of weakensses already found and smart contract code. For identifying weaknesses let's break down the process step by step:

1. Scan through the given smart contract code
2. Within the code identify what the functions do and how they interact with each other
3. Identify any parts of the code that may lead to a weakness or vulnerability 
4. If one exists identify a weakness within the smart contract that does not match the CWEs already found
5. Give a reasoning as to where this weakness is present and how it is a weakness within the code
6. Output the information in JSON format as so with no other information: {{weakness_found: "", reasoning: ""}}
7. If no new weakness is found just output in JSON format with each value being false this: {{weakness_found: null, reasoning: "no new weakness found"}}

Smart Contract: {code}
Weaknesses found: {weaknesses}

Output:{{weakness_found: "", reasoning: ""}} 
"""

CoT = """
You are a smart contract auditor whose purpose is to identify CWE weaknesses within smart contracts. You are to find only one CWE weakness at a time. Given the smart contract and a list of already found weaknesses find a new weakness that hasn't been found in the smart contract. Output it in json format like below:

Input:
Smart Contract: "```\\nif  (vAssets.borrowAsset == FTM) {{ \\n    require(msg.value >= debtTotal, Errors.VL_AMOUNT_ERROR);\\n else {{\\n    //...\\n```"
Weaknesses found: ["CWE-754"]

Weakness found and reasoning:
There is a weakness present where if a user provides more 'FTM' tokens than the required 'debtTotal' amount, the remaining tokens are not returned to the user. Since the contract is not upgradeable and this issue can't be fixed then the related CWE is CWE-1329.
Output: {{"weakness_found": "CWE-1329", "reasoning": "The contract does not return excess FTM tokens to the user if they provide more than the required debtTotal amount, leading to a loss of funds for the user. This contract is not upgradeable, so this issue cannot be fixed leading to a weakness of relying on non upgradeable contracts, or CWE-1329 "Reliance on componenent that is not updateable"}}


Smart Contract: {code}
Weaknesses found: {weaknesses}

If there are no more weaknesses within the smart contract output {{weakness_found: null, reasoning: "no new weakness found"}}, make sure to only output the json string and nothing else.
Output: {{weakness_found: "", reasoning: ""}}
"""

n_shot = """
You are a smart contract auditor whose purpose is to identify CWE weaknesses within a smart contract. As input there is a smart contract and a list of weaknesses that have already been identified. Your job is to look through the smart contract and see if there is a new weakness that has not been identified.
There may be instances where no new weakness is found. Please output in the JSON format shown below and don't output anything else.

Here are 3 examples of input and output:
Input:
Smart contract: "```\\nfunction incentivize(\\n    address sender,\\n    address receiver,\\n    address operator,\\n    uint amountIn\\n) external override onlyFei {{\\n    updateOracle();\\n\\n    if (isPair(sender)) {{\\n        incentivizeBuy(receiver, amountIn);\\n    }}\\n\\n    if (isPair(receiver)) {{\\n        require(\\n            isSellAllowlisted(sender) || isSellAllowlisted(operator),\\n            \"UniswapIncentive: Blocked Fei sender or operator\"\\n        );\\n        incentivizeSell(sender, amountIn);\\n    }}\\n}}\\n```\\n```\\nfunction incentivizeBuy(address target, uint amountIn) internal {{\\n    if (isExemptAddress(target)) {{\\n        return;\\n    }}\\n\\n    (uint incentive, uint32 weight,\\n    Decimal.D256 memory initialDeviation,\\n    Decimal.D256 memory finalDeviation) = getBuyIncentive(amountIn);\\n\\n    updateTimeWeight(initialDeviation, finalDeviation, weight);\\n    if (incentive!= 0) {{\\n        fei().mint(target, incentive);\\n    }}\\n}}\\n```\\n```\\nfunction getBuyIncentive(uint amount) public view override returns (\\n    uint incentive,\\n    uint32 weight,\\n    Decimal.D256 memory initialDeviation,\\n    Decimal.D256 memory finalDeviation\\n) {{\\n    (\\n        initialDeviation,\\n        finalDeviation\\n    ) = getPriceDeviations(-1 * int256(amount));\\n}}\\n```"
Weaknesses found: []

Output: {{weakness_found: "CWE-190", reasoning: "The UniswapIncentive contract’s ‘incentivize’ function contains an integer overflow weakness, CWE-190, since there are unchecked operations in the ‘getBuyIncentive’ function. The ‘getBuyIncentive’ function calculates the buy incentive by casting the ‘amount’ parameter to an ‘int256’ and then performing arithmetic operations on it. However if the ‘amount’ is large enough the cast can overflow, leading to incorrect calculations and potentially allowing an attacker to mint tokens before transferring them. The `getBuyIncentive` function is called by the `incentivizeBuy` function, which then uses the calculated incentive to mint tokens from the target address. If the incentive calculation is incorrect due to an overflow, the minting operation may result in unintended consequences, such as minting tokens before transferring them. The weakness is present in the `getBuyIncentive` function's calculation of price deviations, where the `amount` is cast to an `int256` and then used in arithmetic operations. This can lead to an overflow if the `amount` is large enough, resulting in incorrect calculations and potential token minting before transfer."}}

Input:
Smart contract: "```\\nfunction transferFrom(\\n    address sender,\\n    address recipient,\\n    uint256 amount\\n) external override returns (bool) {{\\n    address spender = msg.sender;\\n    //check allowance requirement\\n    _spendAllowance(sender, spender, amount);\\n    return _transferFrom(sender, recipient, amount);\\n}}\\n```\\n"
Weaknesses found: []

Output: {{weakness_found: null, reasoning: "no new weakness found"}}

Input:
Smart contract: "```\\nif (vAssets.borrowAsset == FTM) {{\\n    require(msg.value >= debtTotal, Errors.VL_AMOUNT_ERROR);\\n}} else {{\\n    //...\\n```"
Weaknesses found: ["CWE-1329"]

Output: {{weakness_found: "CWE-754", reasoning: "This function has a weakness where funds loss can occur when processing transactions involving the native token 'FMT'. If a caller provides more 'FMT' tokens than the required 'debtTotal' amount the excess funds are not returned to the caller. This is related to CWE-754 as this function is not checking extra edge cases in where the caller gives more funds than necessary"}}

Input:
Smart contract: {code}
Weaknesses found: {weaknesses}

Output: {{weakness_found: "", reasoning: ""}}
"""

# taken from GPT Lens, we should update it to use prompt chaining
open_ended = """
You are a smart contract auditor whose purpose is to identify CWE weaknesses within smart contracts. 
You will be given a smart contract code and a list of already identified weaknesses. 
Your task is to analyze the smart contract and identify one new weakness that hasn't been identified yet. 
You should output your findings in the JSON format as so {{weakness_found: "", reasoning: ""}}. If no new weakness is found, output {{weakness_found: null, reasoning: "no new weakness found"}}.
Make sure to output just the JSON string and nothing else.

Input:
Smart Contract: {code}
Weaknesses found: {weaknesses}  

Output: {{weakness_found: "", reasoning: ""}}
"""