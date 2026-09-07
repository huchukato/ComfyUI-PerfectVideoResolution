from .perfect_video_resolution import ComfyUI_PerfectVideoResolution

NODE_CLASS_MAPPINGS = {
    "ComfyUI-PerfectVideoResolution": ComfyUI_PerfectVideoResolution,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI-PerfectVideoResolution": "Perfect Video Resolution",
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
