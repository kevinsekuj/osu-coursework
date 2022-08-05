/* HEADERS */
#include <omp.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#ifndef _OPENMP
fprintf(stderr, "NO OPEN MP SUPPORT\n");
return 1;
#endif

/* CONSTANTS */
const float GRAIN_GROWS_PER_MONTH = 9.0;
const float ONE_DEER_EATS_PER_MONTH = 1.0;

const float AVG_PRECIP_PER_MONTH = 7.0; // average
const float AMP_PRECIP_PER_MONTH = 6.0; // plus or minus
const float RANDOM_PRECIP = 2.0;        // plus or minus noise

const float AVG_TEMP = 60.0;    // average
const float AMP_TEMP = 20.0;    // plus or minus
const float RANDOM_TEMP = 10.0; // plus or minus noise

const float MIDTEMP = 40.0;
const float MIDPRECIP = 10.0;

/* GLOBALS */
int NowYear;       // 2022 - 2027
int NowMonth;      // 0 - 11
float NowPrecip;   // inches of rain per month
float NowTemp;     // temperature this month
float NowHeight;   // grain height in inches
int NowNumDeer;    // number of deer in the current population
int NowNumHunters; // number of hunters in the current population
unsigned int seed = 0;

/* PROTOTYPES */
void Deer();
void Grain();
void Watcher();
void Hunters();
float Ranf(unsigned int *seedp, float low, float high);
int Ranf(unsigned int *seedp, int ilow, int ihigh);
float SQR(float x);

int main(int argc, char const *argv[])
{
  // starting date and time:
  NowMonth = 0;
  NowYear = 2022;

  // starting state (feel free to change this if you want):
  NowNumDeer = 1;
  NowHeight = 1.;
  NowNumHunters = 1;
  NowPrecip = 1.;

  omp_set_num_threads(4); // same as # of sections
#pragma omp parallel sections
  {
#pragma omp section
    {
      Deer();
    }

#pragma omp section
    {
      Grain();
    }

#pragma omp section
    {
      Watcher();
    }

#pragma omp section
    {
      Hunters(); // your own
    }
}
}

void Deer()
{
  while (NowYear < 2028)
  {
    // compute a temporary next-value for this quantity
    // based on the current state of the simulation:
    int nextNumDeer = NowNumDeer;
    int carryingCapacity = (int)(NowHeight);

    if (nextNumDeer < carryingCapacity)
      nextNumDeer++;

    else if (nextNumDeer > carryingCapacity)
      nextNumDeer--;

    if (NowNumHunters > nextNumDeer)
      nextNumDeer--;

    if (nextNumDeer < 0)
      nextNumDeer = 0;

// DoneComputing barrier:
#pragma omp barrier
    NowNumDeer = nextNumDeer;

// DoneAssigning barrier:
#pragma omp barrier

// DonePrinting barrier:
#pragma omp barrier
  }
}

void Grain()
{
  while (NowYear < 2028)
  {
    // compute a temporary next-value for this quantity
    // based on the current state of the simulation:
    float tempFactor = exp(-SQR((NowTemp - MIDTEMP) / 10.));
    float precipFactor = exp(-SQR((NowPrecip - MIDPRECIP) / 10.));

    float nextHeight = NowHeight;
    nextHeight += tempFactor * precipFactor * GRAIN_GROWS_PER_MONTH;
    nextHeight -= (float)NowNumDeer * ONE_DEER_EATS_PER_MONTH;

    if (nextHeight < 0.)
      nextHeight = 0.;

// DoneComputing barrier:
#pragma omp barrier
    NowHeight = nextHeight;

// DoneAssigning barrier:
#pragma omp barrier

// DonePrinting barrier:
#pragma omp barrier
  }
}

void Watcher()
{
  while (NowYear < 2028)
  {
    // compute a temporary next-value for this quantity
    // based on the current state of the simulation:
// DoneComputing barrier:
#pragma omp barrier

    // DoneAssigning barrier:

#pragma omp barrier
    fprintf(stderr, "%d, %f, %f, %f, %d, %d\n", NowMonth, NowTemp, NowPrecip, NowHeight,
            NowNumDeer, NowNumHunters);

    NowMonth++;
    if (NowMonth % 12 == 0)
    {
      NowYear++;
      NowMonth = 0;
    }

    float ang = (30. * (float)NowMonth + 15.) * (M_PI / 180.);

    float temp = AVG_TEMP - AMP_TEMP * cos(ang);
    NowTemp = temp + Ranf(&seed, -RANDOM_TEMP, RANDOM_TEMP);

    float precip = AVG_PRECIP_PER_MONTH + AMP_PRECIP_PER_MONTH * sin(ang);
    NowPrecip = precip + Ranf(&seed, -RANDOM_PRECIP, RANDOM_PRECIP);
    if (NowPrecip < 0.)
      NowPrecip = 0.;

// DonePrinting barrier:
#pragma omp barrier
  }
}

void Hunters()
{
  while (NowYear < 2028)
  {
    // compute a temporary next-value for this quantity
    // based on the current state of the simulation:

    int nextNumHunter = NowNumHunters;

    if (nextNumHunter > NowNumDeer)
      nextNumHunter--;

    else if (nextNumHunter < NowNumDeer)
      nextNumHunter++;

    if (nextNumHunter < 0)
      nextNumHunter = 0;

// DoneComputing barrier:
#pragma omp barrier
    NowNumHunters = nextNumHunter;

// DoneAssigning barrier:
#pragma omp barrier

// DonePrinting barrier:
#pragma omp barrier
  }
}

float Ranf(unsigned int *seedp, float low, float high)
{
  float r = (float)rand_r(seedp); // 0 - RAND_MAX

  return (low + r * (high - low) / (float)RAND_MAX);
}

int Ranf(unsigned int *seedp, int ilow, int ihigh)
{
  float low = (float)ilow;
  float high = (float)ihigh + 0.9999f;

  return (int)(Ranf(seedp, low, high));
}

float SQR(float x)
{
  return x * x;
}