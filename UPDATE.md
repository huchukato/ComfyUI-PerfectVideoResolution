# Update Log

## Version 0.1.1

- Added `use_image_aspect` toggle: when disabled, the manual `aspect_ratio` and `resolution` widgets are respected even with images connected — useful for reference-image workflows (e.g. MiniMax R2VA) where inputs are character sheets, not frame sources. Default stays `True`, so existing workflows keep auto-detecting aspect from the input image.
