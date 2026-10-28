# Prive Z12 : decodeur metadata chrony4.6.1/protocole6, sans autorite UTC.
# Aucun socket, secret, allocation dynamique, appel SDK ou effet systeme.
# Un succes prouve seulement le decodage ; provenance/NTS/temps restent requis.
# Constantes de format wire, distinctes de toute configuration production.
from libc.stddef cimport size_t
from libc.stdint cimport uint8_t, uint16_t, uint32_t

cdef extern from * nogil:
    r"""
    #include <stdint.h>
    #include <string.h>
    #include <stddef.h>
    #include <limits.h>
    #define Z12_CHR_V6 6
    #define Z12_CHR_REQTYPE 1
    #define Z12_CHR_REPTYPE 2
    #define Z12_CHR_OK 0
    #define Z12_CHR_TS_SENT 0x7fffffffu
    #define Z12_CHR_NSEC 1000000000u
    #define Z12_CHR_FMASK 0x1ffffffu
    #define Z12_CHR_FSIGN 0x1000000u
    #define Z12_CHR_FNEG 0x2000000u
    typedef struct { int32_t coef; int16_t exp; } Z12CF;
    typedef struct { uint8_t b[16]; uint16_t fam; } Z12CIP;
    typedef struct { uint64_t sec; uint32_t nsec; } Z12CTS;
    typedef struct {
      int bad, mal, foreign, unsup, range;
      uint16_t status; int has_status;
    } Z12CDiag;
    typedef struct {
      uint32_t ref; Z12CIP ip; uint16_t strat, leap;
      Z12CTS ts; Z12CF f[9];
    } Z12CTrack;
    typedef struct {
      Z12CIP ip; int16_t poll; uint16_t strat, state, mode, flags, reach;
      uint32_t since; Z12CF f[3];
    } Z12CSrc;
    typedef struct {
      uint16_t mode, ktype; uint32_t kid;
      uint16_t klen, keatt; uint32_t keago;
      uint16_t cookies, cooklen, nak, pad;
    } Z12CAuth;
    typedef struct {
      uint32_t ref; Z12CIP ip;
      uint8_t state, auth, leap, pad;
      uint16_t conf, eff; uint32_t ago; Z12CF f[3];
    } Z12CSel;
    typedef struct {
      Z12CIP rip, lip; uint16_t port;
      uint8_t leap, ver, mode, strat; int8_t poll, prec;
      Z12CF rd, rp; uint32_t ref; Z12CTS ts;
      Z12CF off, pdel, pdisp, resp, jit;
      uint16_t flags; uint8_t txc, rxc;
      uint32_t cnt[8]; uint32_t rsv[4];
    } Z12CNtp;
    typedef struct { uint8_t s[256]; uint32_t n; } Z12CName;
    typedef struct {
      uint16_t cmd, reply, status; uint32_t seq;
      union {
        uint32_t nsrc; Z12CTrack trk; Z12CSrc src;
        Z12CAuth auth; Z12CSel sel; Z12CNtp ntp; Z12CName name;
      } u;
    } Z12CRep;
    static uint16_t z12_chr_u16(const uint8_t*p){return (uint16_t)((uint16_t)p[0]<<8|p[1]);}
    static uint32_t z12_chr_u32(const uint8_t*p){return (uint32_t)p[0]<<24|(uint32_t)p[1]<<16|(uint32_t)p[2]<<8|p[3];}
    static void z12_chr_float_decode(uint32_t x,int32_t*c,int16_t*e){
      uint32_t eb=x>>25, cb=x&Z12_CHR_FMASK; int32_t es=(int32_t)eb; if(es>=64)es-=128;
      *e=(int16_t)(es-25);
      *c=(cb&Z12_CHR_FSIGN)?-(int32_t)(Z12_CHR_FNEG-cb):(int32_t)cb;
    }
    static int z12_chr_timespec_decode(const uint8_t*p,uint64_t*sec,uint32_t*ns,Z12CDiag*d){
      uint32_t hi=z12_chr_u32(p),lo=z12_chr_u32(p+4),n=z12_chr_u32(p+8);
      if(n>=Z12_CHR_NSEC){d->range=1;return 0;}
      if(hi==Z12_CHR_TS_SENT)hi=0;
      *sec=((uint64_t)hi<<32)|lo; *ns=n;
      if(*sec>(UINT64_MAX-n)/Z12_CHR_NSEC){d->range=1;return 0;}
      return 1;
    }
    static int z12_chr_ip_decode(const uint8_t*p,Z12CIP*o,Z12CDiag*d){
      uint16_t f=z12_chr_u16(p+16);
      if(p[18]!=0||p[19]!=0){d->mal=1;return 0;}
      if(f>3){d->unsup=1;return 0;}
      memset(o->b,0,sizeof(o->b));
      if(f==2)memcpy(o->b,p,16);else if(f==1||f==3)memcpy(o->b,p,4);
      o->fam=f; return 1;
    }
    static int z12_chr_float_at(const uint8_t*p,Z12CF*o){int32_t c;int16_t e;z12_chr_float_decode(z12_chr_u32(p),&c,&e);o->coef=c;o->exp=e;return 1;}
    static size_t z12_chr_wire_length(uint16_t cmd,uint16_t rep){
      if(cmd==14&&rep==2)return 32; if(cmd==15&&rep==3)return 76;
      if(cmd==33&&rep==5)return 104; if(cmd==57&&rep==26)return 172;
      if(cmd==65&&rep==19)return 284; if(cmd==67&&rep==20)return 52;
      if(cmd==69&&rep==23)return 76; return 0;
    }
    static int z12_chrony_decode(const uint8_t*D,size_t L,uint16_t EC,uint16_t ER,uint32_t ES,
      size_t MN,Z12CRep*O,Z12CDiag*G){
      size_t W; uint16_t v,t,cmd,rep,st;
      if(!D||!O||!G||MN==0||MN>256){if(G){G->bad=1;}return -2;}
      memset(G,0,sizeof*G); memset(O,0,sizeof*O);
      W=z12_chr_wire_length(EC,ER); if(!W){G->unsup=1;return 0;}
      if(L<28||L>284){G->mal=1;return 0;}
      v=D[0];t=D[1];
      if(v!=Z12_CHR_V6||t!=Z12_CHR_REPTYPE){G->unsup=1;return 0;}
      if(D[2]!=0||D[3]!=0){G->foreign=1;return 0;}
      cmd=z12_chr_u16(D+4);rep=z12_chr_u16(D+6);st=z12_chr_u16(D+8);
      G->status=st;G->has_status=1;
      if(cmd!=EC){G->foreign=1;return 0;}
      if(z12_chr_u16(D+10)!=0||z12_chr_u16(D+12)!=0||z12_chr_u16(D+14)!=0){G->foreign=1;return 0;}
      if(z12_chr_u32(D+16)!=ES){G->foreign=1;return 0;}
      if(z12_chr_u32(D+20)!=0||z12_chr_u32(D+24)!=0){G->foreign=1;return 0;}
      if(st!=Z12_CHR_OK)return 0;
      if(rep!=ER){G->foreign=1;return 0;}
      if(L!=W){G->mal=1;return 0;}
      O->cmd=cmd;O->reply=rep;O->status=st;O->seq=ES;
      if(cmd==14){uint32_t n=z12_chr_u32(D+28);O->u.nsrc=n;return 1;}
      if(cmd==33){
        const uint8_t*p=D+28;int i;
        O->u.trk.ref=z12_chr_u32(p);
        if(!z12_chr_ip_decode(p+4,&O->u.trk.ip,G))return 0;
        O->u.trk.strat=z12_chr_u16(p+24);O->u.trk.leap=z12_chr_u16(p+26);
        if(!z12_chr_timespec_decode(p+28,&O->u.trk.ts.sec,&O->u.trk.ts.nsec,G))return 0;
        for(i=0;i<9;i++)z12_chr_float_at(p+40+i*4,&O->u.trk.f[i]);
        return 1;
      }
      if(cmd==15){
        const uint8_t*p=D+28;
        if(!z12_chr_ip_decode(p,&O->u.src.ip,G))return 0;
        { uint32_t v=z12_chr_u16(p+20); O->u.src.poll=(int16_t)(v>=32768?(int32_t)v-65536:(int32_t)v); }
        O->u.src.strat=z12_chr_u16(p+22);O->u.src.state=z12_chr_u16(p+24);
        O->u.src.mode=z12_chr_u16(p+26);O->u.src.flags=z12_chr_u16(p+28);
        O->u.src.reach=z12_chr_u16(p+30);O->u.src.since=z12_chr_u32(p+32);
        z12_chr_float_at(p+36,&O->u.src.f[0]);z12_chr_float_at(p+40,&O->u.src.f[1]);z12_chr_float_at(p+44,&O->u.src.f[2]);
        return 1;
      }
      if(cmd==67){
        const uint8_t*p=D+28;
        O->u.auth.mode=z12_chr_u16(p);O->u.auth.ktype=z12_chr_u16(p+2);
        O->u.auth.kid=z12_chr_u32(p+4);O->u.auth.klen=z12_chr_u16(p+8);
        O->u.auth.keatt=z12_chr_u16(p+10);O->u.auth.keago=z12_chr_u32(p+12);
        O->u.auth.cookies=z12_chr_u16(p+16);O->u.auth.cooklen=z12_chr_u16(p+18);
        O->u.auth.nak=z12_chr_u16(p+20);O->u.auth.pad=z12_chr_u16(p+22);
        if(O->u.auth.pad!=0){G->mal=1;return 0;}
        if(O->u.auth.mode>2){G->unsup=1;return 0;}
        return 1;
      }
      if(cmd==65){
        const uint8_t*p=D+28;const uint8_t*z=NULL;size_t n=0;size_t i;
        for(i=0;i<256;i++)if(p[i]==0){z=p+i;n=i;break;}
        if(!z){G->mal=1;return 0;}
        for(i=n;i<256;i++)if(p[i]!=0){G->mal=1;return 0;}
        if(n==0||n>MN){G->foreign=1;return 0;}
        memcpy(O->u.name.s,p,256);O->u.name.n=(uint32_t)n;return 1;
      }
      if(cmd==69){
        const uint8_t*p=D+28;
        O->u.sel.ref=z12_chr_u32(p);
        if(!z12_chr_ip_decode(p+4,&O->u.sel.ip,G))return 0;
        O->u.sel.state=p[24];O->u.sel.auth=p[25];
        O->u.sel.leap=p[26];O->u.sel.pad=p[27];
        if(O->u.sel.pad!=0){G->mal=1;return 0;}
        O->u.sel.conf=z12_chr_u16(p+28);O->u.sel.eff=z12_chr_u16(p+30);
        O->u.sel.ago=z12_chr_u32(p+32);
        z12_chr_float_at(p+36,&O->u.sel.f[0]);z12_chr_float_at(p+40,&O->u.sel.f[1]);z12_chr_float_at(p+44,&O->u.sel.f[2]);
        return 1;
      }
      if(cmd==57){
        const uint8_t*p=D+28;int i;
        if(!z12_chr_ip_decode(p,&O->u.ntp.rip,G))return 0;
        if(!z12_chr_ip_decode(p+20,&O->u.ntp.lip,G))return 0;
        O->u.ntp.port=z12_chr_u16(p+40);
        O->u.ntp.leap=p[42];O->u.ntp.ver=p[43];
        O->u.ntp.mode=p[44];O->u.ntp.strat=p[45];
        O->u.ntp.poll=(int8_t)(p[46]>=128?(int)p[46]-256:(int)p[46]);
        O->u.ntp.prec=(int8_t)(p[47]>=128?(int)p[47]-256:(int)p[47]);
        z12_chr_float_at(p+48,&O->u.ntp.rd);z12_chr_float_at(p+52,&O->u.ntp.rp);
        O->u.ntp.ref=z12_chr_u32(p+56);
        if(!z12_chr_timespec_decode(p+60,&O->u.ntp.ts.sec,&O->u.ntp.ts.nsec,G))return 0;
        z12_chr_float_at(p+72,&O->u.ntp.off);z12_chr_float_at(p+76,&O->u.ntp.pdel);
        z12_chr_float_at(p+80,&O->u.ntp.pdisp);z12_chr_float_at(p+84,&O->u.ntp.resp);
        z12_chr_float_at(p+88,&O->u.ntp.jit);
        O->u.ntp.flags=z12_chr_u16(p+92);O->u.ntp.txc=p[94];O->u.ntp.rxc=p[95];
        for(i=0;i<8;i++)O->u.ntp.cnt[i]=z12_chr_u32(p+96+i*4);
        for(i=0;i<4;i++){O->u.ntp.rsv[i]=z12_chr_u32(p+128+i*4);if(O->u.ntp.rsv[i]!=0xffffffffu){G->mal=1;return 0;}}
        return 1;
      }
      G->unsup=1;return 0;
    }
    /* Decode seulement : aucune authentification, selection ou admissibilite UTC. */
    static int z12_chrony_parse(const uint8_t *data, size_t length,
        uint16_t command, uint16_t reply, uint32_t sequence, size_t max_name,
        Z12CRep *out, Z12CDiag *diag) {
      Z12CRep temporary = {0};
      int result;
      if(diag==NULL)return -2;
      memset(diag,0,sizeof(*diag));
      if(out!=NULL)memset(out,0,sizeof(*out));
      if(data==NULL||out==NULL||max_name==0||max_name>256){diag->bad=1;return -2;}
      result=z12_chrony_decode(data,length,command,reply,sequence,max_name,&temporary,diag);
      if(result==1)*out=temporary;
      return result;
    }
    
    """
    ctypedef struct Z12CRep:
        pass
    ctypedef struct Z12CDiag:
        int bad
        int mal
        int foreign
        int unsup
        int range
        uint16_t status
        int has_status
    int z12_chrony_parse(const uint8_t *data, size_t length,
        uint16_t command, uint16_t reply, uint32_t sequence, size_t max_name,
        Z12CRep *out, Z12CDiag *diag)
