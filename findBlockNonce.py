#!/bin/python
import hashlib
import os
import random


def mine_block(k, prev_hash, rand_lines):
    """
    k - Number of trailing zeros in the binary representation (integer)
    prev_hash - the hash of the previous block (bytes)
    rand_lines - a set of "transactions," i.e., data to be included in this block (list of strings)

    Complete this function to find a nonce such that 
    sha256( prev_hash + rand_lines + nonce )
    has k trailing zeros in its *binary* representation
    """
    if not isinstance(k, int) or k < 0:
        print("mine_block expects positive integer")
        return b'\x00'
        
    def zero_check(hash_result, zeros_needed):
        # Get binary string and look for trailing zeros
        bits = ''.join(bin(x)[2:].zfill(8) for x in hash_result)
        return bits.endswith('0' * zeros_needed)
        
    def hash_everything(block_prev, tx_lines, try_nonce):
        # Hash concatenation of previous block, transactions and nonce
        mixer = hashlib.sha256()
        mixer.update(block_prev)
        for tx in tx_lines:
            mixer.update(tx.encode('utf-8'))
        mixer.update(try_nonce)
        return mixer.digest()
    
    attempt = 0
    while True:
        # Pack current attempt as bytes
        test_nonce = attempt.to_bytes(32, byteorder='big')
        
        # Try this nonce
        result = hash_everything(prev_hash, rand_lines, test_nonce)
        
        # Found valid nonce?
        if zero_check(result, k):
            return test_nonce
            
        attempt += 1


def get_random_lines(filename, quantity):
    """
    This is a helper function to get the quantity of lines ("transactions")
    as a list from the filename given. 
    Do not modify this function
    """
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())

    random_lines = []
    for x in range(quantity):
        random_lines.append(lines[random.randint(0, quantity - 1)])
    return random_lines


if __name__ == '__main__':
    # This code will be helpful for your testing
    filename = "bitcoin_text.txt"
    num_lines = 10  # The number of "transactions" included in the block

    # The "difficulty" level. For our blocks this is the number of Least Significant Bits
    # that are 0s. For example, if diff = 5 then the last 5 bits of a valid block hash would be zeros
    # The grader will not exceed 20 bits of "difficulty" because larger values take to long
    diff = 20

    rand_lines = get_random_lines(filename, num_lines)
    nonce = mine_block(diff, rand_lines)
    print(nonce)
