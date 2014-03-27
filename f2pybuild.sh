#!/bin/sh

f2py -c  -m JT65   decode_rs.c encode_rs.c init_rs.c wrapkarn.c JT65code_all.f 

