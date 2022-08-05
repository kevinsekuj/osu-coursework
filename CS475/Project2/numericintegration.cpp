#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

// setting the number of threads:
#ifndef NUMT
#define NUMT 2
#endif

// setting the number of trials in the monte carlo simulation:
#ifndef NUMNODES
#define NUMNODES 10
#endif

// how many tries to discover the maximum performance:
#ifndef NUMTRIES
#define NUMTRIES 20
#endif

/* CONSTANTS */
#define _USE_MATH_DEFINES
#define XMIN -1.
#define XMAX 1.
#define YMIN -1.
#define YMAX 1.
const float N = 2.5f;
const float R = 1.2f;

/* PROTOTYPES */
float Height(int, int);

/* GLOBALS */
double volume;
double maxPerformance;

int main(int argc, char *argv[])
{
	omp_set_num_threads(NUMT);
	float fullTileArea = (((XMAX - XMIN) / (float)(NUMNODES - 1)) * ((YMAX - YMIN) / (float)(NUMNODES - 1)));

	for (int i = 0; i < NUMTRIES; i++)
	{

		double timeStart = omp_get_wtime();
		volume = 0;
#pragma omp parallel for default(none) shared(fullTileArea) reduction(+ \
																																			: volume)
		for (int i = 0; i < NUMNODES * NUMNODES; i++)
		{

			// points on a grid
			int iu = i % NUMNODES;
			int iv = i / NUMNODES;

			// area depends on where we are on the grid
			float z = Height(iu, iv);
			double curVolume = (fullTileArea * 2 * z);

			// on a corner
			if ((iu == 0 || iu == NUMNODES - 1) && (iv == 0 || iv == NUMNODES - 1))
			{
				curVolume *= .25;
			}

			// on an edge
			else if ((iu == 0 || iu == NUMNODES - 1) || (iv == 0 || iv == NUMNODES - 1))
			{
				curVolume *= .5;
			}

			volume += curVolume;
		}

		double timeEnd = omp_get_wtime();
		double megaTrialsPerSecond = (double)NUMNODES * NUMNODES / (timeEnd - timeStart) / 1000000.;

		if (megaTrialsPerSecond > maxPerformance)
		{
			maxPerformance = megaTrialsPerSecond;
		}
	}

	fprintf(stderr, "%d, %d, %f, %f\n",
					NUMT, NUMNODES, volume, maxPerformance);
}

float Height(int iu, int iv)
{
	float x = -1. + 2. * (float)iu / (float)(NUMNODES - 1);
	float y = -1. + 2. * (float)iv / (float)(NUMNODES - 1);

	float xn = pow(fabs(x), (double)N);
	float yn = pow(fabs(y), (double)N);
	float rn = pow(fabs(R), (double)N);
	float r = rn - xn - yn;
	if (r <= 0.)
	{
		return 0.;
	}

	float height = pow(r, 1. / (double)N);
	return height;
}
