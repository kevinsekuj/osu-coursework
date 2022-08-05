#!/bin/csh
# num elements, local size

foreach ne ( 1024 4096 16384 65536 262144 1048576 2097152 4194304 8388608)
  foreach ls ( 32 64 256)
        g++ -o third third.cpp /usr/local/apps/cuda/10.1/lib64/libOpenCL.so.1.1 -lm -fopenmp -DNUM_ELEMENTS=$ne -DLOCAL_SIZE=$ls
    ./third
  end
end