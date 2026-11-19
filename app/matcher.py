"""Rule-only demonstration. All products and prices are fictional."""
import re
from typing import Any

CATALOG=[]
_specs=[
("DEMO-CAM-001","NovaCam U3-GS-2","USB3","global",2.0,160,245,14,["Linux","Windows"],["arm64","x86_64"],False),
("DEMO-CAM-002","EdgeVision GE-GS-5","GigE","global",5.0,48,368,10,["Linux","Windows"],["x86_64"],False),
("DEMO-CAM-003","MiniSight U3-RS-2","USB3","rolling",2.0,90,152,7,["Windows"],[],False),
("DEMO-CAM-004","NovaCam U3-GS-1.3","USB3","global",1.3,210,205,11,["Linux","Windows"],["arm64","x86_64"],False),
("DEMO-CAM-005","OptiCore U3-GS-5","USB3","global",5.0,40,430,16,["Linux"],["x86_64"],False),
("DEMO-CAM-006","OptiCore U3-GS-2X","USB3","global",2.3,145,298,12,["Linux","Windows"],["arm64"],True),
("DEMO-CAM-007","EdgeVision GE-RS-8","GigE","rolling",8.0,30,390,20,["Windows"],[],False),
("DEMO-CAM-008","MiniSight U3-GS-1","USB3","global",1.0,240,180,13,["Windows"],[],False),
("DEMO-CAM-009","VisionPro GE-GS-12","GigE","global",12.0,20,775,18,["Linux"],["x86_64"],False),
("DEMO-CAM-010","NovaCam U3-RS-5","USB3","rolling",5.0,65,189,9,["Linux","Windows"],["arm64"],False),
("DEMO-CAM-011","EdgeCam U3-GS-4","USB3","global",4.0,75,310,9,["Linux"],["x86_64"],False),
("DEMO-CAM-012","RapidCam GE-GS-2","GigE","global",2.0,140,279,11,["Linux"],["arm64"],False),
("DEMO-CAM-013","BudgetCam U3-RS-3","USB3","rolling",3.0,50,120,7,["Windows"],[],False),
("DEMO-CAM-014","ProVision U3-GS-8","USB3","global",8.0,35,610,15,["Linux","Windows"],["arm64"],False),
("DEMO-CAM-015","EdgeCam GE-GS-1","GigE","global",1.0,220,240,10,["Linux"],["x86_64"],False),
("DEMO-CAM-016","NanoCam U3-RS-2","USB3","rolling",2.0,110,135,7,["Linux"],["arm64"],False),
]
for sku,name,interface,shutter,mp,fps,price,lead,systems,archs,uncertain in _specs:
    CATALOG.append(dict(sku=sku,name=name,vendor="虚构演示供应商",interface=interface,shutter=shutter,mp=mp,fps=fps,
        price_usd=price,lead_days=lead,os=systems,linux_arch=archs,sdk_arch_uncertain=uncertain,
        mount="C-Mount",sdk="Example SDK",tags=["工业视觉","样例数据"]))

def parse_requirements(text: str)->dict[str,Any]:
    t=text.lower()
    r=dict(text=text,interface="any",shutter="any",os="any",arch="any",min_mp=0,min_fps=0,max_price=None,qty=1)
    if re.search(r"usb\s*3|usb3|u3\b",t):r["interface"]="USB3"
    if re.search(r"gige|千兆网|千兆以太|网口",t):r["interface"]="GigE" if r["interface"]=="any" else "conflict"
    if "全局快门" in t or "global shutter" in t:r["shutter"]="global"
    if "卷帘" in t or "rolling shutter" in t:r["shutter"]="rolling" if r["shutter"]=="any" else "conflict"
    if "linux" in t:r["os"]="Linux"
    if "windows" in t or "win10" in t or "win11" in t:r["os"]="Windows" if r["os"]=="any" else "conflict"
    if "arm64" in t or "aarch64" in t:r["arch"]="arm64"
    elif "x86_64" in t or "x86-64" in t:r["arch"]="x86_64"
    m=re.search(r"(?:≥|>=|至少|不低于|不少于)\s*(\d+(?:\.\d+)?)\s*(?:mp|百万像素)",t) or re.search(r"(\d+(?:\.\d+)?)\s*(?:mp|百万像素)\s*(?:以上|及以上|起)",t)
    if m:r["min_mp"]=float(m.group(1))
    m=re.search(r"(?:≥|>=|至少|不低于|不少于)\s*(\d+)\s*(?:fps|帧)",t) or re.search(r"(\d+)\s*(?:fps|帧)\s*(?:以上|及以上|起)",t)
    if m:r["min_fps"]=int(m.group(1))
    m=re.search(r"(?:\$|usd\s*)(\d+(?:\.\d+)?)",t) or re.search(r"(?:预算|单价|价格)[^\d]{0,10}(\d+(?:\.\d+)?)\s*(?:美元|美金)",t)
    if m:r["max_price"]=float(m.group(1))
    m=re.search(r"(?:数量|采购|需要|qty|quantity)\s*(\d+)\s*(?:台|个|套|pcs|units)?",t)
    if m:r["qty"]=max(1,int(m.group(1)))
    return r

def match(raw:dict[str,Any])->dict[str,Any]:
    r=dict(interface=raw.get("interface") or "any",shutter=raw.get("shutter") or "any",os=raw.get("os") or "any",
        arch=raw.get("arch") or "any",min_mp=float(raw.get("min_mp") or 0),min_fps=int(raw.get("min_fps") or 0),
        max_price=raw.get("max_price"),qty=int(raw.get("qty") or 1),text=str(raw.get("text") or ""))
    if r["interface"] not in ("any","USB3","GigE","conflict") or r["shutter"] not in ("any","global","rolling","conflict") or r["os"] not in ("any","Linux","Windows","conflict") or r["arch"] not in ("any","arm64","x86_64"):
        raise ValueError("Unsupported filter")
    if r["qty"]<1 or r["min_mp"]<0 or r["min_fps"]<0:raise ValueError("Invalid numerical constraint")
    if r["max_price"] not in (None,""):r["max_price"]=float(r["max_price"])
    else:r["max_price"]=None
    results=[]
    for item in CATALOG:
        p=dict(item);fails=[];reviews=[]
        for key in ("interface","shutter"):
            if r[key]=="conflict":fails.append(key+" 约束冲突")
            elif r[key]!="any" and p[key]!=r[key]:fails.append(key+" 不符合要求")
        if r["os"]=="conflict":fails.append("OS 需求冲突")
        elif r["os"]!="any" and r["os"] not in p["os"]:fails.append("SDK 操作系统不兼容")
        if r["os"]=="Linux" and r["arch"]!="any":
            if r["arch"] not in p["linux_arch"]:fails.append("Linux SDK 架构不匹配")
            elif p["sdk_arch_uncertain"]:reviews.append("Linux SDK 架构证据待核实")
        if p["mp"]<r["min_mp"]:fails.append("像素不足")
        if p["fps"]<r["min_fps"]:fails.append("帧率不足")
        if r["max_price"] is not None and p["price_usd"]>r["max_price"]:fails.append("演示单价超预算")
        status="rejected" if fails else ("needs_review" if reviews else "candidate")
        score=round(100-min(p["price_usd"]*.06,45)-min(p["lead_days"]*.35,15),1) if status=="candidate" else None
        p.update(status=status,failures=fails,review_reasons=reviews,score=score,estimated_subtotal_usd=round(p["price_usd"]*r["qty"],2),
            outstanding=["核对厂家规格及 SDK 版本","核实实际库存、MOQ 和报价","复核物流、税费、售后"])
        results.append(p)
    groups={key:[p for p in results if p["status"]==key] for key in ("candidate","needs_review","rejected")}
    groups["candidate"].sort(key=lambda p:-(p["score"] or 0))
    return dict(requirements=r,eligible=groups["candidate"],review=groups["needs_review"],rejected=groups["rejected"],
        stats=dict(total=len(results),eligible=len(groups["candidate"]),review=len(groups["needs_review"]),rejected=len(groups["rejected"])),
        disclaimer="100% synthetic sample data. No live supplier quotes, vector database or LLM.")
