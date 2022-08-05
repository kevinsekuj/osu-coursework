/**
 * @file keygen.c
 * @author Kevin Sekuj (sekujk@oregonstate.edu)
 * @brief  Keygen program which generates a key from a specified length.
 *         The characters in the file generated are of the 27 allowed chars
 *         (A-Z and space) and a newline.
 * @version 0.1
 * @date 2022-05-19
 *
 * @copyright Copyright (c) 2022
 *
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

// constants that define ascii character "boundaries"
int SPACE = 32;
int START = 65;
int END = 91;
int MAX_CHARS = 27;

int main(int argc, char const *argv[])
{
  if (argc != 2)
  {
    fprintf(stderr, "Invalid number of arguments.\n");
    exit(1);
  }

  int keygenLength = atoi(argv[1]);
  int i = 0;
  srand(time(NULL));

  // generate key chars up to specified length using modulus addition
  while (i < keygenLength)
  {
    int randomNumber = rand() % MAX_CHARS;
    int result = randomNumber + START;

    // write space character at ascii 91 (one past Z)
    // else resulting char to stdout
    if (result == END)
    {
      fputc(SPACE, stdout);
    }
    else
    {
      fputc(result, stdout);
    }
    i++;
  }

  // write newline at the end of keygen to complete our key
  printf("\n");
  return 0;
}
