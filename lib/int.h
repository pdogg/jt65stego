/* Include file to configure the RS codec for integer symbols
 *
 * Copyright 2002, Phil Karn, KA9Q
 * May be used under the terms of the GNU General Public License (GPL)
 
 !This library is derived from the JT65/JT9 etc. library released under GPL as part of the WSJT-X source
!originally authored by Joe Taylor K1JT and available from: http://www.physics.princeton.edu/pulsar/K1JT/devel.html!
!Many files have been modified for use in the JT65Stego project in May/June of 2014 by
!Paul Drapeau and Brent Dukes and this version of the library should not be used for any purpose 
!other than the study of steganography in these protocols. It should not be considered a reliable replacement
!for the libraries distributed with WSJT-X.
!
!
!47 CFR §97 - Rules of the Amateur Radio Service
!
!Subpart A—General Provisions
!
!§97.113 Prohibited transmissions.
!
!(a) No amateur station shall transmit:
!
!(4) Music using a phone emission except as specifically provided elsewhere in this section; communications intended to facilitate a criminal act; messages encoded for the purpose of obscuring their meaning, except as otherwise provided herein; obscene or indecent words or language; or false or deceptive messages, signals or identification.
 */
#define DTYPE int

/* Reed-Solomon codec control block */
struct rs {
  int mm;              /* Bits per symbol */
  int nn;              /* Symbols per block (= (1<<mm)-1) */
  DTYPE *alpha_to;     /* log lookup table */
  DTYPE *index_of;     /* Antilog lookup table */
  DTYPE *genpoly;      /* Generator polynomial */
  int nroots;     /* Number of generator roots = number of parity symbols */
  int fcr;        /* First consecutive root, index form */
  int prim;       /* Primitive element, index form */
  int iprim;      /* prim-th root of 1, index form */
  int pad;        /* Padding bytes in shortened block */
};

static int modnn(struct rs *rs,int x){
  while (x >= rs->nn) {
    x -= rs->nn;
    x = (x >> rs->mm) + (x & rs->nn);
  }
  return x;
}
#define MODNN(x) modnn(rs,x)

#define MM (rs->mm)
#define NN (rs->nn)
#define ALPHA_TO (rs->alpha_to) 
#define INDEX_OF (rs->index_of)
#define GENPOLY (rs->genpoly)
#define NROOTS (rs->nroots)
//#define NROOTS (51)
#define FCR (rs->fcr)
#define PRIM (rs->prim)
#define IPRIM (rs->iprim)
#define PAD (rs->pad)
#define A0 (NN)

#define ENCODE_RS encode_rs_int
#define DECODE_RS decode_rs_int
#define INIT_RS init_rs_int
#define FREE_RS free_rs_int

void ENCODE_RS(void *p,DTYPE *data,DTYPE *parity);
int DECODE_RS(void *p,DTYPE *data,int *eras_pos,int no_eras);
void *INIT_RS(int symsize,int gfpoly,int fcr,
		   int prim,int nroots,int pad);
void FREE_RS(void *p);




