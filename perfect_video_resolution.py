import math
import re
from fractions import Fraction
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
from PIL import Image


WAN_PRESETS: Dict[str, List[Tuple[int, int, str]]] = {
    "1:1": [
        (480, 480, "Fast Draft"),
        (640, 640, "Preview"),
        (832, 832, "High Detail"),
        (960, 960, "Wan 2.2 Native"),
    ],
    "2:3": [
        (384, 576, "Fast Draft"),
        (512, 768, "Preview"),
        (672, 1008, "High Detail"),
        (768, 1168, "Wan 2.2 Native"),
    ],
    "3:2": [
        (576, 384, "Fast Draft"),
        (768, 512, "Preview"),
        (1008, 672, "High Detail"),
        (1168, 768, "Wan 2.2 Native"),
    ],
    "3:4": [
        (432, 576, "Fast Draft"),
        (576, 768, "Preview"),
        (720, 960, "High Detail"),
        (816, 1104, "Wan 2.2 Native"),
    ],
    "4:3": [
        (576, 432, "Fast Draft"),
        (768, 576, "Preview"),
        (960, 720, "High Detail"),
        (1104, 816, "Wan 2.2 Native"),
    ],
    "9:16": [
        (352, 624, "Fast Draft"),
        (480, 848, "Preview"),
        (624, 1104, "High Detail"),
        (720, 1280, "Wan 2.2 Native"),
    ],
    "16:9": [
        (624, 352, "Fast Draft"),
        (848, 480, "Preview"),
        (1104, 624, "High Detail"),
        (1280, 720, "Wan 2.2 Native"),
    ],
}


MINIMAX_PRESETS: Dict[str, List[Tuple[int, int, str]]] = {
    "1:1": [
        (512, 512, "Fast Draft"),
        (640, 640, "Preview"),
        (768, 768, "High Detail"),
        (1024, 1024, "Native"),
        (1152, 1152, "1.5K"),
        (1440, 1440, "1080P Class"),
        (1536, 1536, "2K"),
    ],
    "3:4": [
        (448, 576, "Fast Draft"),
        (576, 736, "Preview"),
        (672, 896, "High Detail"),
        (864, 1184, "Native"),
        (992, 1344, "1.5K"),
        (1248, 1664, "1080P Class"),
        (1344, 1760, "2K"),
    ],
    "4:3": [
        (576, 448, "Fast Draft"),
        (736, 576, "Preview"),
        (896, 672, "High Detail"),
        (1184, 864, "Native"),
        (1344, 992, "1.5K"),
        (1664, 1248, "1080P Class"),
        (1760, 1344, "2K"),
    ],
    "9:16": [
        (384, 672, "Fast Draft"),
        (480, 864, "Preview"),
        (576, 1024, "High Detail"),
        (768, 1344, "Native"),
        (864, 1536, "1.5K"),
        (1088, 1920, "1080P Class"),
        (1152, 2048, "2K"),
    ],
    "16:9": [
        (672, 384, "Fast Draft"),
        (864, 480, "Preview"),
        (1024, 576, "High Detail"),
        (1344, 768, "Native"),
        (1536, 864, "1.5K"),
        (1920, 1088, "1080P Class"),
        (2048, 1152, "2K"),
    ],
    "21:9": [
        (768, 320, "Fast Draft"),
        (992, 416, "Preview"),
        (1184, 512, "High Detail"),
        (1536, 672, "Native"),
        (1760, 768, "1.5K"),
        (2208, 960, "1080P Class"),
        (2336, 992, "2K"),
    ],
}

MINIMAX_TARGET_PIXELS = (
    512 * 512,
    int(0.40 * 1024 * 1024),
    1024 * 576,
    int(0.90 * 1024 * 1024),
    1344 * 768,
    1536 * 864,
    int(2.00 * 1024 * 1024),
    2048 * 1152,
)


LTX_PRESETS: Dict[str, List[Tuple[int, int, str]]] = {
    "1:1": [
        (320, 320, "Fast Draft"),
        (640, 640, "Preview"),
        (768, 768, "High Detail"),
        (960, 960, "Native"),
        (1184, 1184, "HD Output"),
        (1440, 1440, "Full HD Output"),
    ],
    "2:3": [
        (256, 384, "Fast Draft"),
        (512, 768, "Preview"),
        (640, 960, "High Detail"),
        (768, 1152, "Native"),
        (960, 1440, "HD Output"),
        (1152, 1728, "Full HD Output"),
    ],
    "3:2": [
        (384, 256, "Fast Draft"),
        (768, 512, "Preview"),
        (960, 640, "High Detail"),
        (1152, 768, "Native"),
        (1440, 960, "HD Output"),
        (1728, 1152, "Full HD Output"),
    ],
    "3:4": [
        (256, 352, "Fast Draft"),
        (512, 704, "Preview"),
        (640, 864, "High Detail"),
        (864, 1152, "Native"),
        (1056, 1408, "HD Output"),
        (1248, 1664, "Full HD Output"),
    ],
    "4:3": [
        (352, 256, "Fast Draft"),
        (704, 512, "Preview"),
        (864, 640, "High Detail"),
        (1152, 864, "Native"),
        (1408, 1056, "HD Output"),
        (1664, 1248, "Full HD Output"),
    ],
    "9:16": [
        (288, 512, "Fast Draft"),
        (544, 960, "Preview"),
        (672, 1184, "High Detail"),
        (736, 1312, "Native"),
        (864, 1536, "HD Output"),
        (1088, 1920, "Full HD Output"),
    ],
    "16:9": [
        (512, 288, "Fast Draft"),
        (960, 544, "Preview"),
        (1184, 672, "High Detail"),
        (1312, 736, "Native"),
        (1536, 864, "HD Output"),
        (1920, 1088, "Full HD Output"),
    ],
}


MODEL_CONFIG: Dict[str, Dict] = {
    "WAN 2.2": {
        "aspect_order": ("1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9"),
        "fallback_aspect": "1:1",
        "presets": WAN_PRESETS,
        "default_divisible_by": 16,
    },
    "MiniMax H3": {
        "aspect_order": ("1:1", "3:4", "4:3", "9:16", "16:9", "21:9"),
        "fallback_aspect": "16:9",
        "presets": MINIMAX_PRESETS,
        "default_divisible_by": 32,
    },
    "LTX": {
        "aspect_order": ("1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9"),
        "fallback_aspect": "1:1",
        "presets": LTX_PRESETS,
        "default_divisible_by": 32,
    },
}


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[\(\)]", "", value or "").lower()).strip()


def _parse_size(value: str) -> Optional[Tuple[int, int]]:
    m = re.search(r"(\d+)\s*[x×]\s*(\d+)", value or "", flags=re.IGNORECASE)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def _parse_aspect_ratio_value(aspect_ratio: str) -> Optional[float]:
    m = re.match(r"^\s*(\d+)\s*:\s*(\d+)\s*$", aspect_ratio or "")
    if not m:
        return None
    w = max(1, int(m.group(1)))
    h = max(1, int(m.group(2)))
    return float(w) / float(h)


def _best_aspect_ratio(width: int, height: int, aspect_order: Tuple[str, ...], fallback: str) -> str:
    if width <= 0 or height <= 0:
        return fallback
    target = float(width) / float(height)
    best_ar = fallback
    best_delta = float("inf")
    for ar in aspect_order:
        ratio = _parse_aspect_ratio_value(ar)
        if ratio is None:
            continue
        delta = abs(ratio - target)
        if delta < best_delta:
            best_delta = delta
            best_ar = ar
    return best_ar


def _rows_for(presets: Dict[str, List[Tuple[int, int, str]]], aspect_ratio: str, fallback: str) -> List[Tuple[int, int, str]]:
    return presets.get(aspect_ratio) or presets.get(fallback) or list(next(iter(presets.values())))


def _labels_for(presets: Dict[str, List[Tuple[int, int, str]]], aspect_ratio: str, fallback: str) -> List[str]:
    rows = _rows_for(presets, aspect_ratio, fallback)
    return [f"{note} — {w}×{h}" for w, h, note in rows]


def _tier_index_for_value(presets: Dict, aspect_ratio: str, value: str, fallback: str) -> Optional[int]:
    rows = _rows_for(presets, aspect_ratio, fallback)
    normalized_value = _normalize_text(value)

    note_matches = sorted(
        enumerate(rows),
        key=lambda indexed_row: len(_normalize_text(indexed_row[1][2])),
        reverse=True,
    )
    for i, (_, _, note) in note_matches:
        if _normalize_text(note) in normalized_value:
            return i

    m = re.match(r"\s*(\d+)\s*[\.\)]", value or "")
    if m:
        idx = int(m.group(1)) - 1
        return max(0, min(idx, len(rows) - 1))

    parsed_size = _parse_size(value)
    if parsed_size is not None:
        width, height = parsed_size
        for i, (row_w, row_h, _) in enumerate(rows):
            if row_w == width and row_h == height:
                return i

    return None


def _parse_resolution(presets: Dict, aspect_ratio: str, resolution_label: str, fallback: str) -> Tuple[int, int]:
    idx = _tier_index_for_value(presets, aspect_ratio, resolution_label, fallback)
    if idx is not None:
        w, h, _ = _rows_for(presets, aspect_ratio, fallback)[idx]
        return w, h
    parsed_size = _parse_size(resolution_label)
    if parsed_size is not None:
        return parsed_size
    w, h, _ = _rows_for(presets, aspect_ratio, fallback)[0]
    return w, h


def _round_to_multiple(value: int, multiple: int) -> int:
    if multiple <= 0:
        return int(value)
    return max(multiple, round(value / multiple) * multiple)


def _adaptive_size(width: int, height: int, target_pixels: int, divisible_by: int) -> Tuple[int, int]:
    if width <= 0 or height <= 0:
        return (divisible_by, divisible_by)
    ratio = float(width) / float(height)
    ideal_width = math.sqrt(float(target_pixels) * ratio)
    ideal_height = math.sqrt(float(target_pixels) / ratio)
    return (
        max(divisible_by, round(ideal_width / divisible_by) * divisible_by),
        max(divisible_by, round(ideal_height / divisible_by) * divisible_by),
    )


def _image_dimensions(image) -> Optional[Tuple[int, int]]:
    if image is None:
        return None
    if isinstance(image, (list, tuple)):
        if not image:
            return None
        image = image[0]
    shape = getattr(image, "shape", None)
    if shape is None:
        return None
    dims = tuple(int(v) for v in shape)
    if len(dims) == 4:
        _, h, w, _ = dims
        return (w, h)
    if len(dims) == 3:
        if dims[-1] in (1, 3, 4):
            h, w, _ = dims
            return (w, h)
        if dims[0] in (1, 3, 4):
            _, h, w = dims
            return (w, h)
        h, w, _ = dims
        return (w, h)
    if len(dims) == 2:
        h, w = dims
        return (w, h)
    return None


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (0, 0, 0)


def _resize_tensor(
    tensor: torch.Tensor,
    target_w: int,
    target_h: int,
    upscale: bool,
    upscale_method: str,
    small_image_mode: str,
    pad_color: str,
    is_mask: bool = False,
) -> torch.Tensor:
    method_map = {
        "lanczos": Image.LANCZOS,
        "bilinear": Image.BILINEAR,
        "bicubic": Image.BICUBIC,
        "nearest": Image.NEAREST,
    }
    resize_method = method_map.get(upscale_method, Image.LANCZOS)
    mask_resize_method = Image.NEAREST if upscale_method == "nearest" else resize_method

    results = []
    is_single_channel = len(tensor.shape) == 3
    for i in range(tensor.shape[0]):
        arr = tensor[i].cpu().numpy()
        if is_mask:
            arr = (arr * 255).astype(np.uint8)
        else:
            arr = (arr * 255).astype(np.uint8)
        mode = "L" if is_mask or is_single_channel else "RGB"
        pil_img = Image.fromarray(arr, mode=mode)

        orig_w, orig_h = pil_img.width, pil_img.height
        is_upscale = target_w > orig_w or target_h > orig_h
        do_resize = not is_upscale or (is_upscale and upscale)

        if do_resize:
            if small_image_mode != "none" and (orig_w < target_w or orig_h < target_h):
                target_ar = target_w / target_h
                img_ar = orig_w / orig_h
                if small_image_mode == "crop":
                    if img_ar > target_ar:
                        tmp_h = target_h
                        tmp_w = int(tmp_h * img_ar)
                    else:
                        tmp_w = target_w
                        tmp_h = int(tmp_w / img_ar)
                    pil_img = pil_img.resize((tmp_w, tmp_h), mask_resize_method if is_mask else resize_method)
                    left = (pil_img.width - target_w) // 2
                    top = (pil_img.height - target_h) // 2
                    pil_img = pil_img.crop((left, top, left + target_w, top + target_h))
                elif small_image_mode == "pad":
                    pil_img.thumbnail((target_w, target_h), mask_resize_method if is_mask else resize_method)
                    fill = 0 if is_mask else _hex_to_rgb(pad_color)
                    bg = Image.new(mode, (target_w, target_h), fill)
                    offset = ((target_w - pil_img.width) // 2, (target_h - pil_img.height) // 2)
                    bg.paste(pil_img, offset)
                    pil_img = bg
            else:
                pil_img = pil_img.resize((target_w, target_h), mask_resize_method if is_mask else resize_method)

        arr_out = np.array(pil_img).astype(np.float32) / 255.0
        if is_mask:
            if len(arr_out.shape) == 3:
                arr_out = arr_out[..., 0]
        results.append(arr_out)

    out = torch.from_numpy(np.stack(results)).to(tensor.device)
    return out


class ComfyUI_PerfectVideoResolution:
    @classmethod
    def INPUT_TYPES(cls):
        default_model = "WAN 2.2"
        config = MODEL_CONFIG[default_model]
        aspect_choices = list(config["aspect_order"])
        default_ar = config["fallback_aspect"]
        resolution_choices = _labels_for(config["presets"], default_ar, default_ar)
        default_res = resolution_choices[0]

        return {
            "required": {
                "model": (["WAN 2.2", "MiniMax H3", "LTX"], {"default": default_model}),
                "aspect_ratio": (aspect_choices, {"default": default_ar}),
                "resolution": (resolution_choices, {"default": default_res}),
                "divisible_by": ("INT", {"default": 16, "min": 1, "max": 128, "step": 1}),
                "upscale": ("BOOLEAN", {"default": False}),
                "upscale_method": (["lanczos", "bilinear", "bicubic", "nearest"], {"default": "lanczos"}),
                "small_image_mode": (["none", "crop", "pad"], {"default": "none"}),
                "pad_color": ("STRING", {"default": "#000000"}),
            },
            "optional": {
                "image": ("IMAGE",),
                "image2": ("IMAGE",),
                "mask": ("MASK",),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("INT", "INT", "IMAGE", "IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("width", "height", "IMAGE", "IMAGE2", "MASK", "resolution_info")
    FUNCTION = "calculate"
    CATEGORY = "utils"

    @classmethod
    def VALIDATE_INPUTS(cls, resolution=None):
        return True

    def calculate(
        self,
        model: str,
        aspect_ratio: str,
        resolution: str,
        divisible_by: int,
        upscale: bool,
        upscale_method: str,
        small_image_mode: str,
        pad_color: str,
        image=None,
        image2=None,
        mask=None,
        unique_id=None,
    ):
        config = MODEL_CONFIG.get(model, MODEL_CONFIG["WAN 2.2"])
        presets = config["presets"]
        aspect_order = config["aspect_order"]
        fallback_aspect = config["fallback_aspect"]
        default_divisible_by = config["default_divisible_by"]

        if divisible_by <= 0:
            divisible_by = default_divisible_by

        image_dims = _image_dimensions(image)
        resolved_aspect = aspect_ratio
        resolved_resolution_label = resolution
        target_w, target_h = _parse_resolution(presets, aspect_ratio, resolution, fallback_aspect)

        if image_dims is not None:
            image_w, image_h = image_dims
            resolved_aspect = _best_aspect_ratio(image_w, image_h, aspect_order, fallback_aspect)

            if model == "MiniMax H3":
                idx = _tier_index_for_value(presets, aspect_ratio, resolution, fallback_aspect)
                if idx is None:
                    parsed = _parse_size(resolution)
                    target_pixels = parsed[0] * parsed[1] if parsed else MINIMAX_TARGET_PIXELS[0]
                else:
                    target_pixels = MINIMAX_TARGET_PIXELS[idx]
                target_w, target_h = _adaptive_size(image_w, image_h, target_pixels, divisible_by)
                resolved_resolution_label = _labels_for(presets, resolved_aspect, fallback_aspect)[
                    idx if idx is not None else 0
                ]
            else:
                target_w, target_h = _parse_resolution(presets, resolved_aspect, resolution, fallback_aspect)
                resolved_resolution_label = _labels_for(presets, resolved_aspect, fallback_aspect)[
                    _tier_index_for_value(presets, resolved_aspect, resolution, fallback_aspect) or 0
                ]

        target_w = int(_round_to_multiple(target_w, divisible_by))
        target_h = int(_round_to_multiple(target_h, divisible_by))

        if image is not None:
            image_out = _resize_tensor(
                image, target_w, target_h, upscale, upscale_method, small_image_mode, pad_color, is_mask=False
            )
        else:
            image_out = torch.zeros((1, target_h, target_w, 3), dtype=torch.float32)

        if image2 is not None:
            image2_out = _resize_tensor(
                image2, target_w, target_h, upscale, upscale_method, small_image_mode, pad_color, is_mask=False
            )
        else:
            image2_out = torch.zeros((1, target_h, target_w, 3), dtype=torch.float32)

        if mask is not None:
            mask_out = _resize_tensor(
                mask, target_w, target_h, upscale, upscale_method, small_image_mode, pad_color, is_mask=True
            )
        else:
            mask_out = torch.ones((1, target_h, target_w), dtype=torch.float32)

        approx_mb = (target_w * target_h * 3) / (1024 * 1024)
        resolution_info = f"{target_w}x{target_h} | {approx_mb:.2f}MB | {target_w*target_h:,} pixels"

        if unique_id and image is not None:
            try:
                from server import PromptServer
                memory_size_mb = (image_out.numel() * image_out.element_size()) / (1024 * 1024)
                PromptServer.instance.send_progress_text(
                    f"<tr><td>Output: </td>"
                    f"<td><b>{target_w}</b> x <b>{target_h}</b> | {memory_size_mb:.2f}MB | {target_w*target_h:,} pixels</td></tr>",
                    unique_id,
                )
            except Exception:
                pass

        result = (int(target_w), int(target_h), image_out, image2_out, mask_out, resolution_info)

        if image_dims is None:
            return result

        state = {
            "model": model,
            "aspect_ratio": resolved_aspect,
            "resolution": resolved_resolution_label,
            "source_width": image_dims[0],
            "source_height": image_dims[1],
        }
        return {
            "ui": {"perfect_video_resolution_state": [state]},
            "result": result,
        }
