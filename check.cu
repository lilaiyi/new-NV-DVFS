#include<stdio.h>
#include <assert.h>

// CUDA runtime
#include <cuda_runtime.h>

// Helper functions and utilities to work with CUDA




int main(){
cudaError_t x = (cudaError_t)46 ;
printf("cudaMalloc failed: %s\n", cudaGetErrorString(x));

}