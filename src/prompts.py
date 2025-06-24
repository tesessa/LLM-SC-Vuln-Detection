# this is a file to store our different prompts that we try out, here is a quick example that can be updated


CoT = """

"""

meta = """

"""

# taken from GPT Lens, we should update it to use prompt chaining
open_ended = """
You are a smart contract auditor, identify and explain severe vulnerabilities in the provided smart contract. Make sure that they are exploitable in real world and beneficial to attackers. Provide each identified vulnerability with intermediate reasoning and its associated function. Remember, you must provide the entire function code and do not use "...". Make your reasoning comprehensive and detailed. Smart contract code: {code}\n\n
"""