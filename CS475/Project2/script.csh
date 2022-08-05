#!/bin/csh

foreach t ( 1 2 4 8 12 16 20 24)
  foreach n ( 2 4 8 16 32 64 128 256 512 1024)
        g++ -O3   numericintegration.cpp  -DNUMT=$t -DNUMNODES=$n  -o numericintegration  -lm  -fopenmp
    ./numericintegration
  end
end