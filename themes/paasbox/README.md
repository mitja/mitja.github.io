# paasbox theme for Hugo

The look of [paasbox.com](../../../paasbox-web) — paper and ink, Fraunces for
headings, Inter for text, and hand-drawn markers — as a theme component on top
of [Blowfish](https://github.com/nunocoracao/blowfish), with two colours of its
own: a petrol accent and the red of the KI Bauer cover (see below).

The source of truth is `paasbox-web/src/styles/` (`paasbox.css` and
`global.css`). When a value changes there, change it in
`assets/css/schemes/paasbox.css` too.

## Use

```toml
# config/_default/hugo.toml
theme = ["paasbox", "blowfish"]

# config/_default/params.toml
colorScheme = "paasbox"

# config/_default/markup.toml — optional, for ==text== and ++text++
[goldmark.extensions.extras.mark]
  enable = true
[goldmark.extensions.extras.insert]
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

paasbox.com's pages use two annotations: a translucent, tilted block behind
one phrase of a heading, and fine wavy or dotted underlines in running text.
Both have a Markdown form:

| Write | Result |
|---|---|
| `## Deploy ==an app==` | the block behind "an app" (coral, or the tone of a `pb-tone-*` ancestor) |
| `++text++` | a fine wavy underline, same colour rule |
| `{{< hl >}}…{{< /hl >}}` | the block in a colour of its own |
| `{{< hl warning >}}…{{< /hl >}}` | the same in amber |
| `{{< wavy >}}…{{< /wavy >}}`, `{{< wavy sm accent >}}` | wavy underline |
| `{{< dotted lg success >}}…{{< /dotted >}}` | dotted underline |
| `{{< marker >}}text{{< /marker >}}` | a felt-tip stroke over the lower half, tilted left |
| `{{< marker mint underline >}}…{{< /marker >}}` | a marker stroke under the text |
| `{{< marker coral circle right >}}…{{< /marker >}}` | a hand-drawn ring, tilted right |
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

`==text==` and `++text++` are styled anywhere inside `<main>`, so they also work
in front-matter text that a template runs through `markdownify` (the landing
page does). A class `pb-tone-primary` (or `-secondary`, `-accent`, `-success`,
`-warning`, `-error`) on an ancestor, such as the heading, sets their colour;
paasbox.com goes round accent, primary, success and warning from one heading to
the next. The block does not wrap, as on paasbox.com, so mark a phrase, not a
sentence.

`{{< marker >}}` is paasbox-web's Marker component. paasbox-web defines it,
but its pages don't use it.

The text inside a shortcode may contain Markdown (`**bold**`, `` `code` ``).
A margin note's body is block Markdown, so it can hold several paragraphs or a list.

Templates and hand-written HTML can use the classes directly:
`<span class="pb-marker pb-marker--circle" data-tone="coral">`, and
`class="pb-display"` sets any element in the heading face.

## Tokens for site CSS

The theme defines paasbox's custom properties, and they flip with dark mode.
Site CSS can use them, with a fallback for plain Blowfish:
`--pb-serif`, `--pb-sans`, `--pb-paper`, `--pb-paper-raised`, `--pb-ink`,
`--pb-ink-soft`, `--pb-line`, `--pb-accent`, `--pb-accent-strong`,
`--pb-marker`, `--pb-mint`, `--pb-coral`, `--pb-blue`, `--pb-shadow`, and the
coral call-to-action `--pb-cta`, `--pb-cta-hover`, `--pb-cta-ink` (primary
buttons only, never links). Blowfish's own `--color-neutral-*`,
`--color-primary-*` (petrol) and `--color-secondary-*` (coral) ramps carry
the same palette.

## Differences from paasbox-web

- **Class names carry a `pb-` prefix.** paasbox's `.highlight` is the class Hugo
  gives every code block, so it is `.pb-highlight` here. The same goes for the
  underline classes.
- **Margin notes stay in the text column.** On paasbox they hang in the right
  margin from 90rem. In Blowfish that margin holds the table of contents, so
  here they float beside the text from 48rem, and the next heading clears them.
- **Dark mode** is Blowfish's `html.dark`, not Starlight's `[data-theme]`, and
  its paper is kibauer's cool slate (`oklch(20% 0.02 270)`, from
  `../kibauer/src/styles/theme.css`) rather than paasbox's green-black.
- **The accent is petrol, not forest green:** `#00657f` light (6.2:1 on the
  paper), `#7fc7df` dark (9.6:1 on the slate), oklch hue 222. Green read as a
  second colour world on the slate dark paper; petrol sits next to its blue
  and opposite the coral buttons and the yellow marker. Green stays only as
  the `success` colour and the explicit `mint` tone.
- **The warm colour is the KI Bauer cover red,** not paasbox's muted salmon:
  `--pb-coral` is the cover's `#e94326` (`#fb836c` on the slate) for wavy
  underlines, the quote bar and `accent` marks; the CTA (`--pb-cta`, primary
  buttons only) is one step darker, `#d43518` with white text (4.9:1), hover
  `#af2d16`, the same in both modes. `--color-secondary-*` is that red's ramp.
- **Highlights are yellow** like a highlighter pen: `==text==` and section
  headings. `pb-tone-*` picks another colour where wanted.
- **An SVG logo follows the scheme.** Blowfish inlines an SVG `params.logo`;
  shapes with the classes `pb-logo-disc` and `pb-logo-mark` take the accent
  and the paper, in both modes. The site's logo and favicons are built by
  `scripts/logo.py` at the repository root.
- **Page titles stay plain.** paasbox.com highlights a phrase of its hero;
  here only section headings carry a highlight.

## What it overrides in Blowfish

No templates, only CSS: page titles (h1) stay without annotations, so there
is nothing to change in Blowfish's layouts. It needs no `!important` because Blowfish's compiled
Tailwind CSS sits in cascade layers, and the unlayered scheme file beats it.
