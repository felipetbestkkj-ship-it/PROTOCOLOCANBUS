#!/usr/bin/env python3
"""Offline digital twin for Hiworld/HdPsa HVAC. No device I/O or transmission."""
from __future__ import annotations
import argparse, json, re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Optional

STATIC, OBSERVED, SIMULATED, INFERRED = "STATIC", "OBSERVED", "SIMULATED", "INFERRED"
LINE_RE = re.compile(r"(?P<direction>RX|TX):\[(?P<hex>.*?)\]")


def checksum(body: bytes) -> int:
    if len(body) < 4 or body[:2] != b"\x5a\xa5": raise ValueError("bad Hiworld prefix")
    return (sum(body[2:]) - 1) & 0xFF


def build_frame(cmd: int, payload: bytes=b"") -> bytes:
    body = bytes([0x5A,0xA5,len(payload)&0xFF,cmd&0xFF]) + payload
    return body + bytes([checksum(body)])


def valid(frame: bytes) -> bool:
    return len(frame)>=5 and frame[:2]==b"\x5a\xa5" and len(frame)==frame[2]+5 and checksum(frame[:-1])==frame[-1]


def hvac_tx(sub: int, value: int) -> bytes: return build_frame(0x3B, bytes([sub&0xFF,value&0xFF]))


def temp(raw: int) -> float:
    raw &= 0xFF; b = raw if raw < 128 else raw-256
    if b in (-2,-1,0): v = 15.0 if b == -2 else float(raw)
    elif 32 <= b <= 39: v = float(((b-32)//2)+16)
    elif 40 <= b <= 52: v = ((b-40)*0.5)+20.0
    elif b >= 53: v = float(((b-52)//2)+26)
    else: v = 0.0
    return 0.0 if raw == 254 else v


def airflow_mask(raw: int) -> int:
    raw &= 0x0F; m=0
    if raw in (3,5,12,14): m |= 4
    if raw in (5,6,13,14): m |= 2
    if raw in (11,12,13,14): m |= 1
    return m


def airflow_raw(mask: int) -> int:
    return {0:0,1:11,2:6,3:13,4:3,5:12,6:5,7:14}[mask]


@dataclass(frozen=True)
class HvacState:
    power:bool; max_ac:bool; rear_hvac:bool; auto:bool; sync:bool; ac:bool
    recirc:bool; auto_recirc:bool; rear_defrost:bool; front_defrost:bool
    wind:int; airflow:int; fan:int; left_raw:int; right_raw:int
    r8:int; r9:int; r10:int; outside_raw:int
    @property
    def mode(self): return airflow_mask(self.airflow)
    @property
    def left(self): return temp(self.left_raw)
    @property
    def right(self): return temp(self.right_raw)


def decode31(frame: bytes) -> HvacState:
    if not valid(frame) or frame[3] != 0x31 or frame[2] != 12: raise ValueError("need valid 0x31/12")
    p=frame[4:-1]
    return HvacState(bool(p[0]&0x40),bool(p[0]&0x20),bool(p[0]&0x10),bool(p[0]&8),bool(p[0]&4),bool(p[0]&1),
        bool(p[1]&0x10),bool(p[1]&8),bool(p[2]&0x20),bool(p[2]&0x10),p[3]&3,p[4]&0x0F,p[5],p[6],p[7],p[8],p[9],p[10],p[11])


def encode31(s: HvacState) -> bytes:
    p0=(0x40 if s.power else 0)|(0x20 if s.max_ac else 0)|(0x10 if s.rear_hvac else 0)|(8 if s.auto else 0)|(4 if s.sync else 0)|(1 if s.ac else 0)
    p1=(0x10 if s.recirc else 0)|(8 if s.auto_recirc else 0); p2=(0x20 if s.rear_defrost else 0)|(0x10 if s.front_defrost else 0)
    return build_frame(0x31,bytes([p0,p1,p2,s.wind&3,s.airflow&15,s.fan&255,s.left_raw&255,s.right_raw&255,s.r8&255,s.r9&255,s.r10&255,s.outside_raw&255]))


@dataclass(frozen=True)
class Request: prop:int; area:int; value:int|float


class Builder:
    """Reimplements HdPsaProtocol.buildHvacPackets semantics."""
    def __init__(self,state:HvacState,temp_unit:int=0): self.s,self.temp_unit=state,temp_unit
    def build(self,r:Request)->list[bytes]:
        p,a,v=r.prop,r.area,r.value; low=[]
        if p==16404: low=[(15,int(v))]
        elif p==24577:
            sub=5 if a==1 else 6 if a==2 else -1
            if sub!=-1: low=[(sub,int(v))]
        elif p==16385:
            if a==8 and int(v)!=int(self.s.power): low=[(1,0 if int(v)==0 else 1)]
            elif a==128: low=[(17,0 if int(v)==0 else 1)]
        elif p==16386: low=[(2,int(v))]
        elif p==16387:
            n=2 if self.temp_unit==0 else 1
            if a==4: low=[(13,1 if float(v)>self.s.right else 2)]*n
            else: low=[(12,1 if float(v)>self.s.left else 2)]*n
        elif p==16388: low=[(13 if a==4 else 12,2 if int(v)==0 else 1)]
        elif p==16389:
            d=int(v)-self.s.fan; low=[(11,1 if d>0 else 2)]*abs(d)
        elif p==16390: low=[(11,2 if int(v)==0 else 1)]
        elif p==16391:
            target,current=int(v),self.s.mode
            for bit,sub in ((2,9),(1,8),(4,10)):
                if (current&bit)!=(target&bit): low.append((sub,1 if target&bit else 0))
        elif p==16392: low=[(14,int(v))]
        elif p==16393: low=[(16,int(v))]
        elif p==16394:
            q=int(v)
            if q!=int(self.s.recirc): low=[(7,0 if q==1 else 1)]
        elif p==16395: low=[(4,0 if int(v)==0 else 1)]
        elif p==16396: low=[(3,int(v))]
        return [hvac_tx(x,y) for x,y in low]


def diff(a:HvacState,b:HvacState):
    skip={"r8","r9","r10","outside_raw"}; out={}
    for k in HvacState.__dataclass_fields__:
        if k not in skip and getattr(a,k)!=getattr(b,k): out[k]=(getattr(a,k),getattr(b,k))
    return out


@dataclass(frozen=True)
class Inference:
    action:str; confidence:float; changed:tuple[str,...]; predicted_tx:Optional[str]; reason:str


def hx(sub,val): return hvac_tx(sub,val).hex(" ").upper()


def infer(a:HvacState,b:HvacState)->Inference:
    d=diff(a,b); k=set(d)
    if k=={"rear_defrost"}:
        on=b.rear_defrost; return Inference(f"REAR_DEFROST_{'ON' if on else 'OFF'}",.999,tuple(sorted(k)),hx(6,int(on)),"single-field transition")
    if k=={"recirc"}:
        on=b.recirc; return Inference(f"RECIRCULATION_{'ON' if on else 'OFF'}",.995,tuple(sorted(k)),hx(7,0 if on else 1),"single-field transition; wire value inverted")
    if "power" in k and k.issubset({"power","ac","fan"}):
        on=b.power; return Inference(f"HVAC_POWER_{'ON' if on else 'OFF'}",.98,tuple(sorted(k)),hx(1,int(on)),"power toggle with A/C/fan side effects")
    if "front_defrost" in k and k.issubset({"front_defrost","recirc","airflow","fan","left_raw"}):
        on=b.front_defrost; return Inference(f"FRONT_DEFROST_{'ON' if on else 'OFF'}",.90 if on else .86,tuple(sorted(k)),hx(5,int(on)),"front-defrost macro")
    return Inference("UNKNOWN",0,tuple(sorted(k)),None,"no high-confidence rule")


TRACE=[
"5a a5 0c 31 45 10 00 01 06 04 fe fe 00 00 00 82 1a","5a a5 0c 31 45 10 10 01 0b 07 ff fe 00 00 00 82 33",
"5a a5 0c 31 45 10 30 01 0b 07 ff fe 00 00 00 82 53","5a a5 0c 31 45 00 20 01 06 04 fe fe 00 00 00 82 2a",
"5a a5 0c 31 45 00 00 01 06 04 fe fe 00 00 00 82 0a","5a a5 0c 31 45 10 00 01 06 04 fe fe 00 00 00 82 1a",
"5a a5 0c 31 04 10 00 01 06 00 fe fe 00 00 00 82 d5","5a a5 0c 31 45 10 00 01 06 04 fe fe 00 00 00 82 1a"]
STATES=[decode31(bytes.fromhex(x)) for x in TRACE]


class StateMachine:
    def __init__(self): self.edges=[(infer(a,b),a,b) for a,b in zip(STATES,STATES[1:])]
    def apply(self,s:HvacState,action:str)->HvacState:
        m=[b for i,a,b in self.edges if i.action==action and a==s]
        if len(m)!=1: raise KeyError((action,s))
        return m[0]
    def replay(self):
        s=STATES[0]; out=[s]
        for i,a,b in self.edges: s=self.apply(s,i.action); out.append(s)
        return out


def action(frame:bytes)->str:
    if not valid(frame) or frame[3]!=0x3B or frame[2]!=2: raise ValueError("need valid 0x3B")
    s,v=frame[4],frame[5]
    m={(1,0):"HVAC_POWER_OFF",(1,1):"HVAC_POWER_ON",(2,0):"AC_OFF",(2,1):"AC_ON",(3,0):"MAX_AC_OFF",(3,1):"MAX_AC_ON",(4,0):"AUTO_OFF",(4,1):"AUTO_ON",(5,0):"FRONT_DEFROST_OFF",(5,1):"FRONT_DEFROST_ON",(6,0):"REAR_DEFROST_OFF",(6,1):"REAR_DEFROST_ON",(7,0):"RECIRCULATION_ON",(7,1):"RECIRCULATION_OFF",(11,1):"FAN_UP",(11,2):"FAN_DOWN",(12,1):"TEMP_LEFT_UP",(12,2):"TEMP_LEFT_DOWN",(13,1):"TEMP_RIGHT_UP",(13,2):"TEMP_RIGHT_DOWN",(15,0):"SYNC_OFF",(15,1):"SYNC_ON",(16,0):"AUTO_RECIRC_OFF",(16,1):"AUTO_RECIRC_ON"}
    if (s,v) in m:return m[s,v]
    if s in (8,9,10) and v in (0,1):
        bit={8:1,9:2,10:4}[s]; return f"AIRFLOW_BIT_{bit}_{'ON' if v else 'OFF'}"
    if s==14:return f"WIND_INTENSITY_{v}"
    if s==17:return f"REAR_HVAC_POWER_{'ON' if v else 'OFF'}"
    return f"UNKNOWN_{s:02X}_{v:02X}"


def minimal(s:HvacState,f:bytes):
    sub,v=f[4],f[5]
    if sub==1:return replace(s,power=bool(v))
    if sub==17:return replace(s,rear_hvac=bool(v))
    if sub==2:return replace(s,ac=bool(v))
    if sub==3:return replace(s,max_ac=bool(v))
    if sub==4:return replace(s,auto=bool(v))
    if sub==5:return replace(s,front_defrost=bool(v))
    if sub==6:return replace(s,rear_defrost=bool(v))
    if sub==7:return replace(s,recirc=(v==0))
    if sub in (8,9,10):
        bit={8:1,9:2,10:4}[sub]; m=(s.mode|bit) if v else (s.mode&~bit); return replace(s,airflow=airflow_raw(m))
    if sub==11:return replace(s,fan=min(255,s.fan+1) if v==1 else max(0,s.fan-1))
    if sub==14:return replace(s,wind=v&3)
    if sub==15:return replace(s,sync=bool(v))
    if sub==16:return replace(s,auto_recirc=bool(v))
    return s


@dataclass(frozen=True)
class SimResult: action:str; state:HvacState; response:bytes; confidence:float; basis:str


class FakeCanbox:
    def __init__(self,s:HvacState): self.s=s; self.sm=StateMachine()
    def receive(self,f:bytes)->SimResult:
        a=action(f); empirical=[b for i,x,b in self.sm.edges if i.action==a and x==self.s]
        if len(empirical)==1: self.s=empirical[0]; return SimResult(a,self.s,encode31(self.s),.99,"empirical transition; command→effect still counterfactual")
        self.s=minimal(self.s,f); return SimResult(a,self.s,encode31(self.s),.70,"static minimum effect")


def split_frames(data:bytes):
    out=[];i=0
    while i+4<len(data):
        if data[i:i+2]==b"\x5a\xa5" and i+data[i+2]+5<=len(data): n=data[i+2]+5;out.append(data[i:i+n]);i+=n
        else:i+=1
    return out


def parse_log(path:str):
    out=[]
    for line in Path(path).read_text(errors="replace").splitlines():
        m=LINE_RE.search(line)
        if not m:continue
        try:data=bytes(int(x,16) for x in m.group("hex").split())
        except ValueError:continue
        out.extend((m.group("direction"),f) for f in split_frames(data))
    return out


def log_report(path:str):
    fs=parse_log(path); st=[];last=None
    for d,f in fs:
        if d=="RX" and len(f)>=4 and f[3]==0x31 and valid(f) and f!=last: st.append(decode31(f));last=f
    return {"valid_frames":sum(valid(f) for _,f in fs),"tx_0x3B":sum(d=="TX" and len(f)>=4 and f[3]==0x3B for d,f in fs),"states_0x31":len(st),"matches_reference":st==STATES,"actions":[infer(a,b).action for a,b in zip(st,st[1:])]}


def report(path=None):
    sm=StateMachine(); out={"model":"Hiworld/HdPsa HVAC offline digital twin","keycode_mode_active":False,"replay_exact":sm.replay()==STATES,"actions":[{"action":i.action,"confidence":i.confidence,"tx_static":i.predicted_tx,"changed":list(i.changed)} for i,_,_ in sm.edges],"one_shot":{"action":"REAR_DEFROST_ON","tx":hx(6,1),"rx":"0x31 payload byte[2] bit5 0→1; no other field changed in observed transition"}}
    if path:out["candata"]=log_report(path)
    return out


def self_test():
    for sub,val,h in [(1,1,"5a a5 02 3b 01 01 3e"),(2,1,"5a a5 02 3b 02 01 3f"),(11,1,"5a a5 02 3b 0b 01 48"),(12,1,"5a a5 02 3b 0c 01 49"),(15,1,"5a a5 02 3b 0f 01 4c")]:assert hvac_tx(sub,val).hex(" ")==h
    for x,s in zip(TRACE,STATES):assert encode31(s)==bytes.fromhex(x)
    b=Builder(STATES[0]);assert b.build(Request(16385,8,1))==[];assert b.build(Request(16385,8,0))==[hvac_tx(1,0)];assert len(b.build(Request(16389,-2147483648,7)))==3;assert b.build(Request(16394,-2147483648,1))==[]
    assert StateMachine().replay()==STATES
    assert [i.action for i,_,_ in StateMachine().edges]==["FRONT_DEFROST_ON","REAR_DEFROST_ON","FRONT_DEFROST_OFF","REAR_DEFROST_OFF","RECIRCULATION_ON","HVAC_POWER_OFF","HVAC_POWER_ON"]
    f=FakeCanbox(STATES[1]).receive(hvac_tx(6,1));assert f.state==STATES[2] and f.response==encode31(STATES[2])


def main():
    a=argparse.ArgumentParser();a.add_argument("--self-test",action="store_true");a.add_argument("--candata");a.add_argument("--json",action="store_true");x=a.parse_args()
    if x.self_test:self_test();print("SELF-TEST PASS");return
    r=report(x.candata);print(json.dumps(r,indent=2,ensure_ascii=False) if x.json else "\n".join(f"{i+1}: {e['action']} conf={e['confidence']} TX={e['tx_static']}" for i,e in enumerate(r['actions'])))
if __name__=="__main__":main()
