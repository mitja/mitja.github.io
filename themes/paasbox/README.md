# paasbox theme for Hugo

The look of [paasbox.com](../../../paasbox-web) — paper and ink, a forest-green
accent, a muted-salmon coral, Fraunces for headings, Inter for text, and
hand-drawn markers — as a theme component on top of
[Blowfish](https://github.com/nunocoracao/blowfish).

The source of truth is `paasbox-web/src/styles/` (`paasbox.css` and
`global.css`). When a value changes there, change it in
`assets/css/schemes/paasbox.css` too.

## Use

```toml
# config/_default/hugo.toml
theme = ["paasbox", "blowfish"]

# config/_default/params.toml
colorScheme = "paasbox"

# config/_default/markup.toml — optional, for ==text==
[goldmark.extensions.extras.mark]
  enable = true
```

`colorScheme = "paasbox"` switches the whole look, not only the colours:
Blowfish loads exactly one file by name from a theme, `css/schemes/<name>.css`,
so the fonts, headings and markers live there too. The site's own
`assets/css/custom.css` is loaded after it and stays free for overrides. Keep in
mind that a heading rule there with `.prose h2` beats the theme's `main h2`.

The fonts are self-hosted from `static/fonts/` (latin and latin-ext, SIL Open
Font License, see the `OFL-*.txt` files there). Nothing is loaded from Google
Fonts.

## Markers in content

| Write | Result |
|---|---|
| `==text==` | yellow marker |
| `{{< marker >}}text{{< /marker >}}` | yellow marker, tilted left |
| `{{< marker mint underline >}}…{{< /marker >}}` | a marker stroke under the text |
| `{{< marker coral circle right >}}…{{< /marker >}}` | a hand-drawn ring, tilted right |
| `{{< hl >}}…{{< /hl >}}` | translucent block in a role colour |
| `{{< hl warning >}}…{{< /hl >}}` | the same in amber |
| `{{< wavy >}}…{{< /wavy >}}`, `{{< wavy sm accent >}}` | wavy underline |
| `{{< dotted lg success >}}…{{< /dotted >}}` | dotted underline |
| `{{< inline-note note="…" >}}word{{< /inline-note >}}` | a bubble on hover and keyboard focus |
| `{{< margin-note >}}…{{< /margin-note >}}` | a taped-on note beside the paragraph that follows |

Options can be written as words in any order (`{{< marker coral circle >}}`)
or by name (`{{< marker tone="coral" style="circle" >}}`). An unknown option
fails the build with the file and line, so a typo cannot ship.

- **marker**: `tone` yellow · mint · coral · blue; `style` highlight ·
  underline · circle; `tilt` left · right · none
- **hl**: `color` primary · secondary · accent · success · warning · error
- **wavy**, **dotted**: `color` as for hl; `size` sm · lg
- **inline-note**: `note="…"` (required); `tone` yellow · mint · coral · blue
- **margin-note**: `label="…"` (default "Note" / "Randnotiz"); `tone` ink ·
  mint · coral · blue; `side` right · left

The text inside a shortcode may contain Markdown (`**bold**`, `` `code` ``).
A margin note's body is block Markdown, so it can hold several paragraphs or a list.

Templates and hand-written HTML can use the classes directly:
`<span class="pb-marker pb-marker--circle" data-tone="coral">`, and
`class="pb-display"` sets any element in the heading face.

## Differences from paasbox-web

- **Class names carry a `pb-` prefix.** paasbox's `.highlight` is the class Hugo
  gives every code block, so it is `.pb-highlight` here. The same goes for the
  underline classes.
- **Margin notes stay in the text column.** On paasbox they hang in the right
  margin from 90rem. In Blowfish that margin holds the table of contents, so
  here they float beside the text from 48rem, and the next heading clears them.
- **Dark mode** is Blowfish's `html.dark`, not Starlight's `[data-theme]`.

## What it overrides in Blowfish

- `layouts/partials/home/profile.html`: Blowfish's, with a marker under the
  author's name. Compare the two when Blowfish is updated.

Everything else is CSS. It needs no `!important` because Blowfish's compiled
Tailwind CSS sits in cascade layers, and the unlayered scheme file beats it.
