# this is a file to store our different prompts that we try out, here is a quick example that can be updated
CoT = """
Given the smart contract and a list of already found weaknesses find a new weakness that hasn't been found in the smart contract. Output it in json format like below:

Input:
Smart Contract: <input example smart contract>
Weaknesses found: []

Weakness found and reasoning: 
Output: {{weakness_found: "", reasoning: ""}}

Smart Contract: {code}

Weaknesses found: {weaknesses}

If there are no more weaknesses within the smart contract output {{weakness_found: false, reasoning: false}}
Output: {{weakness_found: "", reasoning: ""}}
"""

meta = """
You are a Smart Contract Auditor whose purpose is to identify CWE weaknesses within smart contracts. 
As input you will be given a list of weakensses already found and smart contract code. For identifying weaknesses let's break down the process step by step:
1. Scan through the given smart contract code
2. Scan through the given weaknesses
3. If one exists identify a weakness within the smart contract that does not match the CWEs already found
4. Give a reasoning as to where this weakness is present and how it is a weakness within the code
5. Output the information in JSON format as so: {{weakness_found: "", reasoning: ""}}
6. If no new weakness is found just output in JSON format with each value being false this: {{weakness_found: false, reasoning: false}}

Smart Contract: {code}
Weaknesses found: {weaknesses}
"""

n_shot = """
You are a smart contract auditor whose purpose is to identify CWE weaknesses within a smart contract. As input there is a smart contract and a list of weaknesses that have already been identified. Your job is to look through the smart contract and see if there is a new weakness that has not been identified.
There may be instances where no new weakness is found. Please output in the JSON format shown below.

Here are 3 examples of input and output:
Input:
Smart contract: <input example code>
Weaknesses found: <input example list>

Output: {{weakness_found: "<input weakness>", reasoning: "input reasoning>"}}

Input:
Smart contract: <input example code>
Weaknesses found: <input example list>

Output: {{weakness_found: "<input weakness>", reasoning: "input reasoning>"}}

Input:
Smart contract: function executeFlashLoan(uint amount) public { token.transfer(msg.sender, amount); require(token.balanceOf(address(this)) >= amount); }
Weaknesses found: ['CWE-20']

Output: {{weakness_found: "CWE-200", reasoning: "Flash loan allows market manipulation, exploiting loan logic."}}

Input:
Smart contract: {code}
Weaknesses found: {weaknesses}

Output: 
"""

# taken from GPT Lens, we should update it to use prompt chaining
open_ended = """
You are a smart contract auditor, identify and explain severe vulnerabilities in the provided smart contract. Make sure that they are exploitable in real world and beneficial to attackers. Provide each identified vulnerability with intermediate reasoning and its associated function. Remember, you must provide the entire function code and do not use "...". Make your reasoning comprehensive and detailed. Smart contract code: {code}\n\n
"""

# {"id":"SCV-018","category":"Access Control","code_snippet":"function pauseContract() public { paused = true; }","vulnerable":true,"poc":"contract Attack { function exploit(address target) public { AccessControl(target).pauseContract(); } }","description":"Lack of access control allows any user to pause the contract, disrupting operations.","source_links":"https://owasp.org/www-project-smart-contract-top-ten","cve":"CVE-2021-32679","resource":"OWASP Smart Contract Top 10 2025","severity":"High"}
# CWE 116


# {"id":"SCV-023","category":"Access Control","code_snippet":"function changeRate(uint newRate) public { rate = newRate; }","vulnerable":true,"poc":"contract Attack { function exploit(address target) public { AccessControl(target).changeRate(1000); } }","description":"No access control allows any user to modify critical rates, affecting contract economics.","source_links":"https://owasp.org/www-project-smart-contract-top-ten","cve":"CVE-2021-32680","resource":"OWASP Smart Contract Top 10 2025","severity":"High"}
# CWE 778


# {"id":"SCV-043","category":"Access Control","code_snippet":"function setFee(uint newFee) public { fee = newFee; }","vulnerable":true,"poc":"contract Attack { function exploit(address target) public { AccessControl(target).setFee(1000); } }","description":"No access control allows any user to modify the fee, affecting contract economics.","source_links":"https://owasp.org/www-project-smart-contract-top-ten","cve":"CVE-2021-32684","resource":"OWASP Smart Contract Top 10 2025","severity":"High"}
# CWE 670


# {"id":"SCV-048","category":"Access Control","code_snippet":"function updateConfigValue(uint newValue) public { configValue = newValue; }","vulnerable":true,"poc":"contract Attack { function exploit(address target) public { AccessControl(target).updateConfigValue(9999); } }","description":"No access restrictions allow any user to modify critical configurations, disrupting contract behavior.","source_links":"https://owasp.org/www-project-smart-contract-top-ten","cve":"CVE-2021-32685","resource":"OWASP Smart Contract Top 10 2025","severity":"High"}
# CWE 347


# {"id":"SCV-053","category":"Flash Loan Attacks","code_snippet":"function flashLoan(uint amount) public { token.transfer(msg.sender, amount); require(token.balanceOf(address(this)) >= amount); }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FlashLoan(target).flashLoan(amount); manipulateMarket(); } }","description":"Flash loan allows borrowing large tokens to manipulate contract state, exploiting price changes in one transaction.","source_links":"https://www.nature.com/articles/s41598-024-604503","cve":"CVE-2021-32686","resource":"Scientific Reports 2025","severity":"Medium"}
# CWE 362


# {"id":"SCV-062","category":"Front-Running","code_snippet":"function placeBid(uint amount) public { bids[msg.sender] = amount; }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FrontRun(target).placeBid(amount + 1); } }","description":"Public bid function allows miners or bots to front-run transactions, outbidding legitimate users.","source_links":"https://www.resonance.security/owasp-sc-top-10-2025","cve":"CVE-2021-32687","resource":"Resonance Security 2025","severity":"Medium"}
# CWE 190 (known)
# CWE 680



# {"id":"SCV-069","category":"Flash Loan Attacks","code_snippet":"function executeTrade(uint amount) public { token.transfer(msg.sender, amount); require(token.balanceOf(address(this)) >= amount); }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FlashLoan(target).executeTrade(amount); manipulatePrice(); } }","description":"Flash loan enables market manipulation within a single transaction, exploiting trade logic.","source_links":"https://www.nature.com/articles/s41598-025-604503","cve":"CVE-2021-32688","resource":"Scientific Reports 2025","severity":"Medium"}
# CWE-285


# {"id":"SCV-099","category":"Flash Loan Attacks","code_snippet":"function arbitrage(uint amount) public { token.transfer(msg.sender, amount); require(token.balanceOf(address(this)) >= amount); }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FlashLoan(target).arbitrage(amount); manipulateMarket(); } }","description":"Flash loan enables arbitrage manipulation, exploiting pricing flaws in a single transaction.","source_links":"https://www.nature.com/articles/s41598-025-604503","cve":"CVE-2021-32694","resource":"Scientific Reports 2025","severity":"Medium"}
# CWE 248

# {"id":"SCV-104","category":"Flash Loan Attacks","code_snippet":"function borrowTokens(uint amount) public { token.transfer(msg.sender, amount); require(token.balanceOf(address(this)) >= amount); }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FlashLoan(target).borrowTokens(amount); manipulateMarket(); } }","description":"Flash loan allows borrowing large tokens to manipulate market prices within a transaction.","source_links":"https://www.nature.com/articles/s41598-025-604503","cve":"CVE-2021-32695","resource":"Scientific Reports 2025","severity":"Medium"}
# CWE 200

# {"id":"SCV-119","category":"Flash Loan Attacks","code_snippet":"function executeLoan(uint amount) public { token.transfer(msg.sender, amount); require(token.balanceOf(address(this)) >= amount); }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FlashLoan(target).executeLoan(amount); manipulateMarket(); } }","description":"Flash loan allows market manipulation within a transaction, exploiting loan logic.","source_links":"https://www.nature.com/articles/s41598-025-604503","cve":"CVE-2021-32697","resource":"Scientific Reports 2025","severity":"Medium"}
# CWE 20

# {"id":"SCV-134","category":"Flash Loan Attacks","code_snippet":"function flashBorrow(uint amount) public { token.transfer(msg.sender, amount); require(token.balanceOf(address(this)) >= amount); }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FlashLoan(target).flashBorrow(amount); manipulateMarket(); } }","description":"Flash loan allows market manipulation, exploiting pricing logic.","source_links":"https://www.nature.com/articles/s41598-025-604503","cve":"CVE-2021-32699","resource":"Scientific Reports 2025","severity":"Medium"}
# CWE 400

# {"id":"SCV-142","category":"Front-Running","code_snippet":"function placeBet(uint amount) public { bets[msg.sender] = amount; }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FrontRun(target).placeBet(amount + 1); } }","description":"Public betting allows front-running, enabling attackers to outbid users.","source_links":"https://www.resonance.security/owasp-sc-top-10-2025","cve":"CVE-2021-32700","resource":"Resonance Security 2025","severity":"Medium"}
# CWE 306

# {"id":"SCV-194","category":"Flash Loan Attacks","code_snippet":"function executeFlashLoan(uint amount) public { token.transfer(msg.sender, amount); require(token.balanceOf(address(this)) >= amount); }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FlashLoan(target).executeFlashLoan(amount); manipulateMarket(); } }",
#  "description":"Flash loan allows market manipulation, exploiting loan logic.","source_links":"https://www.nature.com/articles/s41598-025-604503","cve":"CVE-2021-32707","resource":"Scientific Reports 2025","severity":"Medium"}
# CWE 20
# CWE 200 (for n-shot)

# {"id":"SCV-512","category":"Front-Running","code_snippet":"function submitOrder(uint amount) public { orders[msg.sender] = amount; }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FrontRun(target).submitOrder(amount + 1); } }","description":"Public order submission allows front-running, enabling outbidding.","source_links":"https://www.resonance.security/owasp-sc-top-10-2025","cve":"CVE-2021-32748","resource":"Resonance Security 2025","severity":"Medium"}
# CWE 862

# {"id":"SCV-604","category":"Flash Loan Attacks","code_snippet":"function borrow(uint amount) public { token.transfer(msg.sender, amount); require(token.balanceOf(address(this)) >= amount); }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FlashLoan(target).borrow(amount); manipulateMarket(); } }","description":"Flash loan enables market manipulation, exploiting borrow logic.","source_links":"https://www.nature.com/articles/s41598-025-604503","cve":"CVE-2021-32760","resource":"Scientific Reports 2025","severity":"Medium"}
# CWE 668

# {"id":"SCV-756","category":"Front-Running","code_snippet":"function submitTrade(uint amount) public { trades[msg.sender] = amount; }","vulnerable":true,"poc":"contract Attack { function exploit(address target, uint amount) public { FrontRun(target).submitTrade(amount + 1); } }","description":"Public trade submission allows front-running, enabling outbidding.","source_links":"https://www.resonance.security/owasp-sc-top-10-2025","cve":"CVE-2021-32780","resource":"Resonance Security 2025","severity":"Medium"}
# CWE 754