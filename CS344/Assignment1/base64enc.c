/**
 * @file    base64enc.c
 * @author  Kevin Sekuj (sekujk@oregonstate.edu)
 * @brief   Base64 Encoder - a simple C program that encodes a stream of data into
 *          base 64 format
 * @version 0.1
 * @date    2022-04-06
 *
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#ifndef UINT8_MAX
#error "No support for uint8_t"
#endif

static char const ALPHABET[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                               "abcdefghijklmnopqrstuvwxyz"
                               "0123456789+/=";
static int const PADDING = 64;
static int const NEW_LINE = 76;
static int const INPUT_SIZE = 3;
static int const OUTPUT_SIZE = 4;

int main(int argc, char const *argv[])
{
    FILE *fp;

    if (argc > 2)
    {
        fprintf(stderr, "Invalid number of arguments.\n");
        exit(1);
    }
    if (argc == 1 || (strcmp(argv[1], "-") == 0))
    {
        fp = freopen(NULL, "rb", stdin);
        if (fp == NULL)
        {
            fprintf(stderr, "Error reading stdin.\n");
            exit(1);
        }
    }
    else
    {
        fp = fopen(argv[1], "rb");
        if (fp == NULL)
        {
            fprintf(stderr, "Error: Could not open file '%s'.\n", argv[1]);
            exit(1);
        }
    }
    uint8_t in[INPUT_SIZE];
    uint8_t out[OUTPUT_SIZE];
    uint8_t bytesRead;
    int charsPrinted = 0;
    while (1)
    {
        bytesRead = fread(in, sizeof(uint8_t), INPUT_SIZE, fp);
        if (bytesRead == 0)
            break;

        out[0] = in[0] >> 2;
        out[1] = ((in[0] & 0x03) << 4) | (in[1] >> 4);
        out[2] = ((in[1] & 0x0F) << 2) | ((in[2] >> 6) & 0x03);
        out[3] = in[2] & 0x3F;

        if (bytesRead < 2)
            out[2] = PADDING;
        if (bytesRead < 3)
            out[3] = PADDING;

        for (uint8_t i = 0; i < sizeof(out) / sizeof(out[0]); ++i)
        {
            if (charsPrinted == NEW_LINE)
            {
                printf("\n");
                charsPrinted = 0;
            }
            printf("%c", ALPHABET[out[i]]);
            charsPrinted++;
        }

        for (uint8_t i = 0; i < sizeof(in) / sizeof(in[1]); ++i)
        {
            in[i] = 0;
        }
    }
    fclose(fp);
    printf("\n");
    return 0;
}
