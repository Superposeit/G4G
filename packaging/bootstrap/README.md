# TutorRD - Easy Install (Windows)

TutorRD is your **offline AI tutor**. Once it is set up, it works with **no
internet** - your questions stay on your own computer.

This folder sets everything up for you. You do **not** need to know any coding.

---

## 1. Install it (do this once)

1. Open the folder that contains this file.
2. **Right-click** `install.ps1` and choose **"Run with PowerShell"**.

If Windows blocks the script, open **PowerShell** (search for it in the Start
menu) and paste this single line, then press Enter:

```
powershell -ExecutionPolicy Bypass -File install.ps1
```

The setup assistant will:

- install the pieces TutorRD needs,
- look at your PC's memory (RAM) and pick the right AI model,
- download that model (this is the slow part - a coffee break),
- put a **TutorRD** shortcut on your Desktop.

When it says **"Setup complete"**, you are ready. You only run the installer
once. Running it again is safe - it skips anything already done.

---

## 2. What the "tier" means

The installer checks your RAM and tells you your tier. This just decides how
TutorRD runs best on your machine:

| Your RAM        | Tier       | What happens                                            |
| --------------- | ---------- | ------------------------------------------------------- |
| **8 GB or more**| **Full**   | Hosts the tutor fast. Downloads Gemma 4 E2B.            |
| **4 to 8 GB**   | **Lite**   | Hosts a small model (Gemma 4 E2B, ~1.4 GB).            |
| **Under 4 GB**  | **Client** | Does **not** download a model. Use **LAN mode** below.  |

Nothing to choose - the installer does the right thing automatically.

---

## 3. Start TutorRD

**Double-click the `TutorRD` shortcut on your Desktop.**

A small window opens and, after a moment, your web browser opens the tutor at:

```
http://localhost:3782
```

Keep that little window open while you study. To **stop** TutorRD, just close
that window (or press `Ctrl+C` inside it). Everything shuts down cleanly.

---

## 4. Use it from a phone or another PC (LAN mode)

If your PC is low on memory (the **Client** tier), or you just want to study
from a phone or tablet, you can connect to a TutorRD that is running on a
**stronger PC on the same Wi-Fi / network**.

On the phone or other device, open a web browser and go to:

```
http://<the-host-PC-IP>:3782
```

- Replace `<the-host-PC-IP>` with the host PC's network address, for example
  `http://192.168.1.50:3782`.
- The host PC shows its address in the TutorRD window when it starts. You can
  also find it on the host PC by opening PowerShell and running `ipconfig`
  (look for "IPv4 Address").
- The host PC and your device must be on the **same network**.

**If pages load but the tutor does not answer** from another device, the host
PC needs to advertise its network address. On the host PC, open TutorRD's
**Settings**, set the API / network address to the host's own IP (advanced),
and restart TutorRD. Ask your TutorRD helper if you are unsure.

---

## 5. If something goes wrong

The installer always explains problems in plain language and tells you the fix.
Here are the common ones:

- **"Node.js is NOT installed"**
  TutorRD needs Node.js to draw the tutor page. Install it, then run the
  installer again. Easiest: open PowerShell and run
  `winget install OpenJS.NodeJS.LTS`, or download the **LTS** installer from
  <https://nodejs.org>.

- **"uv is required but was not found"**
  `uv` sets up Python for you. Open PowerShell and run:
  `irm https://astral.sh/uv/install.ps1 | iex`
  then run the installer again.

- **"Tier: CLIENT (under 4 GB)"**
  Your PC is fine for studying, just not for hosting the AI. Use **LAN mode**
  (section 4) to connect to a stronger TutorRD PC.

- **The model download stopped partway**
  Just run the installer again. The download continues from where it stopped -
  you do not lose progress.

- **The Desktop shortcut is missing**
  Open the `packaging\bootstrap` folder, right-click `start-tutorrd.ps1`, and
  choose "Run with PowerShell".

Still stuck? Take a photo of the window and send it to your TutorRD helper.

---

### For helpers / advanced users

- Backend API runs on port **8001**, the web page on **3782**, and the local
  AI engine ("Engine Manager") on **8000**. All bind to `0.0.0.0`, so LAN
  access works once the network API address is set.
- Python is managed by **uv** (no system Python required). The installer runs
  `uv python install 3.12` then `uv sync --extra server`.
- The web page is a Next.js `output: "standalone"` bundle, so a **Node.js**
  runtime is required to serve it. The installer builds it with
  `scripts/prepare_web_package.py`.
- The model download uses `scripts/download_litertlm_model.py`
  (LiteRT Gemma 4 E2B, `litert-community/gemma-4-E2B-it-litert-lm`).
