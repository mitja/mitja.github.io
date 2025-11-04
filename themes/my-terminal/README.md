# My Terminal Customizations

Custom shortcodes and enhancements for the [Terminal theme](https://github.com/panr/hugo-theme-terminal).

This is a component theme that adds missing shortcodes (alert, youtubeLite, carousel) that are commonly used with the Blowfish theme, adapted to work with the Terminal theme's aesthetic.

## Usage

This theme is designed to be used in composition with the Terminal theme:

```bash
# Run with Terminal theme + customizations
hugo server -t my-terminal,terminal

# Run with Blowfish theme (uses Blowfish's native shortcodes)
hugo server -t blowfish
```

## Shortcodes Included

### Alert

Display alert boxes with emoji icons:

```
{{< alert "lightbulb" >}}
This is an info message
{{< /alert >}}
```

Supported icons:
- `triangle-exclamation` → ⚠️
- `circle-info`, `info` → ℹ️
- `circle-check`, `check` → ✓
- `lightbulb` → 💡
- `fire` → 🔥
- `bug` → 🐛
- `rocket` → 🚀

### YouTube Lite

Embed YouTube videos with terminal-style borders:

```
{{< youtubeLite id="VIDEO_ID" label="Video Title" >}}
```

### Carousel

Image carousel with navigation and auto-play:

```
{{< carousel images="gallery/*" interval="5000" aspectRatio="16-9" >}}
```

## Files Structure

```
themes/my-terminal/
├── layouts/
│   ├── shortcodes/
│   │   ├── alert.html
│   │   ├── youtubeLite.html
│   │   └── carousel.html
│   └── partials/
│       └── extended_head.html
├── static/
│   └── js/
│       └── carousel.js
├── theme.toml
└── README.md
```

## Development

To modify the shortcodes, edit the files in this theme. Changes will be picked up by Hugo's live reload when running the server.

## License

MIT
