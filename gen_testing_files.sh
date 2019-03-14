# Uses reference classgroups implementation to
# generate input/ground-truth files for op, normalize, reduce, square, exp,
# as well as ga list of random group elements.


python3 elem_generator.py --num_examples 250 --procedure op > op.out
python3 elem_generator.py --num_examples 250 --procedure normalize > normalize.out
python3 elem_generator.py --num_examples 250 --procedure reduce > reduce.out
python3 elem_generator.py --num_examples 250 --procedure square > square.out
python3 elem_generator.py --num_examples 250 --procedure exp > exp.out
python3 elem_generator.py --num_examples 1000 --procedure rand_elems > rand_elems.out
