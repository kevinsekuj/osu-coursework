/**
 * @file line_processor.c
 * @author Kevin Sekuj (you@domain.com)
 * @brief Multi-threaded Producer-Consumer Pipeline
 *
 *        This program reads, processes, and outputs lines of input via the use
 *        of multi-threading and the Producer-Consumer Pipeline programming
 *        paradigm. Four threads, the Input, Line Separator, Expansion, and
 *        Output thread process input from standard input by reading in lines,
 *        replacing line separators with spaces, expanding "++" into "^", and
 *        printing processed data 80 characters at a time to stdout.
 *
 *        These 4 threads communicate with each other via the Producer-Consumer
 *        approach, where each pair of threads communicate via shared buffers.
 *        Mutex locks and condition variables coordinate the threads, and the
 *        program continuously processes input without sleeping.
 *
 *        REFERENCE: This program heavily adapts the sample program
 *        6_5_prod_cons_pipeline.c given in the CS344 Multi-threaded Producer
 *        Consumer Pipeline prompt.
 *
 * @version 0.1
 * @date 2022-05-24
 *
 * @copyright Copyright (c) 2022
 *
 */

/* IMPORTS */
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>
/* */

/* CONSTANTS */
#define LINES 50
#define SIZE 1000
#define MAX_LINE_LENGTH 80

char *STOP = "STOP";
char *STOP_LINE = "STOP\n";
const char EXPANSION_CHAR = '+';
const char NULL_TERMINATOR = '\0';
const char REPLACEMENT_CHAR = '^';
/* */

/* GLOBALS */

// Buffers are initialized as matrices of 50 rows of 1000 elements each

// [
//    Row 1  : Array[1000]
//    Row 2  : Array[1000]
//    ...
//    Row 50 : Array[1000]
//                          ]

// Shared Buffer resource between input and separator thread
char buffer_1[LINES][SIZE];
int count_1 = 0;                                     // length of the buffer
int prod_idx_1 = 0;                                  // index where the producer thread will put next item
int con_idx_1 = 0;                                   // index where consumer thread will get next item
pthread_mutex_t mutex_1 = PTHREAD_MUTEX_INITIALIZER; // initializing buffer 1 mutex
pthread_cond_t full_1 = PTHREAD_COND_INITIALIZER;    // initializing buffer 1 con-var

// Shared Buffer resource between separator and expansion thread
char buffer_2[LINES][SIZE];
int count_2 = 0;
int prod_idx_2 = 0;
int con_idx_2 = 0;
pthread_mutex_t mutex_2 = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t full_2 = PTHREAD_COND_INITIALIZER;

// Shared Buffer resource between expansion and output thread
char buffer_3[LINES][SIZE];
int count_3 = 0;
int prod_idx_3 = 0;
int con_idx_3 = 0;
pthread_mutex_t mutex_3 = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t full_3 = PTHREAD_COND_INITIALIZER;
/* GLOBALS */

/**
 * @brief Get the user input line from stdin
 *
 * @param line line read from stdin
 */
void get_user_input(char *line)
{
  fgets(line, SIZE, stdin);
}

/**
 * @brief Puts a line into buffer 1
 *
 * @param line line read from stdin
 */
void put_buff_1(char *line)
{
  // lock mutex before putting a line into the buffer
  pthread_mutex_lock(&mutex_1);
  strcpy(buffer_1[prod_idx_1], line);

  // increment index where next item is put and increment buffer count
  prod_idx_1++;
  count_1++;

  // signal to consumer that buffer has data and unlock mutex
  pthread_cond_signal(&full_1);
  pthread_mutex_unlock(&mutex_1);
}

/**
 * @brief Function that the input thread runs
 *        Gets input from stdin and puts it into buffer 1.
 *
 *        If the line read is a STOP line, we pass along
 *        STOP through the buffers to terminate all threads.
 *
 * @return void*
 */
void *get_input()
{
  while (true)
  {
    // Initialize a line to read in stdin input
    char line[SIZE];
    get_user_input(line);

    // Pass along a STOP message in the buffers if stop line is encountered
    if (strcmp(line, STOP_LINE) == 0)
    {
      put_buff_1(STOP);
      break;
    }

    put_buff_1(line);
  }

  return NULL;
}

/**
 * @brief Get the next line from buffer 1
 *
 * @param line line read from buffer 1
 */
void get_buff_1(char *line)
{
  // Lock mutex before checking the buffer
  pthread_mutex_lock(&mutex_1);

  // If buffer 1's count is empty, it has no data. Wait for producer to signal
  // to consumer that the buffer has data
  while (count_1 == 0)
  {
    pthread_cond_wait(&full_1, &mutex_1);
  }

  // Copy buffer line into line variable to be processed
  strcpy(line, buffer_1[con_idx_1]);

  // Increment index to get the next line, and decrement count of items in buff1
  con_idx_1++;
  count_1--;

  // unlock mutex
  pthread_mutex_unlock(&mutex_1);
}

/**
 * @brief Puts a line into buffer2
 *
 * @param line Line processed by separator thread
 */
void put_buff_2(char *line)
{

  // lock mutex before putting a line into the buffer
  pthread_mutex_lock(&mutex_2);

  // Copy the processed line into the row of our buffer matrix
  strcpy(buffer_2[prod_idx_2], line);

  // increment index where next item is put and increment buffer count
  prod_idx_2++;
  count_2++;

  // signal to consumer that buffer has data and unlock mutex
  pthread_cond_signal(&full_2);
  pthread_mutex_unlock(&mutex_2);
}

/**
 * @brief Function that the separator thread runs
 *
 *        Gets line from shared buffer 1 and processes it by changing
 *        new lines into spaces.
 *
 *        If the line read is a STOP line, we pass along
 *        STOP through the buffers to terminate all threads.
 *
 * @return void*
 */
void *separator()
{
  while (true)
  {
    // Initialize a line to read in line from buffer 1
    char line[SIZE];
    get_buff_1(line);

    // Pass along a STOP message in the buffers if stop line is encountered
    if (strcmp(line, STOP) == 0)
    {
      put_buff_2(STOP);
      break;
    }

    // if the last element of line read from stdin is a newline,
    // change it to a space and copy it into buffer 2
    int last_element = strlen(line) - 1;
    if (line[last_element] == '\n')
    {
      line[last_element] = ' ';
    }

    put_buff_2(line);
  }

  return NULL;
}

/**
 * @brief Get the next line from buffer 2
 *
 * @param line line processed by separator thread
 */
void get_buff_2(char *line)
{
  // Lock mutex before checking the buffer
  pthread_mutex_lock(&mutex_2);

  // If buffer 2's count is empty, it has no data. Wait for producer to signal
  // to consumer that the buffer has data
  while (count_2 == 0)
  {
    pthread_cond_wait(&full_2, &mutex_2);
  }

  // Copy buffer line into line variable to be processed
  strcpy(line, buffer_2[con_idx_2]);

  // Increment index to get the next line, and decrement count of items in buff2
  con_idx_2++;
  count_2--;

  // unlock mutex
  pthread_mutex_unlock(&mutex_2);
}

/**
 * @brief Puts a line into buffer3
 *
 *        REFERENCE:
 *        The variable expansion processing was adapted directly from my
 *        implementation of smallsh.c
 *
 * @param line Line processed by expansion thread
 */
void put_buff_3(char *line)
{

  // lock mutex before putting a line into the buffer
  pthread_mutex_lock(&mutex_3);

  // Copy the processed line into the row of our buffer matrix
  strcpy(buffer_3[prod_idx_3], line);

  // increment index where next item is put and increment buffer count
  prod_idx_3++;
  count_3++;

  // signal to consumer that buffer has data and unlock mutex
  pthread_cond_signal(&full_3);
  pthread_mutex_unlock(&mutex_3);
}

/**
 * @brief Function that the expansion thread runs
 *
 *        Checks lines read from input for expansion characters and replaces them
 *        with carets.
 *
 *        If the line read is a STOP line, we pass along
 *        STOP through the buffers to terminate all threads.
 *
 * @return void*
 */
void *expansion()
{
  while (true)
  {
    // Initialize a line to read in from buffer 2
    char line[SIZE] = {0};
    get_buff_2(line);

    // Pass along a STOP message in the buffers if stop line is encountered
    if (strcmp(line, STOP) == 0)
    {
      put_buff_3(STOP);
      break;
    }

    // Initialize a temporary array
    char temp[SIZE] = {0};

    // iterate through processed line input to replace expansion characters
    // with replacement characters - in this case, ++ by ^. we use a two pointer
    // technique to accomplish this, where pointer j inserts elements into
    // the temp buffer to be sent to the next thread based on the cases below
    int j = 0;
    for (int i = 0; line[i] != NULL_TERMINATOR; i++)
    {
      // Case 1 - found an expansion char
      if (line[i] == EXPANSION_CHAR)
      {
        // Case 1.a. - found another expansion char, replace
        if (line[i + 1] == EXPANSION_CHAR)
        {
          temp[j] = REPLACEMENT_CHAR;
          i++;
          j++;
        }
        // Case 1.b. - only one expansion char was found
        else
        {
          temp[j] = EXPANSION_CHAR;
          j++;
        }
      }
      // Case 2 - no expansion char
      else
      {
        temp[j] = line[i];
        j++;
      }
    }

    put_buff_3(temp);
  }
  return NULL;
}

/**
 * @brief Get the processed, line separated, expanded line from buffer 3.
 *
 * @param line
 */
void get_buff_3(char *line)
{
  // Lock mutex before checking the buffer
  pthread_mutex_lock(&mutex_3);

  // If buffer 3's count is empty, it has no data. Wait for producer to signal
  // to consumer that the buffer has data
  while (count_3 == 0)
  {
    pthread_cond_wait(&full_3, &mutex_3);
  }

  // Copy buffer line into line variable to be processed
  strcpy(line, buffer_3[con_idx_3]);

  // Increment index to get the next line, and decrement count of items in buff2
  con_idx_3++;
  count_3--;

  // unlock mutex
  pthread_mutex_unlock(&mutex_3);
}

/**
 * @brief Function that the write output thread runs
 *
 *        Initializes a local buffer to hold lines of 80 characters to write
 *        along with a null terminator and an index for the buffer to keep
 *        track of how many characters were written in a given iteration, as
 *        there is no guarantee a line will be exactly 80 characters.
 *
 * @return void*
 */
void *write_output()
{
  // temp buffer with a null terminator to hold how many characters were
  // were written in a given iteration, using a buffer index to keep track
  // of chars written
  char buffer_4[81];
  buffer_4[80] = 0;
  int buff_i = 0;

  while (true)
  {
    // read processed, line separated, expanded line from buffer 3
    char line[SIZE];
    get_buff_3(line);

    // break if we see a STOP line
    if (strcmp(line, STOP) == 0)
    {
      break;
    }

    // insert characters from the line read from buffer_3 into our local writing
    // buffer. If the buffer contains 80 characters, we write the line to stdout
    // and reset buff_index to load N characters over 80 into the buffer. The
    // buffer thus contains any leftover characters to print out for the next
    // iteration

    int lineLength = strlen(line);
    for (int i = 0; i < lineLength; i++)
    {
      buffer_4[buff_i] = line[i];
      buff_i++;

      if (buff_i == 80)
      {
        printf("%s\n", buffer_4);
        fflush(stdout);
        buff_i = 0;
      }
    }
  }

  return NULL;
}

int main()
{
  // Initialize threads
  pthread_t input_t, separator_t, expansion_t, output_t;

  pthread_create(&input_t, NULL, get_input, NULL);
  pthread_create(&separator_t, NULL, separator, NULL);
  pthread_create(&expansion_t, NULL, expansion, NULL);
  pthread_create(&output_t, NULL, write_output, NULL);

  // Wait until thread termination
  pthread_join(input_t, NULL);
  pthread_join(separator_t, NULL);
  pthread_join(expansion_t, NULL);
  pthread_join(output_t, NULL);

  return EXIT_SUCCESS;
}