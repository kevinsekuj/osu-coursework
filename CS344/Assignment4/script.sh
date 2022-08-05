#!/bin/bash

./line_processor < input1.txt > out1.txt
./line_processor < input2.txt > out2.txt
./line_processor < input3.txt > out3.txt
./line_processor < mtp_grading_files/big_test > bigout
./line_processor < mtp_grading_files/newline_test > newlineout
./line_processor < mtp_grading_files/plus_test > plusout
./line_processor < mtp_grading_files/wrap_test > wrapout

diff out1.txt golden1.txt
diff out2.txt golden2.txt
diff out3.txt golden3.txt
diff bigout mtp_grading_files/big_soln
diff newlineout mtp_grading_files/newline_soln
diff plusout mtp_grading_files/plus_soln
diff wrapout mtp_grading_files/wrap_soln

echo "if nothing prints besides this then passed"