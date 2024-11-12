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
    
    Find a nonce that produces a hash with k trailing zeros in binary representation.
    
    Args:
        k (int): Number of required trailing zeros
        prev_hash (bytes): Hash of the previous block
        rand_lines (list): List of strings representing transactions
    
    Returns:
        bytes: A nonce that produces a hash with k trailing zeros
    """
    if not isinstance(k, int) or k < 0:
        print("mine_block expects positive integer")
        return b'\x00'
        
    def check_trailing_zeros(hash_bytes, k):
        # Convert the last byte to binary and check trailing zeros
        binary_str = ''.join(format(b, '08b') for b in hash_bytes)
        return binary_str.endswith('0' * k)
        
    def combine_data(prev_hash, rand_lines, nonce):
        # Combine all data that needs to be hashed
        m = hashlib.sha256()
        m.update(prev_hash)
        for line in rand_lines:
            m.update(line.encode('utf-8'))
        m.update(nonce)
        return m.digest()
    
    nonce_counter = 0
    while True:
        # Convert counter to bytes with fixed width to ensure consistent hashing
        nonce = nonce_counter.to_bytes(32, byteorder='big')
        
        # Get the hash of combined data
        current_hash = combine_data(prev_hash, rand_lines, nonce)
        
        # Check if we found a valid nonce
        if check_trailing_zeros(current_hash, k):
            return nonce
            
        nonce_counter += 1


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