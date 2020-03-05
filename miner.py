import json
import hashlib

def proof_of_work(last_block, difficulty):


    # last block to json
    lb_json = json.dumps(last_block, sort_keys=True)

    proof = 0

    while valid_proof(lb_json, proof, difficulty) is False:

        proof += 1 

    return proof

def valid_proof(lb_json, proof, difficulty):

    guess = f"{lb_json}{proof}".encode()

    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:difficulty] == "0" * difficulty


print(proof_of_work(37777907, 6))