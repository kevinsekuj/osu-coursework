/**
 * @file server.c
 * @author Kevin Sekuj (sekujk@oregonstate.edu)
 * @brief  A server which accepts a socket connection, of a at least 5 connections
 *         at once, and processes characters received from that socket depending on
 *         the type of the server - either an encoding type or a decoding type.
 *
 *         One server file, server.c, is compiled into two executables (encrypt server
 *         and decrypt server) using preprocessor macros and compilation flags. The server
 *         will reject connections from encryption/decryption clients if their
 *         handshake values do not match the one the server accepts.
 *
 *         The server accepts bytes from the client in groups of two, from plaintext and
 *         key files. These bytes are processed by helper functions in enc_dec.header and
 *         sent back to the client.
 *
 *        REFERENCE: This server program heavily adapts code from Beej's
 *        Guide to Network Programming, section 6. This guide was referenced
 *        in the OTP assignment prompt and I decided to use the networking
 *        boilerplate code from here instead of the sample program.
 *
 *        https://beej.us/guide/bgnet/html/#client-server-background
 *
 * @version 0.1
 * @date 2022-06-05
 *
 * @copyright Copyright (c) 2022
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>
#include "enc_dec.h"

#define BACKLOG 10

/**
 * @brief Reads a byte from the socket connected to the server, handling an error
 *        and returning it if successful
 *
 * @param connectionSocket connected client
 * @return char byte read
 */
char readByte(int connectionSocket)
{
  char charRead;

  int charsRead = recv(connectionSocket, &charRead, 1, 0);

  if (charsRead < 0)
  {
    perror("ERROR reading from socket");
  }

  return charRead;
}

/**
 * @brief Helper function to reap zombie processes when forked child
 *        process exits.
 */
void sigchld_handler()
{
  // Waitpid can overrite errno - so save it first to restore later
  int saved_errno = errno;

  while (waitpid(-1, NULL, WNOHANG) > 0)
    ;

  errno = saved_errno;
}

/**
 * @brief Boilerplate from beej's to setup the address struct for the
 *        server socket for IPv4 or IPv6
 *
 * @param sa struct describing a generic sock address
 * @return void* address of ipv4/ipv6 address attribute
 */
void *get_in_addr(struct sockaddr *sa)
{
  if (sa->sa_family == AF_INET)
  {
    return &(((struct sockaddr_in *)sa)->sin_addr);
  }

  return &(((struct sockaddr_in6 *)sa)->sin6_addr);
}

int main(int argc, char const *argv[])
{
  // Boilerplate from Beej's for listening initializing socket connection
  // and listening for new connection on it
  int sockfd, new_fd;
  struct addrinfo hints, *servinfo, *p;
  struct sockaddr_storage their_addr;
  socklen_t sin_size;
  struct sigaction sa;
  int yes = 1;
  char s[INET6_ADDRSTRLEN];
  int rv;

  // Check usage and arguments
  if (argc != 2)
  {
    fprintf(stderr, "usage: enc_server listening_port\n");
    exit(1);
  }

  // More boilerplate from Beej's for setting up desired address family values
  // such as specifying preferred socket type
  memset(&hints, 0, sizeof hints);
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags = AI_PASSIVE;

  if ((rv = getaddrinfo(NULL, argv[1], &hints, &servinfo)) != 0)
  {
    fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
    return 1;
  }

  // Boilerplate from Beej's networking guide - Attempt to connect to provided socket
  for (p = servinfo; p != NULL; p = p->ai_next)
  {
    if ((sockfd = socket(p->ai_family, p->ai_socktype,
                         p->ai_protocol)) == -1)
    {
      perror("server: socket");
      continue;
    }

    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes,
                   sizeof(int)) == -1)
    {
      perror("setsockopt");
      exit(1);
    }

    if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1)
    {
      close(sockfd);
      perror("server: bind");
      continue;
    }

    break;
  }

  // Free sv when finished, sv is a structure that contains contain information
  // about the address of a service provider
  freeaddrinfo(servinfo); // all done with this structure

  if (p == NULL)
  {
    fprintf(stderr, "server: failed to bind\n");
    exit(1);
  }

  if (listen(sockfd, BACKLOG) == -1)
  {
    perror("listen");
    exit(1);
  }

  sa.sa_handler = sigchld_handler; // reap all dead processes
  sigemptyset(&sa.sa_mask);
  sa.sa_flags = SA_RESTART;
  if (sigaction(SIGCHLD, &sa, NULL) == -1)
  {
    perror("sigaction");
    exit(1);
  }

  while (1)
  {
    // Main loop for accepting socket connections
    sin_size = sizeof their_addr;
    new_fd = accept(sockfd, (struct sockaddr *)&their_addr, &sin_size);

    if (new_fd == -1)
    {
      perror("accept");
      continue;
    }

    inet_ntop(their_addr.ss_family,
              get_in_addr((struct sockaddr *)&their_addr),
              s, sizeof s);

#ifdef DEBUG
    fprintf(stderr, "server: got connection from %s\n", s);
#endif

    /** Beej's networking guide boilerplate end */

    // Child process
    if (!fork())
    {
      // close socket listener, child doesn't need it
      close(sockfd);

      // We use preprocessor macros instead of copy pasting encode/decode
      // servers/clients. We define a system where the value "0" indicates
      // an encoding server, and the value "1" indicates the decoding server

      // When the server file is compiled, it will be compiled into an executable
      // with the ENCODE flag and without it in order to create these two files
#ifdef ENCODE
      char expected = 0;
      char *serverType = "Encode";
#else
      char expected = 1;
      char *serverType = "Decode";
#endif

      // Attempt to secure the hadnshake from the client. If the handshake fails,
      // or the client type does not match the server type, reject it.
      char handshake;
      if (recv(new_fd, &handshake, 1, 0) != 1)
      {
        perror("Handshake failed");
        exit(1);
      }

      if (handshake != expected)
      {
        fprintf(stderr, "Handshake between server and client didn't match, expected client type: %s\n", serverType);
        exit(1);
      }

      // Server processing loop to handle recv data from the properly connected
      // client
      while (1)
      {
        char charRead = readByte(new_fd);

        // Read an EOF "poison" pill - exit
        if (charRead == EOF)
        {
          break;
        }

        char keyRead = readByte(new_fd);

        // process character depending on the server type which will be handled
        // by compiling with the ENCODE flag (and compiling without it)
#ifdef ENCODE
        char processedChar = encode(keyRead, charRead);
#else
        char processedChar = decode(keyRead, charRead);
#endif

        // Attempt to send processed character to the client
        if (send(new_fd, &processedChar, 1, 0) == -1)
        {
          perror("send");
          exit(0);
        }
      }

      // Close the connection and exit from the child process
      close(new_fd);
      exit(0);
    }
    close(new_fd);
  }
  return 0;
}
