#ifndef ENC_DEC_H
#define ENC_DEC_H

/**
 * @file enc_dec.h
 * @author Kevin Sekuj (sekujk@oregonstate.edu)
 * @brief Header file which contains helper functions for encrypting and decrypting
 *        code.
 * @version 0.1
 * @date 2022-06-05
 *
 * @copyright Copyright (c) 2022
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * @brief Helper function for converting ascii characters to our 0-indexed system
 *
 * @param character one byte char
 * @return char processed char
 */
char bringToZero(char character)
{

  // 27th char (by element) converted to a space
  if (character == ' ')
  {
    character = '[';
  }
  character -= 'A'; // 0 - 26

  return character;
}

/**
 * @brief Helper function for converting ascii chars back from our 0-indexed system
 *
 * @param character 0-indexed char
 * @return char regular ascii char
 */
char bringFromZero(char character)
{
  character += 'A'; // 0 - 26

  // 27th char (by element) converted to a space
  if (character == '[')
  {
    character = ' ';
  }

  return character;
}

/**
 * @brief Function used to encrypt plaintext characters. We read chars
 *        from plaintext and key files and set them to our 0-indexed
 *        system where A is 0, B is 1, etc. We then use modulus addition
 *        with the keygen character to encrypt the byte, and revert it
 *        from our 0-indexed system.
 *
 * @param keyChar
 * @param messageChar
 * @return char processed encrypted character
 */
char encode(char keyChar, char messageChar)
{
  // convert to 0-indexed system
  messageChar = bringToZero(messageChar);
  keyChar = bringToZero(keyChar);

  char encodedChar = (messageChar + keyChar) % 27;
  char processedChar = bringFromZero(encodedChar);

  return processedChar;
}

/**
 * @brief Function used to decypt plaintext characters. We read chars
 *        from ciphertext and key files and set them to our 0-indexed
 *        system where A is 0, B is 1, etc. We then use modulus subtraction
 *        with the key character to decypt the byte, and revert it
 *        from our 0-indexed system.
 *
 * @param keyChar
 * @param messageChar
 * @return char processed decrypted character
 */
char decode(char keyChar, char messageChar)
{
  // convert to 0-indexed system
  messageChar = bringToZero(messageChar);
  keyChar = bringToZero(keyChar);

  // add 27 to ensure modulo is in correct range for subtraction
  char encodedChar = (messageChar - keyChar + 27) % 27;
  char processedChar = bringFromZero(encodedChar);

  return processedChar;
}

#endif
