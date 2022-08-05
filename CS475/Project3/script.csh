#!/bin/csh

foreach t ( 1 2 4 8 12 16 20 24)
  foreach n ( 2 4 8 16 32 64 128 256 512 1024)
        g++ -O3   functionaldecomposition.cpp  -DNUMT=$t -DNUMNODES=$n  -o functionaldecomposition  -lm  -fopenmp
    ./functionaldecomposition
  end
end