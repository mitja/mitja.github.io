---
title: "Creating Embeddable Widgets with Python Air"
date: 2025-10-17
categories: ["AI Engineering", "Blog", "Python"]
tags: ["Python", "Air", "FastAPI", "Web Development", "Widgets"]
draft: true
---

[Python Air](https://github.com/feldroy/air) is a new Python web framework by the authors of Two Scoops of Django. Air is still very experimental, but already suitable to create small tools, dashboards, demos, etc. which are perfect for embedding in blog posts, for example. 

I've tried this and created step-by-step guides for building Python Air apps that can be embedded on other websites with iFrames and JavaScript injection.

## The Two Main Approaches

### Iframe Embedding (Simple but Isolated)

Iframes load your widget in a completely separate browsing context. This provides strong isolation but comes with limitations.

**Pros:**
- Simple to implement
- Strong isolation (your widget can't interfere with the parent page)
- Works everywhere (no CORS issues)
- Parent page can't accidentally break your widget styles

**Cons:**
- Fixed size (harder to make responsive)
- Can't easily communicate with parent page
- Less integrated feel
- Some users block third-party iframes
- Can't access parent page DOM

### Script Injection (More Flexible)

Script injection loads JavaScript that fetches and injects HTML into the parent page. This provides better integration but requires additional work (JavaScript, CORS configuration).

**Pros:**
- More flexible sizing and layout
- Can interact with parent page and adapt to it's context
- Feels more integrated

**Cons:**
- Requires proper CORS setup
- Widget CSS and JS can conflict with parent page
- More complex to implement

## The Iframe Approach Step-by-Step

I started by creating a simple embeddable widget using iframes with the help of Claude Code:

```python
import air
from fastapi.middleware.cors import CORSMiddleware

app = air.Air()

# CORS middleware is optional for iframes, but good practice
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # restrict this for production ...
    allow_methods=["GET"],
    allow_headers=["*"], # also to be restricted ...
)

# the iframe widget endpoint
@app.get("/widget/embed")
async def widget_iframe():
    """Full HTML page designed to be embedded in iframe"""
    return air.Html(
        air.Head(
            air.Style("""
                body {
                    margin: 0;
                    padding: 20px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                .widget-container {
                    background: white;
                    border-radius: 12px;
                    padding: 24px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                .widget-container h3 {
                    margin: 0 0 12px 0;
                    color: #667eea;
                }
                .widget-container p {
                    margin: 0 0 16px 0;
                    color: #666;
                }
                button {
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    font-weight: 600;
                    cursor: pointer;
                }
                button:hover {
                    background: #5568d3;
                }
            """)
        ),
        air.Body(
            air.Div(
                air.H3("Air Widget"),
                air.P("This widget is embedded in an iframe and built with Python Air!"),
                air.Button(
                    "Click Me",
                    onclick="alert('Hello from the iframe widget!')"
                ),
                class_="widget-container"
            )
        )
    )
```

### Embed on External Sites

Users can now embed your widget with a simple iframe tag:

```html
<iframe
    src="http://your-domain.com/widget/embed"
    width="400"
    height="250"
    frameborder="0"
    style="border: none; border-radius: 12px;">
</iframe>
```

### Add Configuration Support

The iframe widget can be made configurable via URL parameters:

```python
from fastapi import Query

@app.get("/widget/embed")
async def widget_iframe(
    title: str = Query("Air Widget"),
    theme: str = Query("purple")
):
    """Configurable iframe widget"""

    # Theme colors
    themes = {
        "purple": {"gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "color": "#667eea"},
        "blue": {"gradient": "linear-gradient(135deg, #2196F3 0%, #1976D2 100%)", "color": "#2196F3"},
        "green": {"gradient": "linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)", "color": "#4CAF50"},
    }

    selected_theme = themes.get(theme, themes["purple"])

    return air.Html(
        air.Head(
            air.Style(f"""
                body {{
                    margin: 0;
                    padding: 20px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: {selected_theme['gradient']};
                }}
                .widget-container {{
                    background: white;
                    border-radius: 12px;
                    padding: 24px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .widget-container h3 {{
                    margin: 0 0 12px 0;
                    color: {selected_theme['color']};
                }}
                .widget-container p {{
                    margin: 0 0 16px 0;
                    color: #666;
                }}
                button {{
                    background: {selected_theme['color']};
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    font-weight: 600;
                    cursor: pointer;
                }}
            """)
        ),
        air.Body(
            air.Div(
                air.H3(title),
                air.P(f"Theme: {theme}"),
                air.Button("Click Me", onclick="alert('Hello!')"),
                class_="widget-container"
            )
        )
    )
```

Now users can customize the widget:

```html
<iframe
    src="http://your-domain.com/widget/embed?title=My+Widget&theme=blue"
    width="400"
    height="250"
    frameborder="0">
</iframe>
```

## The Script Injection Approach Step-by-Step

For more integrated widgets, script injection provides better flexibility.

### Step 1: Create the Widget Loader Script

```python
from fastapi.responses import Response

@app.get("/embed/widget.js")
async def widget_loader_script():
    """JavaScript loader that external sites can embed"""
    js_code = """
(function() {
    // Inject scoped styles
    const style = document.createElement('style');
    style.textContent = `
        .air-widget {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            max-width: 400px;
        }
        .air-widget h3 {
            margin: 0 0 12px 0;
            font-size: 24px;
        }
        .air-widget p {
            margin: 0 0 16px 0;
            opacity: 0.9;
            line-height: 1.5;
        }
        .air-widget button {
            background: white;
            color: #667eea;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .air-widget button:hover {
            transform: translateY(-2px);
        }
    `;
    document.head.appendChild(style);

    // Fetch and inject widget content
    const container = document.getElementById('air-widget-container');
    if (!container) {
        console.error('Air widget container not found. Add <div id="air-widget-container"></div>');
        return;
    }

    fetch(window.location.origin.includes('localhost')
        ? 'http://localhost:8000/api/widget-content'
        : 'http://your-domain.com/api/widget-content'
    )
        .then(response => response.text())
        .then(html => {
            container.innerHTML = html;
        })
        .catch(error => {
            console.error('Failed to load Air widget:', error);
            container.innerHTML = '<p>Widget failed to load</p>';
        });
})();
    """

    return Response(
        content=js_code,
        media_type="application/javascript",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "public, max-age=3600"
        }
    )
```

### Step 2: Create the Widget Content Endpoint

```python
@app.get("/api/widget-content")
async def widget_html_content():
    """Returns the widget HTML"""
    widget = air.Div(
        air.H3("🚀 Air Widget"),
        air.P("This widget is dynamically loaded and can be embedded anywhere!"),
        air.Button(
            "Click Me!",
            onclick="alert('Hello from Air widget!')"
        ),
        class_="air-widget"
    )

    return Response(
        content=str(widget),
        media_type="text/html",
        headers={
            "Access-Control-Allow-Origin": "*",

            "Content-Type": "text/html; charset=utf-8"
        }
    )
```

When you want to vary the widget depending on where it's included, check

```python
@app.get("/api/widget-content/{code}")
async def widget_html_content(code):
    """Returns the widget HTML for code"""
    allowed_origins = {
        'a': ('https://example.com',),
        'b': 
    }
    if code not in allowed_origins.keys():
        # return not found
    # check request origin
    origin = ""
    if origin not in allowed_origins[a]:
        # return not found

    widget = air.Div(
        air.H3(f"🚀 Air Widget for {code}"),
        air.P("This widget is dynamically loaded and can be embedded only on!"),
        air.Button(
            "Click Me!",
            onclick="alert('Hello from Air widget!')"
        ),
        class_="air-widget"
    )

    return Response(
        content=str(widget),
        media_type="text/html",
        headers={
            "Access-Control-Allow-Origin": f"{origin}",
            "Vary": "Origin",
            "Content-Type": "text/html; charset=utf-8"
        }
    )
```

Note https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Allow-Origin

### Step 3: Embed on External Sites

Users embed your widget with just two lines:

```html
<div id="air-widget-container"></div>
<script src="http://your-domain.com/embed/widget.js"></script>
```

### Step 4: Add Configuration Support

Make the script injection widget configurable:

```python
@app.get("/embed/widget.js")
async def widget_loader_script(
    title: str = Query("Air Widget"),
    theme: str = Query("purple")
):
    """Configurable widget loader"""
    js_code = f"""
(function() {{
    const config = {{
        title: '{title}',
        theme: '{theme}'
    }};

    // Inject theme-aware styles
    const themes = {{
        purple: {{ bg: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', btnColor: '#667eea' }},
        blue: {{ bg: 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)', btnColor: '#2196F3' }},
        green: {{ bg: 'linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)', btnColor: '#4CAF50' }}
    }};

    const selectedTheme = themes[config.theme] || themes.purple;

    const style = document.createElement('style');
    style.textContent = `
        .air-widget {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: ${{selectedTheme.bg}};
            color: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            max-width: 400px;
        }}
        .air-widget h3 {{
            margin: 0 0 12px 0;
        }}
        .air-widget p {{
            margin: 0 0 16px 0;
            opacity: 0.9;
        }}
        .air-widget button {{
            background: white;
            color: ${{selectedTheme.btnColor}};
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
        }}
    `;
    document.head.appendChild(style);

    const container = document.getElementById('air-widget-container');
    if (!container) return;

    const baseUrl = window.location.origin.includes('localhost')
        ? 'http://localhost:8000'
        : 'http://your-domain.com';

    fetch(`${{baseUrl}}/api/widget-content?title=${{encodeURIComponent(config.title)}}&theme=${{config.theme}}`)
        .then(r => r.text())
        .then(html => container.innerHTML = html)
        .catch(err => console.error('Widget load failed:', err));
}})();
    """

    return Response(
        content=js_code,
        media_type="application/javascript",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "public, max-age=3600"
        }
    )

@app.get("/api/widget-content")
async def widget_html_content(
    title: str = Query("Air Widget"),
    theme: str = Query("purple")
):
    """Returns themed widget HTML"""
    widget = air.Div(
        air.H3(f"🚀 {title}"),
        air.P(f"Theme: {theme} | Built with Python Air"),
        air.Button("Click Me!", onclick="alert('Hello!')"),
        class_="air-widget"
    )

    return Response(
        content=str(widget),
        media_type="text/html",
        headers={"Access-Control-Allow-Origin": "*"}
    )
```

Now users can configure it via URL parameters:

```html
<div id="air-widget-container"></div>
<script src="http://your-domain.com/embed/widget.js?title=Custom+Title&theme=blue"></script>
```

## Complete Working Example

Here's a complete embeddable widget application with both approaches:

```python
import air
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi import Query

app = air.Air()

# Configure CORS (TODO: how to configure it for specific endpoints?)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Demo page 
# TODO: how to make the code configurable with data attributes?
@app.get("/")
async def home():
    """Demo page showing both embedding approaches"""
    return air.Html(
        air.Head(
            air.Title("Air Widget Demo"),
            air.Style("""
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 40px 20px;
                }
                h1 { color: #333; }
                h2 { color: #667eea; margin-top: 40px; }
                .demo-section {
                    margin: 30px 0;
                    padding: 20px;
                    background: #f5f5f5;
                    border-radius: 8px;
                }
                code {
                    background: #2d2d2d;
                    color: #f8f8f2;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-size: 0.9em;
                }
                pre {
                    background: #2d2d2d;
                    color: #f8f8f2;
                    padding: 15px;
                    border-radius: 8px;
                    overflow-x: auto;
                }
            """)
        ),
        air.Body(
            air.H1("Python Air Widget Embedding Demo"),
            air.P("Two approaches to embed widgets on external websites"),

            air.H2("1. Iframe Approach"),
            air.Div(
                air.H3("Demo:"),
                air.Tag("iframe",
                    src="/widget/embed?title=Iframe+Widget&theme=purple",
                    width="400",
                    height="250",
                    frameborder="0",
                    style="border: none; border-radius: 12px;"
                ),
                air.H3("Embedding code:"),
                air.Tag("pre", air.Code(
                    """<iframe
    src="http://your-domain.com/widget/embed?title=My+Widget&theme=blue"
    width="400"
    height="250"
    frameborder="0">
</iframe>"""
                )),
                class_="demo-section"
            ),

            air.H2("2. Script Injection Approach"),
            air.Div(
                air.H3("Demo:"),
                air.Div(id="air-widget-container"),
                air.Script(src="/embed/widget.js?title=Script+Widget&theme=blue"),
                air.H3("Embedding code:"),
                air.Tag("pre", air.Code(
                    """<div id="air-widget-container"></div>
<script src="http://your-domain.com/embed/widget.js?title=Custom&theme=green"></script>"""
                )),
                class_="demo-section"
            ),

            air.H2("Available Themes"),
            air.P("Both approaches support: ", air.Code("purple"), ", ",
                  air.Code("blue"), ", ", air.Code("green"))
        )
    )

# Iframe endpoints
@app.get("/widget/embed")
async def widget_iframe(
    title: str = Query("Air Widget"),
    theme: str = Query("purple")
):
    themes = {
        "purple": {"gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "color": "#667eea"},
        "blue": {"gradient": "linear-gradient(135deg, #2196F3 0%, #1976D2 100%)", "color": "#2196F3"},
        "green": {"gradient": "linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)", "color": "#4CAF50"},
    }
    selected_theme = themes.get(theme, themes["purple"])

    return air.Html(
        air.Head(
            air.Style(f"""
                body {{
                    margin: 0;
                    padding: 20px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: {selected_theme['gradient']};
                }}
                .widget-container {{
                    background: white;
                    border-radius: 12px;
                    padding: 24px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .widget-container h3 {{
                    margin: 0 0 12px 0;
                    color: {selected_theme['color']};
                }}
                .widget-container p {{
                    margin: 0 0 16px 0;
                    color: #666;
                }}
                button {{
                    background: {selected_theme['color']};
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    font-weight: 600;
                    cursor: pointer;
                }}
            """)
        ),
        air.Body(
            air.Div(
                air.H3(title),
                air.P(f"Iframe widget with {theme} theme"),
                air.Button("Click Me", onclick="alert('Hello from iframe!')"),
                class_="widget-container"
            )
        )
    )

# Script injection endpoints
@app.get("/embed/widget.js")
async def widget_loader_script(
    title: str = Query("Air Widget"),
    theme: str = Query("purple")
):
    js_code = f"""
(function() {{
    const themes = {{
        purple: {{ bg: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', btnColor: '#667eea' }},
        blue: {{ bg: 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)', btnColor: '#2196F3' }},
        green: {{ bg: 'linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)', btnColor: '#4CAF50' }}
    }};

    const selectedTheme = themes['{theme}'] || themes.purple;

    const style = document.createElement('style');
    style.textContent = `
        .air-widget {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: ${{selectedTheme.bg}};
            color: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            max-width: 400px;
        }}
        .air-widget h3 {{
            margin: 0 0 12px 0;
            font-size: 24px;
        }}
        .air-widget p {{
            margin: 0 0 16px 0;
            opacity: 0.9;
        }}
        .air-widget button {{
            background: white;
            color: ${{selectedTheme.btnColor}};
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        .air-widget button:hover {{
            transform: translateY(-2px);
        }}
    `;
    document.head.appendChild(style);

    const container = document.getElementById('air-widget-container');
    if (!container) {{
        console.error('Container #air-widget-container not found');
        return;
    }}

    fetch(window.location.origin + '/api/widget-content?title={title}&theme={theme}')
        .then(r => r.text())
        .then(html => container.innerHTML = html)
        .catch(err => console.error('Widget failed:', err));
}})();
    """

    return Response(
        content=js_code,
        media_type="application/javascript",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "public, max-age=3600"
        }
    )

@app.get("/api/widget-content")
async def widget_html_content(
    title: str = Query("Air Widget"),
    theme: str = Query("purple")
):
    widget = air.Div(
        air.H3(f"🚀 {title}"),
        air.P(f"Script injection widget with {theme} theme"),
        air.Button("Click Me!", onclick="alert('Hello from script widget!')"),
        class_="air-widget"
    )

    return Response(
        content=str(widget),
        media_type="text/html",
        headers={"Access-Control-Allow-Origin": "*"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Testing Your Widget

1. Save the code as `app.py`
2. Run the server:

```bash
python app.py
```

3. Visit `http://localhost:8000` to see both embedding approaches in action
4. Test embedding on external sites (or create a test HTML file)

## Best Practices

### CSS Isolation

For script injection widgets, use unique class prefixes to avoid conflicts:

```python
# Good: namespaced classes
air.Div(class_="mycompany-widget-container")

# Bad: generic classes that might conflict
air.Div(class_="container")
```

### CORS Configuration

For production, restrict CORS to specific domains:

# TODO: Maybe wrapping the app in CORSMW required for applying to error responses:
# app = Starlette()
# app = CORSMiddleware(app=app, allow_origins=["*"])
# see https://www.starlette.dev/middleware/
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://trusted-site1.com",
        "https://trusted-site2.com"
    ],
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)
```

### Rate Limiting

Protect your widget endpoints with rate limiting:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/embed/widget.js")
@limiter.limit("100/minute")
async def widget_loader_script(request: Request):
    # ... widget code
    pass
```

### Caching

Use appropriate cache headers for better performance:

```python
headers = {
    "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
    "Access-Control-Allow-Origin": "*"
}
```

### Security

- Sanitize any user input in configuration parameters
- Use HTTPS in production
- Consider CSP (Content Security Policy) headers
- Don't include sensitive data in widgets
- Validate and escape any dynamic content

## Choosing the Right Approach

**Use iframe embedding when:**
- You need strong style isolation
- The widget should be a fixed size
- You don't need parent-child communication
- Simplicity is more important than flexibility
- You want maximum compatibility

**Use script injection when:**
- You need responsive sizing
- You want parent-child communication
- You need access to parent page context
- You want a more integrated feel
- You're comfortable managing CSS conflicts

## Conclusion

Python Air makes it surprisingly simple to create embeddable widgets entirely in Python. The framework's type-safe HTML generation and FastAPI foundation provide a solid base for building production-ready widgets.

Whether you choose the iframe approach for its simplicity and isolation, or the script injection approach for its flexibility, Air's composable tag system makes both approaches straightforward to implement.

The complete example code is available at the [Air documentation](https://feldroy.github.io/air/) and you can find more examples in the [Air GitHub repository](https://github.com/feldroy/air).

Happy widget building!
