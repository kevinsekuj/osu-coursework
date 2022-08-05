#include <stdio.h>
#define _USE_MATH_DEFINES
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

// print debugging messages?
#ifndef DEBUG
#define DEBUG	false
#endif

// setting the number of threads:
#ifndef NUMT
#define NUMT		    2
#endif

// setting the number of trials in the monte carlo simulation:
#ifndef NUMTRIALS
#define NUMTRIALS	50000
#endif

// how many tries to discover the maximum performance:
#ifndef NUMTRIES
#define NUMTRIES	20
#endif

// ranges for the random numbers:
const float TX_MIN = -10;
const float TX_MAX = 10;
const float TXV_MIN = 10;
const float TXV_MAX = 30;
const float TY_MIN = 45;
const float TY_MAX = 55;
const float SV_MIN = 10;
const float SV_MAX = 30;
const float STH_MIN = 10;
const float STH_MAX = 90;

// degrees-to-radians:
inline
float Radians( float d )
{
    return (M_PI/180.f) * d;
}


float
Ranf( float low, float high )
{
    float r = (float) rand();               // 0 - RAND_MAX
    float t = r  /  (float) RAND_MAX;       // 0. - 1.

    return   low  +  t * ( high - low );
}

int
Ranf( int ilow, int ihigh )
{
    float low = (float)ilow;
    float high = ceil( (float)ihigh );

    return (int) Ranf(low,high);
}

// call this if you want to force your program to use
// a different random number sequence every time you run it:
void
TimeOfDaySeed( )
{
    struct tm y2k = { 0 };
    y2k.tm_hour = 0;   y2k.tm_min = 0; y2k.tm_sec = 0;
    y2k.tm_year = 100; y2k.tm_mon = 0; y2k.tm_mday = 1;

    time_t  timer;
    time( &timer );
    double seconds = difftime( timer, mktime(&y2k) );
    unsigned int seed = (unsigned int)( 1000.*seconds );    // milliseconds
    srand( seed );
}


int
main( int argc, char *argv[ ] ) {
#ifndef _OPENMP
    fprintf(stderr, "No OpenMP support!\n");
    return 1;
#endif

    TimeOfDaySeed();               // seed the random number generator

    omp_set_num_threads(NUMT);    // set the number of threads to use in parallelizing the for-loop:`

    // better to define these here so that the rand() calls don't get into the thread timing:
    float *txs = new float[NUMTRIALS];
    float *tys = new float[NUMTRIALS];
    float *txvs = new float[NUMTRIALS];
    float *svs = new float[NUMTRIALS];
    float *sths = new float[NUMTRIALS];

    // fill the random-value arrays:
    for (int n = 0; n < NUMTRIALS; n++) {
        txs[n] = Ranf(TX_MIN, TX_MAX);
        tys[n] = Ranf(TY_MIN, TY_MAX);
        txvs[n] = Ranf(TXV_MIN, TXV_MAX);
        svs[n] = Ranf(SV_MIN, SV_MAX);
        sths[n] = Ranf(STH_MIN, STH_MAX);
    }

    // get ready to record the maximum performance and the probability:
    double maxPerformance = 0.;    // must be declared outside the NUMTRIES loop
    int numHits;                // must be declared outside the NUMTRIES loop

    // looking for the maximum performance:
    for (int times = 0; times < NUMTRIES; times++) {
        double time0 = omp_get_wtime();

        numHits = 0;

#pragma omp parallel for default(none) shared(txs, tys, txvs, svs, sths, stderr) reduction(+:numHits)
        for (int n = 0; n < NUMTRIALS; n++) {
            // randomize everything:
            float tx = txs[n];
            float ty = tys[n];
            float txv = txvs[n];
            float sv = svs[n];
            float sthd = sths[n];
            float sthr = Radians(sthd);
            float svx = sv * cos(sthr);
            float svy = sv * sin(sthr);

            // how long until the snowball reaches the y depth:
            float t = ty/svy;

            // how far the truck has moved in x in that amount of time:
            float truckx = tx + txv * t;

            // how far the snowball has moved in x in that amount of time:
            float sbx = svx * t;

            // does the snowball hit the truck (just check x distances, not height):
            if (fabs(truckx - sbx) < 20 )
            {
                numHits++;
                if (DEBUG) fprintf(stderr, "Hits the truck at time = %8.3f\n", t);
            }
        } // for( # of  monte carlo trials )

        double time1 = omp_get_wtime();
        double megaTrialsPerSecond = (double) NUMTRIALS / (time1 - time0) / 1000000.;
        if (megaTrialsPerSecond > maxPerformance)
            maxPerformance = megaTrialsPerSecond;

    } // for ( # of timing tries )

    float probability = (float) numHits / (float) (NUMTRIALS);        // just get for last NUMTRIES run
    // fprintf(stderr, "%2d threads : %8d trials ; probability = %6.2f%% ; megatrials/sec = %6.2lf\n",
    //         NUMT, NUMTRIALS, 100. * probability, maxPerformance);

    fprintf(stderr, "%2d, %8d, %6.2f%%, %6.2lf\n",
            NUMT, NUMTRIALS, 100. * probability, maxPerformance);

}