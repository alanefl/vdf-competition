"""
Script that can be used to generate ground-truth pairs for random class group elements
and operations, or simply random class group elements.

Prints out lists of form "[inp1:inp2: ... :inpn]|out|< + or - >", where each inp and out can be integers or tuples (a, b, c).
The final "+" or "-" strings indicate whether the final result is a true ground-truth output or not. Most 
generated elements have the "+" label.

NOTE: this script is only meant to generate examples for testing purposes.
"""

import argparse
import random
from tqdm import tqdm
from inkfish.classgroup import ClassGroup

DISCRIMINANT = int("-30616069034807523947093657516320815215492876376165067902716988657802400037331914448218251590830\
1102189519215849430413184776658192481976276720778009261808832630304841711366872161223643645001916\
6969493423497224870506311710491233557329479816457723381368788734079933165653042145718668727765268\
0575673207678516369650123480826989387975548598309959486361425021860161020248607833276306314923730\
9854570972702350567411779734372573754840570138310317754359137013512655926325773048926718050691092\
9453371727344087286361426404588335160385998280988603297435639020911295652025967761702701701471162\
3966286152805654229445219531956098223")

MAX_EXP_BITS = 256

def print_output_format(inputs, output, truth):
    print("[%s]|%s|%s" % (':'.join([str(inp) for inp in inputs]), str(output), "+" if truth else "-"))

def get_rand_group_elems(n):
    g = ClassGroup.generator_for_discriminant(DISCRIMINANT)
    elems = []
    #print("Generating %d random group elements." % n)
    for _ in range(n):
        exp = random.getrandbits(MAX_EXP_BITS)
        new_elem = g ** exp
        elems.append(new_elem)
    return elems

def gen_op_gt(n):
    lhs = get_rand_group_elems(n)
    rhs = get_rand_group_elems(n)
    for lh, rh in zip(lhs, rhs):
        print_output_format([lh, rh], lh * rh, True)

def gen_normalize_gt(n):
    elems = get_rand_group_elems(3 * n)
    to_go = n
    while to_go > 0:
        mult = random.randint(1, int(n / 2))
        base = random.choice(elems)
        for _ in range(mult - 1):
            other = random.choice(elems)
            base = base.multiply(other, reduce=False)

        before = ClassGroup(base[0], base[1], base[2])
        after = base.normalized()

        if not ClassGroup.is_normal(before[0], before[1], before[2]) and ClassGroup.is_normal(after[0], after[1], after[2]):
            print_output_format([before], after, True)
            to_go -= 1

def gen_reduce_gt(n):
    elems = get_rand_group_elems(3 * n)
    to_go = n
    while to_go > 0:
        mult = random.randint(1, int(n / 2))
        base = random.choice(elems)
        for _ in range(mult - 1):
            other = random.choice(elems)
            base = base.multiply(other, reduce=False)

        before = ClassGroup(base[0], base[1], base[2])
        after = base.reduced()

        if not ClassGroup.is_reduced(before[0], before[1], before[2]) and ClassGroup.is_reduced(after[0], after[1], after[2]):
            print_output_format([before], after, True)
            to_go -= 1

def gen_square_gt(n):
    elems = get_rand_group_elems(n)
    for elem in elems:
        squared = elem.square()
        print_output_format([elem], squared, True)

def gen_exp_gt(n):
    elems = get_rand_group_elems(n)
    for elem in elems:
        exp = random.getrandbits(MAX_EXP_BITS)
        print_output_format([elem, exp], elem ** exp, True)

def gen_rand_elems(n):
    elems = get_rand_group_elems(n)
    for elem in elems:
        print(elem)

def main(args):
    num_examples = args.num_examples
    if args.procedure == "op":
        gen_op_gt(num_examples)
    elif args.procedure == "normalize":
        gen_normalize_gt(num_examples)
    elif args.procedure == "reduce":
        gen_reduce_gt(num_examples)
    elif args.procedure == "square":
        gen_square_gt(num_examples)
    elif args.procedure == "exp":
        gen_exp_gt(num_examples)
    elif args.procedure == 'rand_elems':
        gen_rand_elems(num_examples)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Classgroup Ground-truth Generator')
    parser.add_argument('--num_examples', default=10, type=int,
                        help='Number of ground-truth examples to generate')

    parser.add_argument(
        '--procedure', 
        choices=[
           'op', 'normalize', 'reduce', 'exp', 'square', 'rand_elems'
        ], 
        required=True
    )

    args = parser.parse_args()

    main(args)