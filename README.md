<div align="center">
  <img src="https://raw.githubusercontent.com/huchukato/ComfyUI-PerfectVideoResolution/master/banner.png" alt="Perfect Video Resolution" width="800">

# Perfect Video Resolution

[![ComfyUI](https://img.shields.io/badge/ComfyUI-Custom%20Node-6c5ce7?style=flat-square)](https://github.com/comfyanonymous/ComfyUI)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/huchukato/ComfyUI-PerfectVideoResolution?style=flat-square)](https://github.com/huchukato/ComfyUI-PerfectVideoResolution/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/huchukato/ComfyUI-PerfectVideoResolution?style=flat-square)](https://github.com/huchukato/ComfyUI-PerfectVideoResolution/commits/master)
[![Models](https://img.shields.io/badge/Models-Wan%202.2%20%7C%20MiniMax%20H3%20%7C%20LTX-f97316?style=flat-square)](#features)

A unified ComfyUI custom node that combines model-specific video resolution presets with smart image and mask resizing.
</div>

It merges the functionality of **FindPerfectResolution** and **WanResolutions** into a single node, making it easy to pick the right resolution for **Wan 2.2**, **MiniMax H3**, and **LTX** video generation while also resizing the input image(s) and mask to match.

## Features

- **Model selection**: Wan 2.2, MiniMax H3, LTX
- **Aspect-ratio driven resolution presets** for each model
- **Resolution quality tiers**: Fast Draft, Preview, High Detail, Native (and model-specific labels)
- **Optional image inputs** for I2V/FL2V/SVI workflows:
  - `image` — main input image
  - `image2` — secondary image, resized to the same resolution
  - `mask` — optional mask, resized with the same geometry
- **Smart resize options**: upscale, upscale method, small-image crop/pad, pad color
- **Divisibility control**: default `16` for Wan 2.2, `32` for MiniMax H3 / LTX
- Outputs `width`, `height`, resized `IMAGE`, `IMAGE2`, `MASK`, and a `resolution_info` string

## Installation

Clone this repository into your ComfyUI `custom_nodes` folder:

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/huchukato/ComfyUI-PerfectVideoResolution.git
```

Restart ComfyUI.

## Usage

1. Add the node **Perfect Video Resolution** from the `utils` category.
2. Select the `model`, `aspect_ratio`, and `resolution`.
3. Optionally connect `image`, `image2`, and/or `mask`.
4. Connect `width` and `height` to your video sampler / latent generator.
5. Use the resized `IMAGE`, `IMAGE2`, and `MASK` outputs as needed.

When an image is connected, the node automatically picks the closest supported aspect ratio and resizes everything to the selected resolution.

## Inputs

| Name | Type | Description |
|------|------|-------------|
| `model` | COMBO | Video model: `WAN 2.2`, `MiniMax H3`, `LTX` |
| `aspect_ratio` | COMBO | Aspect ratio presets, depends on selected model |
| `resolution` | COMBO | Resolution quality tier, depends on model + aspect ratio |
| `image` | IMAGE | Optional input image (I2V/FL2V/SVI) |
| `image2` | IMAGE | Optional secondary image, resized to same resolution |
| `mask` | MASK | Optional mask, resized with same geometry |
| `divisible_by` | INT | Pixel alignment (default `16` for WAN, `32` for MMH3/LTX) |
| `upscale` | BOOLEAN | Allow upscaling when target is larger than source |
| `upscale_method` | COMBO | `lanczos`, `bilinear`, `bicubic`, `nearest` |
| `small_image_mode` | COMBO | `none`, `crop`, `pad` |
| `pad_color` | STRING | Background color for pad mode (default `#000000`) |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| `width` | INT | Calculated width |
| `height` | INT | Calculated height |
| `IMAGE` | IMAGE | Resized image |
| `IMAGE2` | IMAGE | Resized secondary image (placeholder if not connected) |
| `MASK` | MASK | Resized mask (placeholder if not connected) |
| `resolution_info` | STRING | Human readable resolution summary |

## Credits

Built by combining ideas from:
- [comfyui-find-perfect-resolution](https://github.com/ashtar1984/comfyui-find-perfect-resolution)
- [ComfyUI-WanResolutions](https://github.com/boobkake22/ComfyUI-WanResolutions)
