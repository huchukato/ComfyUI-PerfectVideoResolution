import { app } from "../../scripts/app.js";

const MODEL_CONFIGS = {
  "WAN 2.2": {
    fallbackAspect: "1:1",
    presets: {
      "1:1": [
        [480, 480, "Fast Draft"],
        [640, 640, "Preview"],
        [832, 832, "High Detail"],
        [960, 960, "Wan 2.2 Native"],
      ],
      "2:3": [
        [384, 576, "Fast Draft"],
        [512, 768, "Preview"],
        [672, 1008, "High Detail"],
        [768, 1168, "Wan 2.2 Native"],
      ],
      "3:2": [
        [576, 384, "Fast Draft"],
        [768, 512, "Preview"],
        [1008, 672, "High Detail"],
        [1168, 768, "Wan 2.2 Native"],
      ],
      "3:4": [
        [432, 576, "Fast Draft"],
        [576, 768, "Preview"],
        [720, 960, "High Detail"],
        [816, 1104, "Wan 2.2 Native"],
      ],
      "4:3": [
        [576, 432, "Fast Draft"],
        [768, 576, "Preview"],
        [960, 720, "High Detail"],
        [1104, 816, "Wan 2.2 Native"],
      ],
      "9:16": [
        [352, 624, "Fast Draft"],
        [480, 848, "Preview"],
        [624, 1104, "High Detail"],
        [720, 1280, "Wan 2.2 Native"],
      ],
      "16:9": [
        [624, 352, "Fast Draft"],
        [848, 480, "Preview"],
        [1104, 624, "High Detail"],
        [1280, 720, "Wan 2.2 Native"],
      ],
    },
  },
  "MiniMax H3": {
    fallbackAspect: "16:9",
    presets: {
      "1:1": [
        [512, 512, "Fast Draft"],
        [640, 640, "Preview"],
        [768, 768, "High Detail"],
        [1024, 1024, "Native"],
        [1152, 1152, "1.5K"],
        [1440, 1440, "1080P Class"],
        [1536, 1536, "2K"],
      ],
      "3:4": [
        [448, 576, "Fast Draft"],
        [576, 736, "Preview"],
        [672, 896, "High Detail"],
        [864, 1184, "Native"],
        [992, 1344, "1.5K"],
        [1248, 1664, "1080P Class"],
        [1344, 1760, "2K"],
      ],
      "4:3": [
        [576, 448, "Fast Draft"],
        [736, 576, "Preview"],
        [896, 672, "High Detail"],
        [1184, 864, "Native"],
        [1344, 992, "1.5K"],
        [1664, 1248, "1080P Class"],
        [1760, 1344, "2K"],
      ],
      "9:16": [
        [384, 672, "Fast Draft"],
        [480, 864, "Preview"],
        [576, 1024, "High Detail"],
        [768, 1344, "Native"],
        [864, 1536, "1.5K"],
        [1088, 1920, "1080P Class"],
        [1152, 2048, "2K"],
      ],
      "16:9": [
        [672, 384, "Fast Draft"],
        [864, 480, "Preview"],
        [1024, 576, "High Detail"],
        [1344, 768, "Native"],
        [1536, 864, "1.5K"],
        [1920, 1088, "1080P Class"],
        [2048, 1152, "2K"],
      ],
      "21:9": [
        [768, 320, "Fast Draft"],
        [992, 416, "Preview"],
        [1184, 512, "High Detail"],
        [1536, 672, "Native"],
        [1760, 768, "1.5K"],
        [2208, 960, "1080P Class"],
        [2336, 992, "2K"],
      ],
    },
  },
  "LTX": {
    fallbackAspect: "1:1",
    presets: {
      "1:1": [
        [320, 320, "Fast Draft"],
        [640, 640, "Preview"],
        [768, 768, "High Detail"],
        [960, 960, "Native"],
        [1184, 1184, "HD Output"],
        [1440, 1440, "Full HD Output"],
      ],
      "2:3": [
        [256, 384, "Fast Draft"],
        [512, 768, "Preview"],
        [640, 960, "High Detail"],
        [768, 1152, "Native"],
        [960, 1440, "HD Output"],
        [1152, 1728, "Full HD Output"],
      ],
      "3:2": [
        [384, 256, "Fast Draft"],
        [768, 512, "Preview"],
        [960, 640, "High Detail"],
        [1152, 768, "Native"],
        [1440, 960, "HD Output"],
        [1728, 1152, "Full HD Output"],
      ],
      "3:4": [
        [256, 352, "Fast Draft"],
        [512, 704, "Preview"],
        [640, 864, "High Detail"],
        [864, 1152, "Native"],
        [1056, 1408, "HD Output"],
        [1248, 1664, "Full HD Output"],
      ],
      "4:3": [
        [352, 256, "Fast Draft"],
        [704, 512, "Preview"],
        [864, 640, "High Detail"],
        [1152, 864, "Native"],
        [1408, 1056, "HD Output"],
        [1664, 1248, "Full HD Output"],
      ],
      "9:16": [
        [288, 512, "Fast Draft"],
        [544, 960, "Preview"],
        [672, 1184, "High Detail"],
        [736, 1312, "Native"],
        [864, 1536, "HD Output"],
        [1088, 1920, "Full HD Output"],
      ],
      "16:9": [
        [512, 288, "Fast Draft"],
        [960, 544, "Preview"],
        [1184, 672, "High Detail"],
        [1312, 736, "Native"],
        [1536, 864, "HD Output"],
        [1920, 1088, "Full HD Output"],
      ],
    },
  },
};

function configForNode(node) {
  if (node.comfyClass !== "ComfyUI-PerfectVideoResolution") return null;
  return MODEL_CONFIGS;
}

function widgetValue(node, widget) {
  if (!widget) return undefined;
  const index = node.widgets?.indexOf(widget) ?? -1;
  if (index >= 0 && Array.isArray(node.widgets_values)) {
    const saved = node.widgets_values[index];
    if (saved != null) return saved;
  }
  return widget.value;
}

function syncWidgetValues(node) {
  if (!Array.isArray(node.widgets_values) || !Array.isArray(node.widgets)) return;
  node.widgets.forEach((widget, index) => {
    node.widgets_values[index] = widget.value;
  });
}

function getWidgets(node) {
  return {
    modelWidget: node.widgets?.find((w) => w.name === "model"),
    aspectWidget: node.widgets?.find((w) => w.name === "aspect_ratio"),
    resWidget: node.widgets?.find((w) => w.name === "resolution"),
  };
}

function rowsFor(config, model, aspectRatio) {
  const m = config[model];
  return m.presets[aspectRatio] ?? m.presets[m.fallbackAspect];
}

function labelsFor(config, model, aspectRatio) {
  return rowsFor(config, model, aspectRatio).map(([w, h, note]) => `${note} — ${w}×${h}`);
}

function normalizeText(str) {
  return (str || "")
    .toLowerCase()
    .replaceAll(/[()]/g, "")
    .replaceAll(/\s+/g, " ")
    .trim();
}

function parseSize(str) {
  const normalized = (str || "").replaceAll("×", "x");
  const m = /(\d+)\s*x\s*(\d+)/i.exec(normalized);
  if (!m) return null;
  return { w: parseInt(m[1], 10), h: parseInt(m[2], 10) };
}

function sizeForLabel(config, model, aspectRatio, value) {
  const parsed = parseSize(value);
  if (parsed) return parsed;
  const rows = rowsFor(config, model, aspectRatio);
  for (const [w, h, note] of rows) {
    if (normalizeText(value).includes(normalizeText(note))) return { w, h };
  }
  const row = rows[0];
  return { w: row[0], h: row[1] };
}

function nearestOption(options, target) {
  if (!target) return options[0];
  let best = options[0];
  let bestDelta = Infinity;
  for (const opt of options) {
    const size = parseSize(opt);
    if (!size) continue;
    const delta = Math.abs(size.w * size.h - target.w * target.h);
    if (delta < bestDelta) {
      bestDelta = delta;
      best = opt;
    }
  }
  return best;
}

function updateResolutionOptions(node, config, preferred = {}) {
  const { modelWidget, aspectWidget, resWidget } = getWidgets(node);
  if (!modelWidget || !aspectWidget || !resWidget) return;

  const model = preferred.model ?? modelWidget.value;
  const modelConfig = config[model];
  if (!modelConfig) return;

  const aspectOptions = Object.keys(modelConfig.presets);
  let aspectRatio = preferred.aspectRatio ?? aspectWidget.value;
  if (!aspectOptions.includes(aspectRatio)) {
    aspectRatio = modelConfig.fallbackAspect;
  }
  aspectWidget.options = aspectWidget.options ?? {};
  aspectWidget.options.values = aspectOptions;
  aspectWidget.value = aspectRatio;

  const options = labelsFor(config, model, aspectRatio);
  const currentValue = preferred.resolution ?? resWidget.value;
  let nextValue;
  if (currentValue && options.includes(currentValue)) {
    nextValue = currentValue;
  } else {
    nextValue = nearestOption(options, sizeForLabel(config, model, aspectRatio, currentValue)) ?? options[0];
  }
  resWidget.options = resWidget.options ?? {};
  resWidget.options.values = options;
  resWidget.value = nextValue;

  syncWidgetValues(node);
  node.setDirtyCanvas(true, true);
}

function extractState(output) {
  const state = output?.perfect_video_resolution_state;
  return Array.isArray(state) ? state[0] : state;
}

app.registerExtension({
  name: "perfect_video_resolution.dynamic_lists",
  async nodeCreated(node) {
    const config = configForNode(node);
    if (!config) return;

    const { modelWidget, aspectWidget } = getWidgets(node);
    if (!modelWidget || !aspectWidget) return;

    const origModelCallback = modelWidget.callback;
    modelWidget.callback = (value) => {
      origModelCallback?.call(node, value);
      updateResolutionOptions(node, config, { model: value });
    };

    const origAspectCallback = aspectWidget.callback;
    aspectWidget.callback = (value) => {
      origAspectCallback?.call(node, value);
      updateResolutionOptions(node, config, { aspectRatio: value });
    };

    const onExecuted = node.onExecuted;
    node.onExecuted = function (output) {
      onExecuted?.call(this, output);
      const state = extractState(output);
      if (!state) return;
      const model = state.model;
      if (model && MODEL_CONFIGS[model]) {
        updateResolutionOptions(this, config, {
          model: model,
          aspectRatio: state.aspect_ratio,
          resolution: state.resolution,
        });
      }
    };

    updateResolutionOptions(node, config);
  },

  loadedGraphNode(node) {
    const config = configForNode(node);
    if (!config) return;
    updateResolutionOptions(node, config);
  },
});
