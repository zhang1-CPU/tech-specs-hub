# E-Bike, 3D Printers & Smart Home Data Source Documentation

## Last Updated: May 14, 2026

---

## 1. E-Bike & Micromobility

### 1.1 Bosch eBike Systems

| Model | Data | Source Level | Source |
|-------|------|--------------|--------|
| Performance Line CX (BDU384Y) | 120 Nm, 750W, 600% support, 2.8kg | **A** | [Bosch eBike Official](https://www.bosch-ebike.com/en/products/performance-line-cx/) |
| Performance Line CX Race | 112 Nm, 600W, 400% | **A** | Bosch official documentation |
| Performance Line Speed | 85 Nm, 600W, 340% | **A** | Bosch official documentation |
| Active Line Plus | 50 Nm, 270W, 270% | **A** | Bosch official documentation |
| PowerTube 750 | 750 Wh, 36V, 4.4 kg | **A** | Bosch official documentation |
| PowerTube 625 | 625 Wh, 36V, 3.6 kg | **A** | Bosch official documentation |
| PowerPack 500/400 | 500/400 Wh, 36V | **A** | Bosch official documentation |

### 1.2 Bafang Motors

| Model | Data | Source Level | Source |
|-------|------|--------------|--------|
| M620 Ultra (BBS02) | 160 Nm, 1000W, 3.4 kg | **B** | [Bafang official specs](https://www.bafang.com) |
| M500 | 95 Nm, 500W, 2.9 kg | **B** | Bafang official specs |
| M400 | 80 Nm, 350W, 2.9 kg | **B** | Bafang official specs |

### 1.3 Segway-Ninebot

| Model | Data | Source Level | Source |
|-------|------|--------------|--------|
| Max G2 Ultra | 450W, 551Wh, 70 km range | **B** | Amazon listings, ZOL specs |
| Max G2 | 350W, 459Wh, 55 km range | **B** | Amazon listings |
| Max G30LP/P | 350W, 367-551Wh, 40-65 km | **B** | Amazon listings |

---

## 2. Smart Home - Roborock & Dreame

### 2.1 Roborock

| Model | Data | Source Level | Source |
|-------|------|--------------|--------|
| S8 MaxV Ultra | 10000 Pa, 6400 mAh, LiDAR+AI | **B** | Roborock official |
| S8 Pro Ultra | 6000 Pa, 5200 mAh | **B** | Roborock official |
| S7 MaxV Ultra | 5100 Pa, 5200 mAh | **B** | Roborock official |

### 2.2 Dreame

| Model | Data | Source Level | Source |
|-------|------|--------------|--------|
| L20 Ultra | 7000 Pa, 6400 mAh | **B** | Dreame official |
| L10s Pro Ultra Heat | 7000 Pa, 5200 mAh | **B** | Dreame official |
| D10s Pro | 5000 Pa, 5200 mAh | **B** | Dreame official |

---

## 3. 3D Printers

### 3.1 Bambu Lab

| Model | Data | Source Level | Source |
|-------|------|--------------|--------|
| X1 Carbon | 256×256×256mm, 0.4mm nozzle, 300°C, 500mm/s | **B** | Bambu Lab official |
| X1E | 256×256×256mm, 300°C, Ethernet | **B** | Bambu Lab official |
| P1P | 256×256×256mm, 300°C, 500mm/s | **B** | Bambu Lab official |
| P1S | 256×256×256mm, 300°C, enclosed | **B** | Bambu Lab official |
| A1 Mini | 256×180×180mm, 300°C, 500mm/s | **B** | Bambu Lab official |

### 3.2 Prusa Research

| Model | Data | Source Level | Source |
|-------|------|--------------|--------|
| MK4 | 250×210×220mm, 0.4mm, 300°C, 200mm/s | **A** | [Prusament.com](https://www.prusament.com) |
| XL | 360×360×360mm, multi-material | **A** | Prusament.com |
| MINI+ | 180×180×180mm, 280°C | **A** | Prusament.com |

### 3.3 Creality

| Model | Data | Source Level | Source |
|-------|------|--------------|--------|
| K1 | 220×220×250mm, CoreXY, 300°C | **B** | Creality official |
| K1C | 220×220×250mm, carbon fiber | **B** | Creality official |
| Ender 3 S1 Pro | 220×220×270mm, 260°C | **B** | Creality official |

---

## 4. Source Level Definitions

- **A级 (A)**: Official manufacturer documentation, verified datasheets
- **B级 (B)**: Authorized distributors, major retail platforms (Amazon, official stores)
- **C级 (C)**: Community-reported data, user forums, review sites

---

## 5. Notes

1. **Bosch eBike**: The Smart System with Bluetooth connectivity is standard across all 2024+ models
2. **Bambu Lab AMS**: Auto Material System with RFID chip reading for filament tracking
3. **Roborock S8 MaxV Ultra**: Features Reactive AI obstacle avoidance with structured light
4. **Dreame L20 Ultra**: Hot water mop washing (58°C) for better cleaning

---

## 6. Pending Updates

- **P2 (Next Quarter)**: Autel EVO II Pro, Skydio X10 specifications
- **P3 (Annual)**: Dyson V15 battery analysis, Garmin firmware downgrade guides