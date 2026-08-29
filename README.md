# HyperFrames Demo Clips

**A code-driven b-roll asset factory for infrastructure demos.**

[![HyperFrames](https://img.shields.io/badge/HyperFrames-0.8.3-5A29E4?style=flat-square)](https://hyperframes.heygen.com)
[![GSAP](https://img.shields.io/badge/GSAP-3.14.2-88CE02?style=flat-square)](https://gsap.com)
[![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)]()

---

## Why This Exists

I wanted to create a demo video for my infrastructure platform, but I didn't want to wrestle with traditional video editors. 

I discovered HyperFrames a declarative video framework and decided to try the animations as code.

This repo contains **7 standalone motion clips** (totaling ~30 seconds) built with HTML, CSS, and GSAP, orchestrated via HyperFrames. They're designed to be rendered to MP4 and dropped into a larger video edit as visual filler scrolling ticketing systems, terminal typing, security gap indicators, and more.

**The result?** I can iterate on animations, tweak timings, and re-render in minutes instead of hours. It was a fun exploration.

---

## The Clips

| # | Scene | Duration | Visual |
|---|-------|----------|--------|
| 1 | **Ops Ticketing Inbox** | 12s | Scrolling ticket feed + priority tags |
| 2 | **Terminal + IP Allocation** | 10s | SSH session + live IP assignment panel |
| 3 | **Security Gaps** | 8s | Pain point visualizations (isolation, audit gaps) |
| 4 | **Product Reveal** | 8s | Brand/tagline reveal with motion |
| 5 | **Provisioning** | 3s | Quick "Provisioning" title card |
| 6 | **Secure Connectivity** | 3s | "Secure Connectivity" title card |
| 7 | **Access Control** | 3s | "Access Control" title card |

---

## Rendering

### Full render (all scenes)

```bash
npm run render
# or
python render.py
```

### Per-scene render

```bash
python render.py --scene 01-ticket-inbox
python render.py --scene 02-terminal-ip
python render.py --scene 03-security-gaps
python render.py --scene 04-product-reveal
python render.py --scene 05-section-provisioning
python render.py --scene 06-section-connectivity
python render.py --scene 07-section-access-control
```

Output goes to `renders/<scene-name>.mp4`.

## Tech Stack

- [HyperFrames](https://hyperframes.heygen.com) 0.8.3
- GSAP 3.14.2
- HTML / CSS
- Python render helper
