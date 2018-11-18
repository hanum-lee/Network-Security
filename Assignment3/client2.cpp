/*
** client.c -- a stream socket client demo
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <netinet/tcp.h>
#include <netinet/ip.h>
#include <iostream>
#include <iomanip>
#include <arpa/inet.h>

#define PORT "30205" // the port client will be connecting to

#define MAXDATASIZE 100 // max number of bytes we can get at once
//https://stackoverflow.com/questions/42004374/crafting-tcp-ip-packets
//https://stackoverflow.com/questions/13620607/creating-ip-network-packets
//https://stackoverflow.com/questions/8845178/c-programming-tcp-checksum

using namespace std;

struct pseudo_header {
    u_int32_t source_address;
    u_int32_t dest_address;
    u_int8_t placeholder;
    u_int8_t protocol;
    u_int16_t tcp_length;
};

unsigned short CheckSum(unsigned short *buffer, int size){
    unsigned long cksum=0;
    while(size >1)
    {
        cksum+=*buffer++;
        size -=sizeof(unsigned short);
    }
    if(size)
        cksum += *(unsigned char*)buffer;

    cksum = (cksum >> 16) + (cksum & 0xffff);
    cksum += (cksum >>16);
    return (unsigned short)(~cksum);
}


// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
	if (sa->sa_family == AF_INET) {
		return &(((struct sockaddr_in*)sa)->sin_addr);
	}

	return &(((struct sockaddr_in6*)sa)->sin6_addr);
}



int main(int argc, char *argv[])
{
	int sockfd, numbytes;
	char buf[MAXDATASIZE];
	struct addrinfo hints, *servinfo, *p;
	int rv;
	char s[INET6_ADDRSTRLEN];

	if (argc != 2) {
	    fprintf(stderr,"usage: client hostname\n");
	    exit(1);
	}

	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;

	if ((rv = getaddrinfo(argv[1], PORT, &hints, &servinfo)) != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return 1;
	}

	// loop through all the results and connect to the first we can

	if ((sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)) == -1) {
		perror("client: socket");
		return 1;
	}

	char datagram[4096];
	memset(datagram,0,4096);

  char *data = datagram + sizeof(struct ip) + sizeof(struct tcphdr);
  strcpy(data, "");

  // some address resolution
  char source_ip[32];
  strcpy(source_ip, "127.0.0.1");
  struct sockaddr_in sai;
  sai.sin_family = AF_INET;
  sai.sin_port = htons(80);

  sai.sin_addr.s_addr = inet_addr("127.0.0.1");
  cout << "sai.sin_addr.s_addr=" << sai.sin_addr.s_addr << endl;

  //Fill in the IP Header
  struct ip *iph = (struct ip *) datagram;
  iph->ip_hl = 5;
  iph->ip_v = 4;
  iph->ip_tos = 0;
  iph->ip_len = htons(sizeof(struct ip) + sizeof(struct tcphdr) + strlen(data));
  iph->ip_id = htons(54321);
  iph->ip_off = 0;
  iph->ip_ttl = 255;
  iph->ip_p = IPPROTO_TCP;
  iph->ip_sum = 0;
  iph->ip_src.s_addr = inet_addr(source_ip);
  iph->ip_dst.s_addr = sai.sin_addr.s_addr;

  //Ip checksum
  unsigned short checksum = CheckSum((unsigned short *) datagram, iph->ip_len);
  iph->ip_sum = checksum;
  cout << "iph->ip_sum=" << checksum << endl;

  unsigned char *pIph = (unsigned char *) datagram;
  for (int i = 0; i < 20; i++) {
      cout << setfill('0') << setw(2) << hex << (int) pIph[i] << " ";
      if (i + 1 >= 4 && (i + 1) % 4 == 0) {
          cout << endl;
      }
  }

  //TCP Header
  struct tcphdr *tcph = (struct tcphdr *) (datagram + sizeof(struct ip));
  struct pseudo_header psh;
  tcph->th_sport = htons(80);
  tcph->th_dport = htons(80);
  tcph->th_seq = 0;
  tcph->th_ack = 0;
  tcph->th_off = 5;
  tcph->th_flags = TH_SYN;
  tcph->th_win  = htons(5840); /* maximum allowed window size */
  tcph->th_sum = 0;
  tcph->th_urp = 0;

  //Now the TCP checksum
  psh.source_address = inet_addr(source_ip);
  psh.dest_address = sai.sin_addr.s_addr;
  psh.placeholder = 0;
  psh.protocol = IPPROTO_TCP;
  psh.tcp_length = htons(sizeof(struct tcphdr) + strlen(data));

  int psize = sizeof(struct pseudo_header) +
              sizeof(struct tcphdr) +
              strlen(data);

  malloc(psize);
  char *pseudogram;
  pseudogram = (char*)malloc(psize);


  memcpy(pseudogram, (char*) &psh, sizeof(struct pseudo_header));
  cout<< "TEst" << endl;
  memcpy(pseudogram + sizeof(struct pseudo_header), tcph, sizeof(struct tcphdr) + strlen(data));

  checksum = CheckSum((unsigned short*) pseudogram, psize);

  tcph->th_sum = checksum;
  cout << "tcph->th_sum=" << checksum << endl;

  unsigned char *pTcph = (unsigned char *) tcph;
  for (int i = 0; i < 20; i++) {
      cout << setfill('0') << setw(2) << hex << (int) pTcph[i] << " ";
      if (i + 1 >= 4 && (i + 1) % 4 == 0) {
          cout << endl;
      }
  }

  //IP_HDRINCL to tell the kernel that headers are included in the packet
  int one = 1;
  const int *val = &one;
  if (setsockopt(sockfd, IPPROTO_IP, IP_HDRINCL, val, sizeof(one)) < 0) {
      perror("Error setting IP_HDRINCL");
      exit(0);
  }

  struct sockaddr *pSa = (struct sockaddr *) &sai;

  // Send the packet
  if (sendto(sockfd, datagram, iph->ip_len, 0, pSa, sizeof(sai)) < 0) { // failed here
      perror("sendto failed");

  } else { //Data send successfully
      printf("Packet Send. Length : %d \n", iph->ip_len);
  }

/*	if (sendto(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
		perror("client: connect");
		close(sockfd);
		return 1;
	}*/

	if (p == NULL) {
		fprintf(stderr, "client: failed to connect\n");
		return 2;
	}

	inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr),
			s, sizeof s);
	printf("client: connecting to %s\n", s);

	freeaddrinfo(servinfo); // all done with this structure
/*
	if ((numbytes = recv(sockfd, buf, MAXDATASIZE-1, 0)) == -1) {
	    perror("recv");
	    exit(1);
	}

	buf[numbytes] = '\0';

	printf("client: received '%s'\n",buf);
*/
	close(sockfd);

	return 0;
}
