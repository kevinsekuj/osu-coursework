/**
 * @file archive.c
 * @author Kevin Sekuj (sekujk@oregonstate.edu)
 * @brief Archiver and unpacker written in C
 * @version 0.1
 * @date 2022-04-13
 *
 * @copyright Copyright (c) 2022
 *
 */
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <errno.h>
#include <err.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

/**
 * Like mkdir, but creates parent paths as well
 *
 * @return 0, or -1 on error, with errno set
 * @see mkdir(2)
 */
int mkpath(const char *pathname, mode_t mode)
{
    char *tmp = malloc(strlen(pathname) + 1);
    strcpy(tmp, pathname);
    for (char *p = tmp; *p != '\0'; ++p)
    {
        if (*p == '/')
        {
            *p = '\0';
            struct stat st;
            if (stat(tmp, &st))
            {
                if (mkdir(tmp, mode))
                {
                    free(tmp);
                    return -1;
                }
            }
            else if (!S_ISDIR(st.st_mode))
            {
                free(tmp);
                return -1;
            }
            *p = '/';
        }
    }
    free(tmp);
    return 0;
}

/**
 * Allocates a string containing the CWD
 *
 * @return allocated string
 */
char *
getcwd_a(void)
{
    char *pwd = NULL;
    for (size_t sz = 128;; sz *= 2)
    {
        pwd = realloc(pwd, sz);
        if (getcwd(pwd, sz))
            break;
        if (errno != ERANGE)
            err(errno, "getcwd()");
    }
    return pwd;
}

/**
 * Packs a single file or directory recursively
 *
 * @param fn The filename to pack
 * @param outfp The file to write encoded output to
 */
void pack(char *const fn, FILE *outfp)
{
    struct stat st;
    stat(fn, &st);

    if (stat(fn, &st) == -1)
    {
        perror("Error");
        exit(-1);
    }

    if (strcmp(fn, ".") == 0 || strcmp(fn, "..") == 0)
    {
        return;
    }

    if (!S_ISREG(st.st_mode) && !S_ISDIR(st.st_mode))
    {
        fprintf(stderr, "Skipping non-regular file `%s'.\n", fn);
        return;
    }

    if (S_ISREG(st.st_mode))
    {

        FILE *fp = fopen(fn, "rb");
        char *fileContents = calloc(st.st_size + 1, sizeof(char));

        assert((size_t)st.st_size == fread(fileContents, sizeof(char), st.st_size, fp));

        fprintf(
            outfp,
            "%ld:%s%ld:%s",
            strlen(fn), fn, st.st_size, fileContents);

        free(fileContents);
        fclose(fp);

        return;
    }
    DIR *curDir = opendir(fn);
    struct dirent *aDir;
    struct stat dirStat;
    stat(fn, &dirStat);

    chdir(fn);
    fprintf(
        outfp,
        "%ld:%s/",
        strlen(fn) + 1, fn);

    while ((aDir = readdir(curDir)) != NULL)
    {

        pack(aDir->d_name, outfp);
    }
    chdir("..");
    fprintf(outfp, "0:");
    closedir(curDir);
}

/**
 * Unpacks an entire archive
 *
 * @param fp The archive to unpack
 */

int unpack(FILE *fp)
{
    if (ferror(fp))
    {
        fprintf(stderr, "Error reading file.");
        exit(-1);
    }

    /* Get file name */
    int fnSize;
    if (EOF == fscanf(fp, "%d:", &fnSize))
    {
        return 0;
    }

    if (fnSize == 0)
    {
        chdir("..");
        unpack(fp);
        return 0;
    }

    char *fn = calloc(fnSize + 1, sizeof(char));

    assert((size_t)fnSize == fread(fn, sizeof(char), fnSize, fp));

    if (fn[strlen(fn) - 1] == '/')
    {
        if (mkpath(fn, 0700))
            err(errno, "mkpath()");
        chdir(fn);
    }
    else
    {
        int fSize;
        fscanf(fp, "%d:", &fSize);
        FILE *outfile = fopen(fn, "w");
        for (int i = 0; i < fSize; i++)
        {
            char c = fgetc(fp);
            fputc(c, outfile);
        }

        fclose(outfile);
    }
    free(fn);
    unpack(fp);
    return 0;
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        fprintf(stderr, "Usage: %s FILE... OUTFILE\n"
                        "       %s INFILE\n",
                argv[0], argv[0]);
        exit(1);
    }
    char *fn = argv[argc - 1];
    if (argc > 2)
    { /* Packing files */
        FILE *fp = fopen(fn, "w");
        for (int i = 1; i < argc - 1; ++i)
        {
            pack(argv[i], fp);
        }
        fclose(fp);
    }
    else
    { /* Unpacking an archive file */
        FILE *fp = fopen(fn, "r");
        if (fp == NULL)
        {
            fprintf(stderr, "Error reading file\n");
            exit(1);
        }
        unpack(fp);
        fclose(fp);
    }
}
